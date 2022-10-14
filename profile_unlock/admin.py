from django.contrib import admin

from .models import UnlockedProfile, UserAccessCredit


class UserAccessCreditAdmin(admin.ModelAdmin):
  list_display = ('id', 'email', 'unlock_code', 'is_valid', 'expires_on')
  list_display_links = ('email', 'unlock_code')
  list_per_page = 25

admin.site.register(UserAccessCredit, UserAccessCreditAdmin)

admin.site.register(UnlockedProfile)
