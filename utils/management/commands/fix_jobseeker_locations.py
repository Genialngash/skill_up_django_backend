import googlemaps
import h3
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from establishments.models import Company
from faker import Faker
from utils.models import JobseekerZoneMetadata, h3_resolutions

from .locations import locations

User = get_user_model()
fake = Faker() 
gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


class Command(BaseCommand):
    help = 'This command updates jobseekers with no locations set'

    def handle(self, *args, **kwargs):
        users = User.objects.filter(u_type='Jobseeker')

        for user in users:
            profile = user.jobseeker_profile
            location_name = profile.location
            print(location_name)

            # Create h3Zones for the Jobseeker
            if location_name and len(location_name) > 0:
                geocode_result = gmaps.geocode(location_name)
                lat = geocode_result[0]['geometry']['location']['lat']
                lng = geocode_result[0]['geometry']['location']['lng']


                JobseekerZoneMetadata.objects.get_or_create(
                    profile=profile,
                    zone_one=h3.geo_to_h3(lat, lng, h3_resolutions['one']),
                    zone_two=h3.geo_to_h3(lat, lng, h3_resolutions['two']),
                    zone_three=h3.geo_to_h3(lat, lng, h3_resolutions['three']),
                    zone_four=h3.geo_to_h3(lat, lng, h3_resolutions['four']),
                    zone_five=h3.geo_to_h3(lat, lng, h3_resolutions['five']),
                    zone_six=h3.geo_to_h3(lat, lng, h3_resolutions['six']),
                    zone_seven=h3.geo_to_h3(lat, lng, h3_resolutions['seven']),
                )
