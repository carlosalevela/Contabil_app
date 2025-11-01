from rest_framework import serializers
from .models import Producto
from decimal import Decimal

UNIDADES_PERMITIDAS = {"UND", "KG", "LT", "M", "CAJA", "PAQ", "PAR", "MT2", "MT3"}
METODOS_COSTO = {"PROMEDIO", "PEPS", "UEPS", "IDENTIFICADO"}

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        # Omitimos cualquier columna legacy como 'trial106'
        fields = [
            'id', 'empresa_id', 'sku', 'nombre', 'unidad', 'metodo_costo',
            'costo_promedio', 'precio_detal', 'precio_mayor', 'umbral_mayor',
            'activo', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']

    def validate(self, data):
        # Tomar valores actuales + entrantes (para PATCH)
        instance = getattr(self, 'instance', None)

        empresa_id = data.get('empresa_id', getattr(instance, 'empresa_id', None))
        sku = (data.get('sku', getattr(instance, 'sku', '')) or '').strip()
        nombre = (data.get('nombre', getattr(instance, 'nombre', '')) or '').strip()
        unidad = (data.get('unidad', getattr(instance, 'unidad', '')) or '').strip().upper()
        metodo_costo = (data.get('metodo_costo', getattr(instance, 'metodo_costo', '')) or '').strip().upper()

        costo_promedio = data.get('costo_promedio', getattr(instance, 'costo_promedio', None))
        precio_detal = data.get('precio_detal', getattr(instance, 'precio_detal', None))
        precio_mayor = data.get('precio_mayor', getattr(instance, 'precio_mayor', None))
        umbral_mayor = data.get('umbral_mayor', getattr(instance, 'umbral_mayor', None))

        # Requeridos básicos
        if empresa_id is None:
            raise serializers.ValidationError({"empresa_id": "Este campo es requerido."})
        if not sku:
            raise serializers.ValidationError({"sku": "Este campo es requerido."})
        if not nombre:
            raise serializers.ValidationError({"nombre": "Este campo es requerido."})
        if not unidad:
            raise serializers.ValidationError({"unidad": "Este campo es requerido."})
        if not metodo_costo:
            raise serializers.ValidationError({"metodo_costo": "Este campo es requerido."})
        if costo_promedio is None:
            raise serializers.ValidationError({"costo_promedio": "Este campo es requerido."})
        if precio_detal is None:
            raise serializers.ValidationError({"precio_detal": "Este campo es requerido."})

        # Catálogos
        if unidad not in UNIDADES_PERMITIDAS:
            raise serializers.ValidationError({"unidad": f"Unidad no válida. Permitidas: {sorted(UNIDADES_PERMITIDAS)}"})
        if metodo_costo not in METODOS_COSTO:
            raise serializers.ValidationError({"metodo_costo": f"Método no válido. Permitidos: {sorted(METODOS_COSTO)}"})

        # Tipos/negocios
        if Decimal(costo_promedio) < 0:
            raise serializers.ValidationError({"costo_promedio": "No puede ser negativo."})
        if Decimal(precio_detal) < Decimal(costo_promedio):
            raise serializers.ValidationError({"precio_detal": "Debe ser mayor o igual al costo_promedio."})

        if precio_mayor is not None:
            if Decimal(precio_mayor) < Decimal(costo_promedio):
                raise serializers.ValidationError({"precio_mayor": "Debe ser mayor o igual al costo_promedio."})
            if Decimal(precio_mayor) > Decimal(precio_detal):
                raise serializers.ValidationError({"precio_mayor": "Debe ser menor o igual al precio_detal."})
            if umbral_mayor is None or int(umbral_mayor) < 1:
                raise serializers.ValidationError({"umbral_mayor": "Requerido y >= 1 cuando se define precio_mayor."})

        # Unicidad (empresa_id, sku) a nivel de app (DB puede no tener constraint)
        qs = Producto.objects.filter(empresa_id=empresa_id, sku__iexact=sku)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError({"sku": "Este SKU ya existe para la empresa."})

        # Normalizaciones
        data['sku'] = sku
        data['nombre'] = nombre
        data['unidad'] = unidad
        data['metodo_costo'] = metodo_costo
        return data
