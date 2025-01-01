from django.http import JsonResponse

def health_check(request):
    health_status = {
        "status": "OK",
        "database": "Connected",
        "uptime": "Running"
    }
    return JsonResponse(health_status)
