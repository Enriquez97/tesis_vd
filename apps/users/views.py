from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from apps.users.models import Municipalidad,Profile
from django.contrib.auth.models import User
# Create your views here.
def update_profile(request):
     return render(request,'users/update_profile.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user:
                login(request, user)
                return redirect('home')
        else:
                return render(request,'users/login.html',{'error':'Acceso Denegado'})
    return render (request,'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
