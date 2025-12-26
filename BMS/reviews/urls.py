from django.urls import path
from .views import ReviewListCreate, ReviewDetail

urlpatterns = [
    path('users/', ReviewListCreate.as_view(), name='review-list'),  # Handles reviews/
    path('<int:pk>/', ReviewDetail.as_view(), name='review-detail'),  # Handles reviews/<int:pk>/
]
