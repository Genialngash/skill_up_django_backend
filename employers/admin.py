from django.contrib import admin

from .models import JobOffer


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
  list_display = ('id', 'applicant', 'created_on_timestamp',)
  search_fields = ('applicant',)
  list_display_links = ('id', 'applicant', )
  list_per_page = 25
