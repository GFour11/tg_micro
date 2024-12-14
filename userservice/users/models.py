import os
import string
import random
from django.db import models
from cryptography.fernet import Fernet


ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

if not ENCRYPTION_KEY:
    raise ValueError("Ключ шифрування не знайдено в змінній середовища ENCRYPTION_KEY")

cipher = Fernet(ENCRYPTION_KEY)

def generate_random_link(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class User(models.Model):
    id = models.AutoField(primary_key=True)  # Автоінкрементне поле
    user_id = models.BigIntegerField(unique=True)  # Ідентифікатор користувача, який передається вручну (наприклад, для Telegram)
    referral_code = models.CharField(max_length=10) # Реферальний код
    my_referral_code = models.CharField(max_length=10, default=generate_random_link)

    def __str__(self):
        return f"User {self.id}"

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'


class UserData(models.Model):
    field = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')

    class Meta:
        verbose_name = 'Дані користувача'
        verbose_name_plural = 'Дані користувача'


class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys', to_field='id')  # Указываем связь по id
    key_name = models.CharField(max_length=255, unique=True, blank=True)  # Унікальний ID ключа
    key_value = models.CharField(max_length=255)  # Назва ключа
    secret = models.CharField(max_length=255)  # Зашифрований секрет
    exchange = models.CharField(max_length=255)  # Назва біржі

    def save(self, *args, **kwargs):
        # Шифруємо secret перед збереженням
        if not self.is_encrypted(self.secret):
            self.secret = cipher.encrypt(self.secret.encode()).decode()
        super().save(*args, **kwargs)

    def is_encrypted(self, value: str) -> bool:
        try:
            cipher.decrypt(value.encode())
            return True
        except Exception:
            return False

    def get_decrypted_secret(self) -> str:
        # Дешифруємо секрет перед передачею
        return cipher.decrypt(self.secret.encode()).decode()

    def __str__(self):
        return f"Ключ {self.key_name} для користувача {self.user.user_id}"

    class Meta:
        verbose_name = 'API Ключ'
        verbose_name_plural = 'API Ключі'

