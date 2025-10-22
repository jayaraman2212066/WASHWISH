from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
import os
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

def index(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Admin dashboard with statistics
        from services.models import Orders, User
        from django.db.models import Sum, Count
        
        context = {
            'total_users': User.objects.filter(is_staff=False).count(),
            'total_orders': Orders.objects.count(),
            'total_revenue': Orders.objects.aggregate(Sum('totalcost'))['totalcost__sum'] or 0,
            'pending_orders': Orders.objects.exclude(statusid__status='Completed').count(),
        }
        return render(request, "admin_dashboard.html", context)
    return render(request, "index.html")

def services(request):
    return render(request, "services.html")
    
def about(request):
    return render(request, "services.html")

def health_check(request):
    # Simplified health check
    response_data = {
        "status": "healthy",
        "message": "Application is running"
    }
    return JsonResponse(response_data)

@csrf_exempt
@require_http_methods(["GET"])
def status_check(request):
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    response_data = {
        "status": "ok",
        "database": db_status,
        "environment": os.environ.get('ENVIRONMENT', 'development')
    }
    return JsonResponse(response_data)
