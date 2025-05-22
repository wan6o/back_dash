from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChambreViewSet, ChambreDetailViewSet, TeteDeCableViewSet, ChambreTirageDetailViewSet

router = DefaultRouter()
router.register(r'chambres', ChambreViewSet)
router.register(r'chambre-details', ChambreDetailViewSet)
router.register(r'tetes-de-cable', TeteDeCableViewSet)
router.register(r'chambre-tirage-details', ChambreTirageDetailViewSet)  # ajout ici

urlpatterns = [
    path('', include(router.urls)),
]
