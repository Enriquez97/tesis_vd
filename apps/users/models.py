from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Municipalidad(models.Model):
    
    #user_empresa =  models.OneToOneField(User,on_delete=models.CASCADE)
    name_municipalidad = models.CharField(max_length=100, blank=True,null=True)
    phone_number_municipalidad = models.CharField(max_length=20, blank=True,null=True)
    picture_municipalidada = models.ImageField(upload_to='media',blank=True,null=True)
    codigo_municipalidad= models.CharField(max_length=15, blank=True,null=True)
    ruc_municipalidad = models.CharField(max_length=12, blank=True,null=True)
    create_municipalidad = models.DateTimeField(auto_now_add=True,null=True)
    modified_municipalidad = models.DateTimeField(auto_now=True,null=True)
    
    
    def __str__(self):

        return self.name_municipalidad 
    
class Cargo(models.Model):
    
    
    name_cargo= models.CharField(max_length=100, blank=True,null=True)
    create_cargo = models.DateTimeField(auto_now_add=True,null=True)
    modified_cargo = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):

        return self.name_cargo
    
class Profile(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user =  models.OneToOneField(User,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='media',blank=True,null=True)
    phone = models.CharField(max_length=20, blank=True,null=True)
    municipalidad=models.ForeignKey(Municipalidad,on_delete=models.CASCADE)
    cargo=models.ForeignKey(Cargo,on_delete=models.CASCADE,null=True)
    create = models.DateTimeField(auto_now_add=True,null=True)
    modified = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):

        return self.username