from django.urls import path, include, re_path
from . import views

urlpatterns = [
        path('',views.home, name='home'),
        path("test", views.dash_test, name=""),
        path("carga-padron", views.carga_padron, name="carga_padron"),
        path("padron", views.dashboard_padron_general, name="padron_dash"),
        path("carga-compromiso", views.carga_compromiso, name="carga_compromiso"),
        path("compromiso", views.dashboard_compromiso_general, name="compromiso_dash"),
        
]