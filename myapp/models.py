from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# -------------------------------
# Upload path
# -------------------------------
def upload_to(instance, filename):
    return f'badges/{filename}'

# -------------------------------
# Custom User Manager
# -------------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email.split('@')[0])
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# -------------------------------
# Custom User Model
# -------------------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=191)
    phone = models.CharField(max_length=20)
    badge = models.FileField(upload_to=upload_to, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

User = get_user_model()

# -------------------------------
# Report Model
# -------------------------------
class Report(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.user.email if self.user else 'Anonymous'}"

# -------------------------------
# Terms and Privacy
# -------------------------------
class TermsAndConditions(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

class PrivacyPolicy(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

# -------------------------------
# Documentation
# -------------------------------
class Documentation(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='documentation_images/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# -------------------------------
# Intervention Model
# -------------------------------
class Intervention(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title

# -------------------------------
# Notification Model
# -------------------------------
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.email}"

# -------------------------------
# Chambre Model (nouveau)vs
# -------------------------------
class Chambre(models.Model):
    TYPE_CHOICES = [
        ('soudure', 'Chambre de soudure'),
        ('tirage', 'Chambre de tirage'),
    ]

    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_ajout = models.DateTimeField(auto_now_add=True)

    intervention = models.ForeignKey(
        Intervention, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='chambres'
    )

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"

class ChambreDetail(models.Model):
    chambre = models.ForeignKey('Chambre', on_delete=models.CASCADE, related_name='details')
    nb_cables_entree = models.IntegerField()
    nb_cables_sortie = models.IntegerField()
    type_boitier = models.CharField(max_length=100)
    commentaire = models.TextField(blank=True)
    photo = models.ImageField(upload_to='chambre_photos/', blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Détail de {self.chambre.nom}"


class TeteDeCable(models.Model):
    site_name = models.CharField(max_length=100)  # ou un FK si les sites sont modélisés
    type_odf = models.CharField(max_length=100)
    nb_ports = models.IntegerField()
    ports_utilises = models.CharField(max_length=100)
    depart = models.CharField(max_length=100)
    arrivee = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='tetes_cable_photos/', blank=True, null=True)
    description = models.TextField(blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tête de câble {self.site_name} ({self.nb_ports} ports)"
    
class ChambreTirageDetail(models.Model):
    chambre = models.ForeignKey('Chambre', on_delete=models.CASCADE, related_name='tirage_details')
    nb_conduits = models.IntegerField()
    commentaire = models.TextField(blank=True)
    photo = models.ImageField(upload_to='chambre_tirage_photos/', blank=True, null=True)  # bien défini ici
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Détail tirage de {self.chambre.nom}"

