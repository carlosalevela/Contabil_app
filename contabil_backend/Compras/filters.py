import django_filters as df
from .models import Compras

class ComprasFilter(df.FilterSet):
    fecha_desde = df.DateFilter(field_name="fecha", lookup_expr="gte")
    fecha_hasta = df.DateFilter(field_name="fecha", lookup_expr="lte")

    class Meta:
        model = Compras
        fields = ["empresa_id", "almacen_id", "proveedor_nit", "estado"]
