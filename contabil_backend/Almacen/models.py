from django.db import models
from Usuario.models import Empresa  # Empresa unmanaged en tu app Usuario

class Almacen(models.Model):
    id = models.BigAutoField(primary_key=True)
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        db_column="empresa_id",
        related_name="almacenes",
    )
    nombre = models.CharField(max_length=80)
    ubicacion = models.CharField(max_length=120, null=True, blank=True)
    trial102 = models.BooleanField(null=True, blank=True, db_column="trial102")

    class Meta:
        db_table = "almacen"
        managed = False  # ¡importante! la tabla ya existe en PostgreSQL

    def __str__(self):
        return self.nombre
