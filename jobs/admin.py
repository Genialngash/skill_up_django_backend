from django.contrib import admin

from . import models


class JobBookmarkAdmin(admin.ModelAdmin):
  list_display = ('id', 'user',)
  list_display_links = ('id', 'user')
  list_per_page = 25

admin.site.register(models.JobBookmark, JobBookmarkAdmin)
