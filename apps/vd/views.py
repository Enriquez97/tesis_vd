from django.shortcuts import render
from apps.vd.layouts.dash_padron import dash_carga_padron,dash_padron_nominal
from apps.vd.layouts.dash_compromiso import dash_carga_compromiso,dash_compromiso,dash_descarga_data_compromiso
def home(request):
    
    #dash=Home()
    #context={'dashboard':dash}
    return render(request, 'home.html')#,context

def dash_test(request):
    #owo=request.user.id
    dashboard = dash_descarga_data_compromiso()
    context={'dashboard':dashboard}
    return render(request, 'dash.html',context)

def carga_padron(request):
    context = {'dashboad':dash_carga_padron()}
    return render(request, 'carga_padron.html',context)

#dash_padron_nominal

def dashboard_padron_general(request):
    context = {'dashboad':dash_padron_nominal()}
    return render(request, 'dash_padron_general.html',context)


def carga_compromiso(request):
    context = {'dashboad':dash_carga_compromiso()}
    return render(request, 'carga_compromiso.html',context)

def dashboard_compromiso_general(request):
    context = {'dashboad':dash_compromiso()}
    return render(request, 'dash_compromiso_general.html',context)