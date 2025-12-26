from django.urls import path
from .views import UserListCreate, UserDetail

urlpatterns = [
    path('', UserListCreate.as_view(), name='user-list'),  # changed 'users/' to ''
    path('<int:pk>/', UserDetail.as_view(), name='user-detail'),  # removed 'users/' from the start
]
