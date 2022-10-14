import django_filters
import googlemaps
import h3
from django.conf import settings
from django_filters import rest_framework as filters
from establishments.models import JobApplication, JobCard
from utils.models import h3_resolutions

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


class JobCardFilter(filters.FilterSet):
    pub = django_filters.CharFilter(lookup_expr='exact', field_name='is_published')
    taken = django_filters.CharFilter(lookup_expr='exact', field_name='taken')
    co = django_filters.CharFilter(lookup_expr='exact', field_name='company')
    # location = django_filters.CharFilter(lookup_expr='icontains', field_name='location')
    contract = django_filters.CharFilter(lookup_expr='exact', field_name='contract_type')
    zone = django_filters.CharFilter(method='zone_filter')
    cat = django_filters.CharFilter(lookup_expr='icontains', field_name='category')


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
        model = JobCard
        fields = ['pub', 'taken', 'contract', 'cat']


class JobApplicationsFilter(filters.FilterSet):
    co = django_filters.CharFilter(lookup_expr='exact', field_name='job_card__company')
    job_card = django_filters.CharFilter(lookup_expr='exact', field_name='job_card')
    # taken = django_filters.CharFilter(lookup_expr='exact', field_name='card__taken')
    # contract = django_filters.CharFilter(lookup_expr='icontains', field_name='card__contract_type')

    class Meta:
        model = JobApplication
        fields = ['job_card', 'co',]


class JobApplicantFilter(filters.FilterSet):
    co = django_filters.CharFilter(lookup_expr='exact', field_name='job_card__company')
    job_card = django_filters.CharFilter(lookup_expr='exact', field_name='job_card')
    user = django_filters.CharFilter(lookup_expr='exact', field_name='job_card__user')
    # taken = django_filters.CharFilter(lookup_expr='exact', field_name='card__taken')
    # contract = django_filters.CharFilter(lookup_expr='icontains', field_name='card__contract_type')


    class Meta:
        model = JobApplication
        fields = ['job_card', 'co',]
