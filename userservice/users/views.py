import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from cryptography.fernet import Fernet
from .models import User, APIKey
from .serializers import UserSerializer, APIKeySerializer

# Завантажуємо ключ шифрування зі змінних оточення
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

if not ENCRYPTION_KEY:
    raise ValueError("Ключ шифрування не знайдено у змінній оточення ENCRYPTION_KEY")

cipher = Fernet(ENCRYPTION_KEY)


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Створення користувача з JSON-даними
    def create(self, request):
        user_id = request.data.get('user_id')
        data = request.data.get('data')

        if not user_id or not data:
            return Response({"error": "user_id і data обов'язкові"}, status=status.HTTP_400_BAD_REQUEST)

        user = User(user_id=user_id, data=data)
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Отримання всіх користувачів
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    # Отримання користувача за його ID
    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(user_id=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    # Оновлення користувача
    def update(self, request, pk=None):
        try:
            user = User.objects.get(user_id=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Видалення користувача
    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(user_id=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Створення ключа для користувача
    @action(detail=True, methods=['post'], url_path='keys')
    def create_key(self, request, user_id=None):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        key_name = request.data.get('key')
        key_secret = request.data.get('secret')

        if not key_name or not key_secret:
            return Response({"error": "key і secret обов'язкові"}, status=status.HTTP_400_BAD_REQUEST)

        # Шифруємо секрет
        encrypted_secret = cipher.encrypt(key_secret.encode()).decode()

        # Створюємо новий ключ для користувача
        user_key = APIKey(user=user, key_name=key_name, secret=encrypted_secret)
        user_key.save()

        serializer = APIKeySerializer(user_key)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Отримання всіх ключів користувача
    @action(detail=True, methods=['get'], url_path='keys')
    def list_keys(self, request, user_id=None):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user_keys = APIKey.objects.filter(user=user)
        serializer = APIKeySerializer(user_keys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Отримання одного ключа користувача
    @action(detail=True, methods=['get'], url_path='keys/(?P<key_id>[^/.]+)')
    def retrieve_key(self, request, user_id=None, key_id=None):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user_key = APIKey.objects.get(user=user, id=key_id)
        except APIKey.DoesNotExist:
            return Response({"error": "Key not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = APIKeySerializer(user_key)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Видалення ключа користувача
    @action(detail=True, methods=['delete'], url_path='keys/(?P<key_id>[^/.]+)')
    def delete_key(self, request, user_id=None, key_id=None):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user_key = APIKey.objects.get(user=user, id=key_id)
        except APIKey.DoesNotExist:
            return Response({"error": "Key not found"}, status=status.HTTP_404_NOT_FOUND)

        user_key.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Оновлення ключа користувача
    @action(detail=True, methods=['put'], url_path='keys/(?P<key_id>[^/.]+)')
    def update_key(self, request, user_id=None, key_id=None):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user_key = APIKey.objects.get(user=user, id=key_id)
        except APIKey.DoesNotExist:
            return Response({"error": "Key not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = APIKeySerializer(user_key, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Отримання всіх розшифрованих ключів користувача
    @action(detail=True, methods=['get'], url_path='keys/decrypted')
    def list_decrypted_keys(self, request, user_id=None):
        try:
            # Шукаємо користувача за user_id
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Отримуємо всі ключі користувача
        user_keys = APIKey.objects.filter(user=user)

        # Список розшифрованих ключів
        decrypted_keys = []
        for key in user_keys:
            decrypted_secret = cipher.decrypt(key.secret.encode()).decode()  # Розшифровуємо ключ
            decrypted_keys.append({
                'key_id': key.id,  # Повертаємо id ключа
                'key_name': key.key_name,
                'key_value': decrypted_secret,
                'secret': key.secret
            })

        return Response(decrypted_keys, status=status.HTTP_200_OK)

