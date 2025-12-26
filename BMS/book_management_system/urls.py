from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include(('inventory.urls', 'inventory'), namespace='inventory')),
    path('reviews/', include(('reviews.urls', 'reviews'), namespace='reviews')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
]

# Optional: Define custom error handlers if you have custom views for these
# handler404 = 'myapp.views.my_custom_page_not_found_view'
# handler500 = 'myapp.views.my_custom_error_view'
