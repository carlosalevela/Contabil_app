# compras/models.py
from django.db import models

class Compras(models.Model):
    class Estado(models.TextChoices):
        BORRADOR   = "BORRADOR", "Borrador"
        CONFIRMADA = "CONFIRMADA", "Confirmada"
        ANULADA    = "ANULADA", "Anulada"

    id               = models.BigAutoField(primary_key=True)  # PK existente
    empresa_id       = models.IntegerField()
    proveedor_nombre = models.CharField(max_length=150)
    proveedor_nit    = models.CharField(max_length=50)
    fecha            = models.DateField()
    almacen_id       = models.IntegerField()
    estado           = models.CharField(max_length=12, choices=Estado.choices, default=Estado.BORRADOR)
    total            = models.DecimalField(max_digits=14, decimal_places=2)
    creado_por       = models.IntegerField()
    creado_en        = models.DateTimeField()
    trial102         = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table  = "compra"   # usa la tabla existente
        managed   = False      # Django NO intentará crear/alterar esta tabla
        ordering  = ["-fecha", "-id"]

    def __str__(self):
        return f"Compras #{self.id} - {self.proveedor_nombre} ({self.fecha})"
