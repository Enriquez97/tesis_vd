from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('login',views.login_view, name='login'),
    path('logout',views.logout_view, name='logout'),
    #path('profile/',views.update_profile, name='update_profile'),
]