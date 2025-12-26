####################controller :
from django.http import JsonResponse
from ..models import RegisteredServices
from django.views.decorators.csrf import csrf_exempt 
from suds.client import Client 
import json



def index(request):
      services = RegisteredServices.objects.values()
      services_res = {
            "RegisteredServices":list(services)
      }
      return JsonResponse(services_res)

@csrf_exempt
def create(request):
    if request.method == 'POST':
        # Parse the JSON data from request body
        data = json.loads(request.body)
        new_service = RegisteredServices()
        new_service.name = data.get('name')
        new_service.description = data.get('description')
        new_service.endpoint = data.get('endpoint')

        new_service.save()

        services = RegisteredServices.objects.values()
        services_res = {
            "message": "Service created successfully",
            "service": list(services)
        }
        return JsonResponse(services_res, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def update(request, service_id):
    if request.method == 'PUT':
        service = RegisteredServices.objects.filter(id=service_id).first()
        data = request.body.decode('utf-8')
        data = json.loads(data)
            
        # Update the task name
        service.name = data.get('name', service.name)
        service.description = data.get('description', service.description)
        service.endpoint = data.get('endpoint', service.endpoint)

        service.save()

        return JsonResponse({'message': 'Service updated successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'})
    


@csrf_exempt
def destroy(request,service_id):
      service = RegisteredServices.objects.filter(id=service_id).first()
      service.delete()
      return JsonResponse({'message': 'Service Deleted successfully'})
     
def discover_services(request):
    if request.method == 'GET':
        services = RegisteredServices.objects.filter(name=request.GET.get('name')).all()
        available_service = []

        for service in services:
            try: 
                Client(service.endpoint +'?WSDL')
                available_service.append({
                    'id': service.id,
                    'name': service.name,
                    'endpoint': service.endpoint,
                    'description': service.description
                })
            except:
                 continue
            
        if len(available_service) > 0:
            return JsonResponse({'service': available_service})  
            #return JsonResponse({'service': {'id':available_service.id,'name': available_service.name, 'endpoint': available_service.endpoint , 'description': available_service.description}})
        else:
            return JsonResponse({'error': 'No available services found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'},status= 405)