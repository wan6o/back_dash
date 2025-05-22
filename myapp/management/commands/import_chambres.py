import json
from django.core.management.base import BaseCommand
from myapp.models import Chambre

class Command(BaseCommand):
    help = "Importe les chambres depuis un fichier GeoJSON"

    def handle(self, *args, **kwargs):
        filepath = 'myapp/media/geojson/doc.geojson'
        with open(filepath, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)

        count = 0
        for feature in geojson_data.get('features', []):
            props = feature.get('properties', {})
            geometry = feature.get('geometry', {})
            name = props.get('name', '').strip()
            coords = geometry.get('coordinates', [])

            if not name or not coords or geometry.get('type') != 'Point':
                continue

            type_val = 'soudure' if 'soudure' in name.lower() or name.lower().startswith('ch') else 'tirage'
            longitude, latitude = coords[:2]  # ✅ ici

            chambre, created = Chambre.objects.get_or_create(
                nom=name,
                defaults={'latitude': latitude, 'longitude': longitude, 'type': type_val}
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} chambres importées avec succès.'))
