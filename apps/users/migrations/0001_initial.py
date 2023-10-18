# Generated by Django 3.2.15 on 2023-10-07 01:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_cargo', models.CharField(blank=True, max_length=100, null=True)),
                ('create_cargo', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_cargo', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Municipalidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_municipalidad', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number_municipalidad', models.CharField(blank=True, max_length=20, null=True)),
                ('picture_municipalidada', models.ImageField(blank=True, null=True, upload_to='media')),
                ('codigo_municipalidad', models.CharField(blank=True, max_length=15, null=True)),
                ('ruc_municipalidad', models.CharField(blank=True, max_length=12, null=True)),
                ('create_municipalidad', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_municipalidad', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='media')),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('create', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('cargo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.cargo')),
                ('municipalidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.municipalidad')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]