from cryptography.fernet import Fernet
import os
from .models import UserData

# Отримуємо ключ шифрування зі змінної оточення
encryption_key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
cipher = Fernet(encryption_key)

def encrypt_text(plain_text):
    return cipher.encrypt(plain_text.encode()).decode()

def decrypt_text(encrypted_text):
    return cipher.decrypt(encrypted_text.encode()).decode()

def get_user_data(user):
    user_data = UserData.objects.filter(user_id=user)
    user_data_dict = {data.field: data.value for data in user_data}
    user_data_dict["user_id"] = user.id
    return user_data_dict

def delete_user_data(user):
    UserData.objects.filter(user_id=user).delete()

def update_user_data(user, new_data):
    for field, value in new_data.items():
        user_data_entry, created = UserData.objects.get_or_create(user_id=user, field=field)
        user_data_entry.value = value
        user_data_entry.save()


