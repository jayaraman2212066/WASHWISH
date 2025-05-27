from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "index.html")

def services(request):
    return render(request, "services.html")
    
def about(request):
    return render(request, "about.html")

def health_check(request):
    return HttpResponse("OK", content_type="text/plain")
