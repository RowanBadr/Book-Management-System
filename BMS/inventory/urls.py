from django.urls import path
from .services.inventoryService import create_book, update_book, delete_book, list_books, health_check, get_book_details
from .services.reviewsService import (
    create_review, update_review, delete_review, list_reviews, health_check as reviews_health_check
)
from .services.userService import (
    create_user, update_user, delete_user, list_users, health_check as users_health_check
)
from .controllers.RegisteredServices import index, create, update, destroy, discover_services

urlpatterns = [
    # Inventory URL patterns
    path('books/details/<int:book_id>/', get_book_details, name='get_book_details'),

    path('books/', list_books, name='list_books'),
    path('books/create/', create_book, name='create_book'),
    path('books/update/<int:book_id>/', update_book, name='update_book'),
    path('books/delete/<int:book_id>/', delete_book, name='delete_book'),
    path('health/', health_check, name='inventory_health_check'),

    # Reviews URL patterns
    path('reviews/', list_reviews, name='list_reviews'),
    path('reviews/create/', create_review, name='create_review'),
    path('reviews/update/<int:review_id>/', update_review, name='update_review'),
    path('reviews/delete/<int:review_id>/', delete_review, name='delete_review'),
    path('reviews/health/', reviews_health_check, name='reviews_health_check'),
    
    # Users URL patterns
    path('users/', list_users, name='list_users'),
    path('users/create/', create_user, name='create_user'),
    path('users/update/<int:user_id>/', update_user, name='update_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('users/health/', users_health_check, name='users_health_check'),

    # Registered Services URL patterns
    path("registerServices/", index, name='service_index'),
    path("registerServices/create/", create, name='service_create'),
    path("registerServices/update/<int:service_id>/", update, name='service_update'),
    path("registerServices/destroy/<int:service_id>/", destroy, name='service_destroy'),
    path("registerServices/discovery/", discover_services, name='service_discovery'),
]
