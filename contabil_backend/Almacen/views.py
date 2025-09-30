from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Almacen as AlmacenModel
from .serializers import AlmacenSerializer
from .permissions import IsAdminOrReadOnly

class AlmacenViewSet(viewsets.ModelViewSet):
    serializer_class = AlmacenSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "ubicacion"]
    ordering_fields = ["id", "nombre"]
    ordering = ["id"]

    queryset = AlmacenModel.objects.all()

    # Permisos: autenticado para leer, admin para escribir
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        # Admin ve todo; otros solo su empresa
        return qs if u.is_superuser else qs.filter(empresa_id=u.empresa_id)
