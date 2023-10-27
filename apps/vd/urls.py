from django.urls import path, include, re_path
from . import views

urlpatterns = [
        path('',views.home, name='home'),
        path("test", views.dash_test, name=""),
        path("carga-padron", views.carga_padron, name="carga_padron"),
        path("padron", views.dashboard_padron_general, name="padron_dash"),
        path("carga-compromiso", views.carga_compromiso, name="carga_compromiso"),
        path("compromiso", views.dashboard_compromiso_general, name="compromiso_dash"),
        path("unir-data", views.concatenar_data, name="concatenar_data"),
        path("extraer-data-padron", views.extraer_data_padron, name="extraer_data_padron"),
        
        
        path("ingesta-any", views.ingesta_any, name="ingesta_any"),
        path("dashboard-seguimiento", views.dashboard_seguimiento_indicadores, name="dashboard_seguimiento"),
        path("analisis-report-vd", views.dashboard_analisis_inicio_vd, name="analisis_vd"),
        path("vd_detalle_resultados", views.dashboard_resultados_indicadores, name="vd_detalle_resultados"),
        
        path("vd-oportunas", views.dashboard_indicador_vd_oportunas, name="vd_oportunas"),
        path("vd-consecutivas", views.dashboard_indicador_vd_consecutivas, name="vd_consecutivas"),
        path("vd-georreferenciadas", views.dashboard_indicador_vd_georreferenciadas, name="vd_georreferenciadas"),
        #
]