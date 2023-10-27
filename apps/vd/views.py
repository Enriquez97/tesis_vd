from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.vd.layouts.dash_padron import dash_carga_padron,dash_padron_nominal
from apps.vd.layouts.dash_compromiso import dash_carga_compromiso,dash_compromiso,dash_descarga_data_compromiso,dashboard_indicadores_vd
from apps.vd.layouts.dash_general import dash_concatenar_data,dashboard_reporteVD_
from apps.vd.layouts.dash_extraccion_data import dash_extraer_padron
from ..vd.layouts.layouts_ingesta import dash_ingestas
from ..vd.layouts.layouts_indicadores import *
from ..vd.layouts.inicio import dash_home
@login_required
def home(request):
    context = {'dashboad':dash_home()}
    #dash=Home()
    #context={'dashboard':dash}
    return render(request, 'home.html', context)#,context
@login_required
def dash_test(request):
    #owo=request.user.id
    dashboard = dash_descarga_data_compromiso()
    context={'dashboard':dashboard}
    return render(request, 'dash.html',context)
@login_required
def carga_padron(request):
    context = {'dashboad':dash_carga_padron()}
    return render(request, 'carga_padron.html',context)

#dash_padron_nominal
@login_required
def dashboard_padron_general(request):
    context = {'dashboad':dash_padron_nominal()}
    return render(request, 'dash_padron_general.html',context)

@login_required
def carga_compromiso(request):
    context = {'dashboad':dash_carga_compromiso()}
    return render(request, 'carga_compromiso.html',context)
@login_required
def dashboard_compromiso_general(request):
    context = {'dashboad':dash_compromiso()}
    return render(request, 'dash_compromiso_general.html',context)
@login_required
def concatenar_data(request):
    context = {'dashboad':dash_concatenar_data()}
    return render(request, 'concatenar_data.html',context)
@login_required
def extraer_data_padron(request):
    context = {'dashboad':dash_extraer_padron()}
    return render(request, 'extraer_data_padron.html',context)

################### INGESTA DE DATOS
@login_required
def ingesta_any(request):
    context = {'dashboad':dash_ingestas()}
    return render(request, 'ingesta_any.html',context)
#


########DASHBOARDS
@login_required
def dashboard_seguimiento_indicadores(request):
    context = {'dashboad':dashboard_indicadores_vd()}
    return render(request, 'Dashboards/seguimiento_indicadores.html',context)

@login_required
def dashboard_analisis_inicio_vd(request):
    context = {'dashboad':dashboard_reporteVD_()}
    return render(request, 'Dashboards/analisis_inicio_vd.html',context)

@login_required
def dashboard_resultados_indicadores(request):
    context = {'dashboad':dash_indicador_resultados()}
    return render(request, 'Dashboards/vd_detalle_resultados.html',context)

@login_required
def dashboard_indicador_vd_oportunas(request):
    context = {'dashboad':dash_indicador_vd_oportunas()}
    return render(request, 'Dashboards/indicador_vd_oportunas.html',context)

@login_required
def dashboard_indicador_vd_consecutivas(request):
    context = {'dashboad':dash_indicador_vd_consecutivas()}
    return render(request, 'Dashboards/indicador_vd_consecutivas.html',context)

def dashboard_indicador_vd_georreferenciadas(request):
    context = {'dashboad':dash_indicador_vd_georreferenciadas()}
    return render(request, 'Dashboards/indicador_vd_geo.html',context)