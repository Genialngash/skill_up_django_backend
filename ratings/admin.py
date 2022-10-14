from django.contrib import admin

from .models import CompanyRating, JobseekerRating

admin.site.register(JobseekerRating)
admin.site.register(CompanyRating)
