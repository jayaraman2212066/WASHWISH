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
    # Simplified health check
    response_data = {
        "status": "healthy",
        "message": "Application is running"
    }
    return JsonResponse(response_data)

# New simple status check view
def status_check(request):
    return JsonResponse({"status": "ok"})
