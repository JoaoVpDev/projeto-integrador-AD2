from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Item

admin.site.register(Item)

try:
    admin_group, created = Group.objects.get_or_create(name="Administradores")
    visualizador_group, created = Group.objects.get_or_create(name="Visualizadores")
except:
    pass
