from django.urls import path
from django_api import settings
from .views import geojson_view, RegisterView, LoginView, MeView, MeUpdateView, ChangePasswordView, ReportIssueView, TermsView, PrivacyPolicyView, DocumentationListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
    path('me/update/', MeUpdateView.as_view(), name='me-update'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('report/', ReportIssueView.as_view(), name='report-issue'),
    path('terms/', TermsView.as_view()),
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('documentation/', DocumentationListView.as_view(), name='documentation-list'),
    path('geojson/', geojson_view, name='geojson_view'),  # Assurez-vous que cette route existe
]

from django.conf.urls.static import static
# Permet de servir les fichiers médias pendant le développement
if settings.DEBUG:  # N'oubliez pas d'ajouter cette condition
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # ✅ Pour servir les fichiers