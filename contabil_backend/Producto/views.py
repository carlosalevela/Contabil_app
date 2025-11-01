from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Producto
from .serializers import ProductoSerializer


class ProductoPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductoListCreateAPI(generics.ListCreateAPIView):
    queryset = Producto.objects.all().order_by('-id')
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProductoPagination

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Filtrar por empresa del usuario (seguridad)
        if hasattr(self.request.user, 'empresa_id'):
            qs = qs.filter(empresa_id=self.request.user.empresa_id)
        
        # Filtros desde query params
        empresa_id = self.request.query_params.get('empresa_id')
        buscar = self.request.query_params.get('buscar')
        activo = self.request.query_params.get('activo')
        unidad = self.request.query_params.get('unidad')
        metodo_costo = self.request.query_params.get('metodo_costo')

        if empresa_id:
            qs = qs.filter(empresa_id=empresa_id)
        
        if buscar:
            qs = qs.filter(Q(sku__icontains=buscar) | Q(nombre__icontains=buscar))
        
        if activo is not None:
            activo_bool = activo.lower() in ('true', '1', 'yes')
            qs = qs.filter(activo=activo_bool)
        
        if unidad:
            qs = qs.filter(unidad__iexact=unidad)
        
        if metodo_costo:
            qs = qs.filter(metodo_costo__iexact=metodo_costo)

        # Validar ordering
        ordering = self.request.query_params.get('ordering')
        if ordering:
            allowed_fields = ['id', '-id', 'sku', '-sku', 'nombre', '-nombre', 
                            'precio_detal', '-precio_detal', 'creado_en', '-creado_en']
            if ordering in allowed_fields:
                qs = qs.order_by(ordering)
        
        return qs

    def perform_create(self, serializer):
        # Asociar automáticamente la empresa del usuario
        if hasattr(self.request.user, 'empresa_id'):
            serializer.save(empresa_id=self.request.user.empresa_id)
        else:
            serializer.save()


class ProductoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        # Filtrar por empresa del usuario (seguridad)
        if hasattr(self.request.user, 'empresa_id'):
            qs = qs.filter(empresa_id=self.request.user.empresa_id)
        return qs

    def delete(self, request, *args, **kwargs):
        """Soft delete: inactivar en lugar de eliminar"""
        try:
            instance = self.get_object()
            instance.activo = False
            instance.save(update_fields=['activo'])
            return Response(
                {"message": "Producto inactivado correctamente"},
                status=status.HTTP_200_OK
            )
        except Producto.DoesNotExist:
            raise NotFound("Producto no encontrado.")