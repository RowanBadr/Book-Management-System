from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json

from django.db import connection
from django.core.exceptions import ImproperlyConfigured

User = get_user_model()

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password')
        )
        user.save()
        return JsonResponse({'message': 'User created successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_user(request, user_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            user = User.objects.get(id=user_id)
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.save()
            return JsonResponse({'message': 'User updated successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def list_users(request):
    if request.method == 'GET':
        users = User.objects.all().values('id', 'username', 'email')
        return JsonResponse(list(users), safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



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