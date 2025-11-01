from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Compras
from .serializers import ComprasSerializer
from .filters import ComprasFilter

class ComprasViewSet(ModelViewSet):
    queryset = Compras.objects.all()
    serializer_class = ComprasSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ComprasFilter
    search_fields = ["proveedor_nombre", "proveedor_nit"]
    ordering_fields = ["fecha", "total", "creado_en", "id"]
    ordering = ["-fecha", "-id"]

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.estado != Compra.Estado.BORRADOR:
            return Response(
                {"detail": "Solo se puede eliminar una compra en BORRADOR."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def confirmar(self, request, pk=None):
        obj = self.get_object()
        if obj.estado != Compra.Estado.BORRADOR:
            return Response({"detail": "Solo se puede confirmar desde BORRADOR."},
                            status=status.HTTP_400_BAD_REQUEST)
        obj.estado = Compra.Estado.CONFIRMADA
        obj.save(update_fields=["estado"])
        return Response(self.get_serializer(obj).data)

    @action(detail=True, methods=["post"])
    def anular(self, request, pk=None):
        obj = self.get_object()
        if obj.estado not in [Compra.Estado.BORRADOR, Compra.Estado.CONFIRMADA]:
            return Response({"detail": "Transición inválida."},
                            status=status.HTTP_400_BAD_REQUEST)
        obj.estado = Compra.Estado.ANULADA
        obj.save(update_fields=["estado"])
        return Response(self.get_serializer(obj).data)
