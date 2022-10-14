import django_filters
import googlemaps
import h3
from django.conf import settings
from django_filters import rest_framework as filters
from users.models import JobseekerProfile
from utils.models import h3_resolutions

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

class JobseekerFilters(filters.FilterSet):
    prof = django_filters.CharFilter(lookup_expr='exact', field_name='profession')
    rating = django_filters.NumberFilter(lookup_expr='gte', field_name='avg_rating')
    zone = django_filters.CharFilter(method='zone_filter')

    def zone_filter(self, queryset, zone, value):
        # print(dir(self))
        # print(self.data)

        query_data = dict(self.data)
        location = query_data['location'][0]
        geocode_result = gmaps.geocode(location)

        location_lat = geocode_result[0]['geometry']['location']['lat']
        location_lng = geocode_result[0]['geometry']['location']['lng']

        try:
            h3_zone = h3.geo_to_h3(
                location_lat, location_lng, h3_resolutions[value]
            )

            # Construct the full lookup expression.
            lookup = '_'.join(['zone_metadata__zone', value])
            return queryset.filter(**{lookup: h3_zone,})

        except:
            print('Query Failed')
            return queryset
    
    
    class Meta:
        model = JobseekerProfile
        fields = ['prof', 'rating',]
