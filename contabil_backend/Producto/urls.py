from django.urls import path
from .views import ProductoListCreateAPI, ProductoDetailAPI

urlpatterns = [
    path('productos/', ProductoListCreateAPI.as_view(), name='producto-list-create'),
    path('productos/<int:pk>/', ProductoDetailAPI.as_view(), name='producto-detail'),
]
