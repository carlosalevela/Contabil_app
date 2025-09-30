from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from Almacen.models import Almacen

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class PublicAlmacenesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Opción A: todos los almacenes de la empresa 1
        qs = Almacen.objects.filter(empresa_id=1).values("id", "nombre")
        # Opción B: solo 3 específicos -> qs = Almacen.objects.filter(id__in=[1,2,3]).values(...)
        return Response(list(qs))
