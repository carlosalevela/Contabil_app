from django.db import models

class Producto(models.Model):
    """
    Mapea la tabla existente 'producto' en Postgres.
    NO gestiona migraciones (managed=False) para no alterar tu DB.
    """
    id = models.AutoField(primary_key=True)
    empresa_id = models.IntegerField(db_column='empresa_id')
    sku = models.CharField(max_length=64)
    nombre = models.CharField(max_length=150)
    unidad = models.CharField(max_length=10)
    metodo_costo = models.CharField(max_length=20)
    costo_promedio = models.DecimalField(max_digits=12, decimal_places=2)
    precio_detal = models.DecimalField(max_digits=12, decimal_places=2)
    precio_mayor = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    umbral_mayor = models.IntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)  # si la DB ya lo setea, igual no estorba

    class Meta:
        db_table = 'producto'
        managed = False  # importante: no crear/alterar tabla existente
        indexes = [
            models.Index(fields=['empresa_id', 'sku']),
            models.Index(fields=['empresa_id', 'nombre']),
            models.Index(fields=['activo']),
        ]

    def __str__(self):
        return f"{self.sku} - {self.nombre}"
