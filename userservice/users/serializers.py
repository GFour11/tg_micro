from rest_framework import serializers
from .models import User, APIKey

# Серіалізатор для користувача
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'data']

# Серіалізатор для ключів користувача
class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ['key_name', 'key_value', 'secret']
