from django.contrib import admin
from .models import Profile, Cargo, Municipalidad
# Register your models here.
admin.site.register(Profile)
admin.site.register(Cargo)
admin.site.register(Municipalidad)