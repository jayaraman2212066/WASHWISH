from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
import os

def index(request):
    return render(request, "index.html")

def services(request):
    return render(request, "services.html")
    
def about(request):
    return render(request, "about.html")

def health_check(request):
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "OK"
    except Exception as e:
        db_status = f"Error: {str(e)}"

    # Check environment
    env_status = {
        "DEBUG": os.environ.get("DEBUG", "Not set"),
        "DATABASE_URL": "Set" if os.environ.get("DATABASE_URL") else "Not set",
        "SECRET_KEY": "Set" if os.environ.get("SECRET_KEY") else "Not set",
    }

    response_data = {
        "status": "healthy",
        "database": db_status,
        "environment": env_status
    }

    return JsonResponse(response_data)
