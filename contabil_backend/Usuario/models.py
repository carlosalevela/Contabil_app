# Usuario/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Empresa(models.Model):
    id = models.BigAutoField(primary_key=True)
    class Meta:
        db_table = "empresa"
        managed = False  # la tabla ya existe en tu PostgreSQL

class Rol(models.Model):
    id = models.BigAutoField(primary_key=True)
    class Meta:
        db_table = "rol"
        managed = False  # la tabla ya existe en tu PostgreSQL

class User(AbstractUser):
    # username existe, pero usaremos email para login
    email = models.EmailField(unique=True)

    empresa = models.ForeignKey(
        Empresa, null=True, blank=True, on_delete=models.SET_NULL, related_name="users"
    )
    rol = models.ForeignKey(
        Rol, null=True, blank=True, on_delete=models.SET_NULL, related_name="users"
    )
    telefono = models.CharField(max_length=20, null=True, blank=True)

    USERNAME_FIELD = "email"          # login por email
    REQUIRED_FIELDS = ["username"]    # sigue pidiendo username al crear superuser

    def __str__(self):
        return self.email
