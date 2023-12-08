from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):
    return render(request,'mainapp/home.html')

def interactive_map(request):
    return HttpResponse("interactive map")

def route(request):
    return HttpResponse("route")

def bicimad_status(request):
    return HttpResponse("bicimad")

def bicimad_ui(request):
    return HttpResponse("bicimad_ui")

