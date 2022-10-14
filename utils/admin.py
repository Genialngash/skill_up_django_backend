from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import JobCardZoneMetadata, JobseekerZoneMetadata


class JobCardZoneMetadataAdmin(admin.ModelAdmin):
  list_display = ('id', 'job_card',)
  list_display_links = ('id', 'job_card')
  list_per_page = 25

admin.site.register(JobCardZoneMetadata, JobCardZoneMetadataAdmin)


class JobseekerZoneMetadataAdmin(admin.ModelAdmin):
  list_display = ('id', 'profile',)
  list_display_links = ('id', 'profile')
  list_per_page = 25

admin.site.register(JobseekerZoneMetadata, JobseekerZoneMetadataAdmin)
