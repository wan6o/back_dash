from rest_framework import serializers
from .models import Chambre, ChambreDetail, TeteDeCable, ChambreTirageDetail

class ChambreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chambre
        fields = '__all__'

class ChambreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChambreDetail
        fields = '__all__'

class TeteDeCableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeteDeCable
        fields = '__all__'

class ChambreTirageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChambreTirageDetail
        fields = '__all__'
