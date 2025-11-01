# compras/admin.py
from django.contrib import admin, messages
from .models import Compras

@admin.register(Compras)
class ComprasAdmin(admin.ModelAdmin):
    list_display = ("id","fecha","empresa_id","proveedor_nombre","estado","total")
    search_fields = ("proveedor_nombre","proveedor_nit","id")
    list_filter  = ("estado","empresa_id","almacen_id","fecha")
    date_hierarchy = "fecha"
    ordering = ("-fecha","-id")
    readonly_fields = ("creado_en","creado_por")

    @admin.action(description="Confirmar compras seleccionadas")
    def confirmar(self, request, queryset):
        count = 0
        for c in queryset:
            if c.estado == "BORRADOR":
                c.estado = "CONFIRMADA"
                c.save(update_fields=["estado"])
                count += 1
        messages.success(request, f"{count} compra(s) confirmada(s).")

    @admin.action(description="Anular compras seleccionadas")
    def anular(self, request, queryset):
        updated = queryset.exclude(estado="ANULADA").update(estado="ANULADA")
        messages.warning(request, f"{updated} compra(s) anulada(s).")

    actions = ["confirmar", "anular"]
