from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'empresa_id', 'sku', 'nombre', 'unidad', 'metodo_costo', 'precio_detal', 'activo', 'creado_en')
    list_filter = ('empresa_id', 'unidad', 'metodo_costo', 'activo')
    search_fields = ('sku', 'nombre')
