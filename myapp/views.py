import os
from django.http import FileResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.http import FileResponse
import os
from django_api import settings
from .models import Documentation, PrivacyPolicy, TermsAndConditions
from .serializers import (
    DocumentationSerializer,
    PrivacyPolicySerializer,
    RegisterSerializer,
    TermsSerializer,
    UserProfileSerializer,
    ReportSerializer,
)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        data = request.data.copy()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        data['name'] = f"{first_name} {last_name}"

        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message': 'Inscription réussie', 'token': token.key}, status=201)
        else:
            print("ERREUR D'INSCRIPTION ❌", serializer.errors)
            return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Connexion réussie',
                'token': token.key,
                'user': UserProfileSerializer(user, context={'request': request}).data
            })
        return Response({'error': 'Email ou mot de passe incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)


class MeUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not check_password(current_password, user.password):
            return Response({'error': 'Mot de passe actuel incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Mot de passe mis à jour avec succès.'})


class ReportIssueView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Signalement enregistré ✅'}, status=201)
        return Response(serializer.errors, status=400)
    
class TermsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        terms = TermsAndConditions.objects.last()
        serializer = TermsSerializer(terms)
        return Response(serializer.data)

class PrivacyPolicyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        policy = PrivacyPolicy.objects.last()
        if policy:
            serializer = PrivacyPolicySerializer(policy)
            return Response(serializer.data)
        return Response({'error': 'Aucune politique trouvée.'}, status=404)

from rest_framework.permissions import IsAuthenticated

class DocumentationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        docs = Documentation.objects.all()
        serializer = DocumentationSerializer(docs, many=True, context={"request": request})
        return Response(serializer.data)
    
def geojson_view(request):
    # Chemin du fichier GeoJSON dans le répertoire des médias
    filepath = os.path.join(settings.MEDIA_ROOT, 'geojson', 'FO-NDB.geojson')  # Utilisez le chemin relatif pour accéder au fichier GeoJSON
    
    try:
        with open(filepath, 'r') as file:
            data = file.read()  # Lire le contenu du fichier GeoJSON
        return JsonResponse(data, safe=False)  # Renvoie la réponse GeoJSON
    except FileNotFoundError:
        return JsonResponse({"error": "Fichier GeoJSON introuvable."}, status=404)