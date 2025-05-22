from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Chambre, ChambreDetail, TeteDeCable, ChambreTirageDetail
from .serializers import ChambreSerializer, ChambreDetailSerializer, TeteDeCableSerializer, ChambreTirageDetailSerializer


class ChambreViewSet(viewsets.ModelViewSet):
    queryset = Chambre.objects.all()
    serializer_class = ChambreSerializer


class ChambreDetailViewSet(viewsets.ModelViewSet):
    queryset = ChambreDetail.objects.all()
    serializer_class = ChambreDetailSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]


class TeteDeCableViewSet(viewsets.ModelViewSet):
    queryset = TeteDeCable.objects.all()
    serializer_class = TeteDeCableSerializer
    permission_classes = [AllowAny]


class ChambreTirageDetailViewSet(viewsets.ModelViewSet):
    queryset = ChambreTirageDetail.objects.all()
    serializer_class = ChambreTirageDetailSerializer
    permission_classes = [AllowAny]
