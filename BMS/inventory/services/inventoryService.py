from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt

import json
from django.db import connection
from django.core.exceptions import ImproperlyConfigured

from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
from ..models import Book
import json


def get_book_details(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        response_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'publish_date': book.publish_date.strftime('%Y-%m-%d'),
            'ISBN': book.ISBN
        }
        return JsonResponse(response_data, status=200)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)


#@csrf_exempt
def create_book(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_book = Book(
            title=data.get('title'),
            author=data.get('author'),
            publish_date=data.get('publish_date'),
            ISBN=data.get('ISBN')
        )
        new_book.save()
        return JsonResponse({'message': 'Book created successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

#@csrf_exempt
def update_book(request, book_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            book = Book.objects.get(id=book_id)
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)
            book.publish_date = data.get('publish_date', book.publish_date)
            book.ISBN = data.get('ISBN', book.ISBN)
            book.save()
            return JsonResponse({'message': 'Book updated successfully'}, status=200)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

#@csrf_exempt
def delete_book(request, book_id):
    if request.method == 'DELETE':
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return JsonResponse({'message': 'Book deleted successfully'}, status=200)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def list_books(request):
    if request.method == 'GET':
        books = Book.objects.all().values()
        return JsonResponse(list(books), safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def health_check(request):
    # Simple health check endpoint for the service
    return JsonResponse({'status': 'Inventory service is up and running'}, status=200)





def health_check(request):
    """
    Performs a health check of the service, including a database connectivity check.
    """
    health_data = {
        'status': 'healthy',
        'database': 'connected'
    }
    
    # Checking database connectivity
    try:
        # Attempt to make a query to the database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception as e:
        # Update the health data if there is an issue with the database
        health_data['status'] = 'unhealthy'
        health_data['database'] = 'disconnected'
        health_data['error'] = str(e)

    # Return the health check data
    if health_data['status'] == 'healthy':
        return JsonResponse(health_data, status=200)
    else:
        return JsonResponse(health_data, status=500)