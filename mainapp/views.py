from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

from .forms import CreateUserForm

def login_page(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
    context={}
    return render(request,'mainapp/login.html',context)

def logout_user(request):
    logout(request)
    return redirect('login')

def register(request):
    form = CreateUserForm()

    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for '+ user)
            return redirect('login')
    context = {'form':form}
    return render(request,'mainapp/register.html',context)


def home(request):
    return render(request,'mainapp/home.html')

def interactive_map(request):
    return HttpResponse("interactive map")

def route(request):
    return HttpResponse("route")

def bicimad_status(request):
    return HttpResponse("bicimad")


@login_required(login_url='login')
def bicimad_ui(request):
    return HttpResponse("bicimad_ui")



