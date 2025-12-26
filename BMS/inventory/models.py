from django.db import models
from django.conf import settings
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    publish_date = models.DateField()
    ISBN = models.CharField(max_length=13)  # ISBN number typically has 13 characters

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews_reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_review_users')
    # Other fields...
    rating = models.IntegerField(default=1, choices=((1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')))
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating} Stars: {self.comment[:20]}...'  # Display the first 20 characters of the comment


class RegisteredServices(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    endpoint = models.CharField(max_length=100)