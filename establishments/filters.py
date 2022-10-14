import django_filters
from django_filters import rest_framework as filters

from .models import Company


class CompanyListFilter(filters.FilterSet):
    mgr = django_filters.CharFilter(lookup_expr='exact', field_name='hiring_manager')
    class Meta:
        model = Company
        fields = ['mgr',]
