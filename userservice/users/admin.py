from django.contrib import admin
from .models import User, APIKey, UserData
from .utils import decrypt_text


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # list_display = ('id', 'data', 'referral_code')  # Відображаємо ідентифікатор користувача та атрибути
    list_display = ('id', 'referral_code', 'my_referral_code')
    search_fields = ('id',)  # Поле для пошуку за ідентифікатором
    list_filter = ('id',)  # Фільтр за ідентифікатором

    def get_user_attributes(self, obj):
        return obj.attributes  # Повертаємо атрибути користувача
    get_user_attributes.short_description = 'User Attributes'

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('field', 'value', 'user_id')
    search_fields = ('user_id',)
    list_filter = ('user_id',)


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'key_name', 'exchange', 'get_decrypted_secret')  # Відображаємо користувача, ключ і розшифрований секрет
    search_fields = ('user__user_id', 'key_value')  # Пошук за ідентифікатором користувача та ключем
    list_filter = ('user', 'key_value')  # Фільтрація за користувачем і ключем

    # Отображение расшифрованного секрета
    def get_decrypted_secret(self, obj):
        try:
            return decrypt_text(obj.secret)  # Розшифровуємо секрет для відображення
        except Exception:
            return "Ошибка расшифровки"
    get_decrypted_secret.short_description = 'Decrypted Secret'


