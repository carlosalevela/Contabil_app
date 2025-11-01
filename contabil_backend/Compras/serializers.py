from rest_framework import serializers
from django.utils import timezone
from .models import Compras
import datetime as _dt

class ComprasSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    creado_por = serializers.IntegerField(read_only=True)
    creado_en = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Compras
        fields = (
            "id","empresa_id","proveedor_nombre","proveedor_nit","fecha",
            "almacen_id","estado","total","creado_por","creado_en","trial102"
        )

    def validate_total(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError("El total debe ser >= 0.")
        return value

    def validate_fecha(self, value):
        # Si no quieres validar fecha futura, elimina esto
        if value > _dt.date.today():
            raise serializers.ValidationError("La fecha no puede ser futura.")
        return value

    def update(self, instance, validated_data):
        # Bloquea edición si no está en BORRADOR
        if instance.estado != Compra.Estado.BORRADOR:
            raise serializers.ValidationError("Solo se puede editar cuando la compra está en BORRADOR.")
        # No permitimos cambiar estado vía PATCH normal
        validated_data.pop("estado", None)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        # Forzamos estado inicial y seteamos creador/fecha creación
        validated_data["estado"] = Compra.Estado.BORRADOR
        user = self.context.get("request").user if self.context.get("request") else None
        validated_data["creado_por"] = getattr(user, "id", 0) or 0
        validated_data["creado_en"] = timezone.now()
        return Compra.objects.create(**validated_data)
