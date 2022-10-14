from django.contrib import admin

from .models import Company, Employee, JobApplication, JobCard

admin.site.register(JobApplication)
admin.site.register(JobCard)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'website_url',)
  search_fields = ('name',)
  list_display_links = ('id', 'name', )
  list_per_page = 25


@admin.register(Employee)
class CompanyEmployeeAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'role', 'company', )
  search_fields = ('role',)
  list_display_links = ('user', )
  list_per_page = 25
