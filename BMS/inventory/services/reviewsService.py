from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Review
import json
from ..models import Book
import requests



def create_review(request):
    if request.method == 'POST':
        data = request.json()
        book_id = data.get('book_id')

        # Call the Inventory Service to check if the book exists
        response = requests.get(f'http://127.0.0.1:8000/inventory/books/details/{book_id}/')
        if response.status_code == 404:
            return JsonResponse({'error': 'Book not found'}, status=404)

        # If the book exists, proceed to create the review
        review = Review(
            book_id=book_id,
            user_id=data.get('user_id'),
            rating=data.get('rating'),
            comment=data.get('comment')
        )
        review.save()
        return JsonResponse({'message': 'Review created successfully'}, status=201)
    
    
@csrf_exempt
def create_review(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_review = Review(
                book_id=data.get('book_id'),  # Assuming 'book_id' is used instead of 'product_id'
                user_id=data.get('user_id'),  # Assuming user_id is required
                rating=data.get('rating'),
                comment=data.get('comment')
            )
            new_review.save()
            return JsonResponse({'message': 'Review created successfully', 'review_id': new_review.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_review(request, review_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            review = Review.objects.get(id=review_id)
            review.rating = data.get('rating', review.rating)
            review.comment = data.get('comment', review.comment)
            review.save()
            return JsonResponse({'message': 'Review updated successfully'}, status=200)
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_review(request, review_id):
    if request.method == 'DELETE':
        try:
            review = Review.objects.get(id=review_id)
            review.delete()
            return JsonResponse({'message': 'Review deleted successfully'}, status=200)
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def list_reviews(request):
    if request.method == 'GET':
        reviews = Review.objects.all().values('id', 'book_id', 'user_id', 'rating', 'comment')
        return JsonResponse(list(reviews), safe=False, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def health_check(request):
    """
    Health check for the reviews service.
    """
    try:
        # Simple query to check database connectivity
        Review.objects.exists()
        return JsonResponse({'status': 'healthy', 'database': 'connected'}, status=200)
    except:
        return JsonResponse({'status': 'unhealthy', 'database': 'disconnected'}, status=500)
