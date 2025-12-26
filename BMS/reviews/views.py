# views.py
from django.conf import settings
from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer
import requests


class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


def call_inventory_service():
    inventory_service = settings.SERVICES['inventory']
    url = f"http://{inventory_service['host']}:{inventory_service['port']}/api/path"
    # Use requests or similar library to make the network call
    response = requests.get(url)
    return response.json()
