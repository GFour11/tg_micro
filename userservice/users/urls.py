from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/<int:user_id>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
    path('users/<int:user_id>/keys/', UserViewSet.as_view({'post': 'create_key', 'get': 'list_keys'}), name='user-key-list'),
    path('users/<int:user_id>/keys/decrypted/', UserViewSet.as_view({'get': 'list_decrypted_keys'}), name='user-decrypted-key-list'),
    path('users/<int:user_id>/keys/<str:key_id>/', UserViewSet.as_view({'put': 'update_key', 'delete': 'delete_key'}), name='user-key-detail'),
]

