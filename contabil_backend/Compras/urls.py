from rest_framework.routers import DefaultRouter
from .views import ComprasViewSet

router = DefaultRouter()
router.register(r"compras", ComprasViewSet, basename="compras")

urlpatterns = router.urls
