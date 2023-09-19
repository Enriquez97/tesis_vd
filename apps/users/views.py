from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#from apps.users.models import Empresa,Usuario
from django.contrib.auth.models import User
# Create your views here.
def update_profile(request):
     return render(request,'users/update_profile.html')
"""
def login_view(request):
    empresas=list(Empresa.objects.all())
    print(empresas)
    context={'empresas':empresas}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user:
                login(request, user)
                return redirect('home')#('/cuentas_por_pagar/')
        else:
                return render(request,'users/login.html',{'error':'Invalid username and password'})
        
    return render (request,'users/login.html',context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
"""