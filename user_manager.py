import os
import sys
from datetime import datetime

import django
from asgiref.sync import sync_to_async

from microservice_core.messages.message import ErrorBody

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/userservice')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userservice.settings')
django.setup()

from users.models import User, APIKey, UserData
from users.utils import get_user_data, delete_user_data, update_user_data
from custom_classes import UsersResponseBody


class UserManager:
    @sync_to_async
    def get_or_create(self, request):
        try:
            user_id = request["user_id"]
            user_data = request["user_data"]
        except KeyError:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=400, error_message="Неправильний формат запиту",
                                                     timestamp=datetime.utcnow().isoformat()))
        referral_code = request["referral_code"]
        if referral_code is None:
            referral_code = ''

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            user = User.objects.create(user_id=user_id, referral_code=referral_code)
            for field, value in user_data.items():
                if value is not None:
                    UserData.objects.create(user_id=user, field=field, value=value)

        return UsersResponseBody(status="success", message="Пользователь добавлен.")


    @sync_to_async
    def delete_user_internal(self, request):
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
        delete_user_data(user)
        user.delete()
        return UsersResponseBody(status="success", message="Користувач видалений.")

    @sync_to_async
    def get_user_info_internal(self, request):
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
        user_data = get_user_data(user)
        return UsersResponseBody(status="success", message=user_data)

    @sync_to_async
    def get_all_users(self, request):
        users = User.objects.all()
        result = [get_user_data(user) for user in users]
        return UsersResponseBody(status="success", message=result)

    @sync_to_async
    def update_user_internal(self, request):
        try:
            user_id = request["user_id"]
            user_data = request["user_data"]
        except KeyError:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=400, error_message="Неправильний формат запиту",
                                                     timestamp=datetime.utcnow().isoformat()))
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return UsersResponseBody(status="error", error=ErrorBody(error_code=401, error_message="Користувач не знайдений",
                                                     timestamp=datetime.utcnow().isoformat()))
        update_user_data(user, user_data)
        return UsersResponseBody(status="success", message="Користувач змінений.")
