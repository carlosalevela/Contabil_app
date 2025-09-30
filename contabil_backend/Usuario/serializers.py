from rest_framework import serializers
from django.contrib.auth import get_user_model
from Almacen.models import Almacen

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    almacen = serializers.PrimaryKeyRelatedField(
        queryset=Almacen.objects.all(), write_only=True, required=True
    )

    class Meta:
        model = User
        fields = ("email","username","password","first_name","last_name","telefono","empresa","rol")

    def validate(self, data):
        almac = data["almacen"]
        # La empresa es la #1 (ajusta si cambias)
        if almac.empresa_id != 1:
            raise serializers.ValidationError({"almacen": "El almacén no pertenece a la empresa."})
        return data

    def create(self, validated_data):
        validated_data.pop("almacen", None)  # no tenemos campo en User, solo validamos
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data.get("first_name",""),
            last_name=validated_data.get("last_name",""),
            telefono=validated_data.get("telefono"),
            empresa_id=1,            # fija la empresa 1
            is_staff=False,
            is_superuser=False,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","email","username","first_name","last_name","telefono","empresa","rol","is_active")
