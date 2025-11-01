from django.contrib import admin
from .models import Almacen

@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'empresa', 'ubicacion']
    list_filter = ['empresa']
    search_fields = ['nombre', 'ubicacion']