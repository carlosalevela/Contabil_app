# Almacen/serializers.py
from rest_framework import serializers
from .models import Almacen as AlmacenModel

class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlmacenModel
        fields = "__all__"
        read_only_fields = ()  # ya no bloqueamos empresa

    def create(self, validated_data):
        user = self.context["request"].user
        # Si NO viene empresa en el body, usa la del usuario
        if "empresa_id" not in validated_data and "empresa" not in validated_data:
            if not getattr(user, "empresa_id", None):
                raise serializers.ValidationError("Debes enviar 'empresa' o asignar empresa al usuario.")
            validated_data["empresa_id"] = user.empresa_id
        # (Opcional) si quieres restringir que solo superuser pueda crear para otra empresa:
        if ("empresa" in validated_data or "empresa_id" in validated_data) and not user.is_superuser:
            # si el usuario no es superuser, forzamos su empresa
            validated_data["empresa_id"] = user.empresa_id
        return super().create(validated_data)
    # en Almacen/serializers.py
    def validate(self, data):
        req = self.context["request"]
        empresa_id = data.get("empresa_id") or getattr(req.user, "empresa_id", None)
        nombre = data.get("nombre") or getattr(self.instance, "nombre", None)
        if nombre and empresa_id:
            from .models import Almacen as M
            qs = M.objects.filter(empresa_id=empresa_id, nombre__iexact=nombre)
            if self.instance: qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({"nombre": "Ya existe un almacén con ese nombre en tu empresa."})
        return data

