import os
import sys
from datetime import datetime

import django
from django.forms.models import model_to_dict
from cryptography.fernet import Fernet
from asgiref.sync import sync_to_async

from microservice_core.messages.message import ErrorBody
from users.models import User, APIKey
from custom_classes import UsersResponseBody

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/userservice')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userservice.settings')
django.setup()

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

if not ENCRYPTION_KEY:
    raise ValueError("Ключ шифрування не знайдено у змінній оточення ENCRYPTION_KEY")

cipher = Fernet(ENCRYPTION_KEY)

class KeyManager:
    @sync_to_async
    def add_key(self, request):
        try:
            user_id = request["user_id"]
            key_data = request["key_data"]
            key_name = key_data["key"]
            key_secret = key_data["secret"]
            key_exchange = key_data["exchange"]
        except KeyError:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=400, error_message="Неправильний формат запиту",
                                                     timestamp=datetime.utcnow().isoformat()))
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=401, error_message="Користувач не знайдений",
                                                     timestamp=datetime.utcnow().isoformat()))
        if not key_name or not key_secret:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=400, error_message="key і secret обов'язкові",
                                                     timestamp=datetime.utcnow().isoformat()))

        # Створюємо новий ключ для користувача
        try:
            user_key = APIKey(user=user, key_name=key_name, secret=key_secret, exchange=key_exchange)
            user_key.save()
        except django.db.utils.IntegrityError:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=409, error_message="Ключ з таким іменем вже присутній",
                                                     timestamp=datetime.utcnow().isoformat()))
        return UsersResponseBody(status="success", message=model_to_dict(user_key))


    @sync_to_async
    def add_key_internal(self, request):
        try:
            user_id = request["user_id"]
            key_data = request["key_data"]
            key_name = key_data["key"]
            key_secret = key_data["secret"]
        except KeyError:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=400, error_message="Неправильний формат запиту",
                                                     timestamp=datetime.utcnow().isoformat()))
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=401, error_message="Користувач не знайдений",
                                                     timestamp=datetime.utcnow().isoformat()))
        if not key_name or not key_secret:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=400, error_message="key і secret обов'язкові",
                                                     timestamp=datetime.utcnow().isoformat()))
        encrypted_secret = cipher.encrypt(key_secret.encode()).decode()

        # Створюємо новий ключ для користувача
        user_key = APIKey(user=user, key_name=key_name, secret=encrypted_secret)
        user_key.save()
        return UsersResponseBody(status="success", message=model_to_dict(user_key))


    @sync_to_async
    def list_keys(self, request):
        try:
            user_id = request["user_id"]
        except KeyError:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=400, error_message="Неправильний формат запиту",
                                                     timestamp=datetime.utcnow().isoformat()))
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=401, error_message="Користувач не знайдений",
                                                     timestamp=datetime.utcnow().isoformat()))
        user_keys = APIKey.objects.filter(user=user)
        user_keys = [model_to_dict(key) for key in user_keys]
        return UsersResponseBody(status="success", message=user_keys)


    @sync_to_async
    def get_key_internal(self, request):
        try:
            user_id = request["user_id"]
            key_id = request["key_id"]
        except KeyError:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=400, error_message="Неправильний формат запиту",
                                                     timestamp=datetime.utcnow().isoformat()))
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=401, error_message="Користувач не знайдений",
                                                     timestamp=datetime.utcnow().isoformat()))
        try:
            key = APIKey.objects.get(id=key_id)
        except APIKey.DoesNotExist:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=404, error_message="Ключ не знайдений",
                                                     timestamp=datetime.utcnow().isoformat()))
        key.secret = key.get_decrypted_secret()
        return UsersResponseBody(status="success", message=model_to_dict(key))


    @sync_to_async
    def list_keys_internal(self, request):
        try:
            user_id = request["user_id"]
        except KeyError:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=400, error_message="Неправильний формат запиту",
                                                     timestamp=datetime.utcnow().isoformat()))
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=401, error_message="Користувач не знайдений",
                                                     timestamp=datetime.utcnow().isoformat()))
        user_keys = APIKey.objects.filter(user=user)
        user_keys = [model_to_dict(key) for key in user_keys]
        return UsersResponseBody(status="success", message=user_keys)


    @sync_to_async
    def delete_key(self, request):
        try:
            user_id = request["user_id"]
            key_id = request["key_id"]
        except KeyError:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=400, error_message="Неправильний формат запиту",
                                                     timestamp=datetime.utcnow().isoformat()))
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=401, error_message="Користувач не знайдений",
                                                     timestamp=datetime.utcnow().isoformat()))
        try:
            key = APIKey.objects.get(id=key_id)
        except APIKey.DoesNotExist:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=404, error_message="Ключ не знайдений",
                                                     timestamp=datetime.utcnow().isoformat()))
        key.delete()
        return UsersResponseBody(status="success", message="Ключ видалений.")


    @sync_to_async
    def update_key(self, request):
        try:
            key_id = request["key_id"]
            value = request["value"]
        except KeyError:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=400, error_message="Неправильний формат запиту",
                                                     timestamp=datetime.utcnow().isoformat()))
        try:
            key = APIKey.objects.get(id=key_id)
        except APIKey.DoesNotExist:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=404, error_message="Ключ не знайдений",
                                                     timestamp=datetime.utcnow().isoformat()))
        key.secret = value
        key.save()
        return UsersResponseBody(status="success", message="Ключ змінений.")
