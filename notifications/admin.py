from django.contrib import admin

from .models import EmailNotificationSubscription, Notification

# admin.site.register(JobApplicationNotificationMetadata)

class NotificationAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'created_on',)
  list_display_links = ('user',)
  list_per_page = 25

admin.site.register(Notification, NotificationAdmin)


class EmailNotificationSubscriptionAdmin(admin.ModelAdmin):
  list_display = ('id', 'user',)
  list_display_links = ('user',)
  list_per_page = 25

admin.site.register(EmailNotificationSubscription, EmailNotificationSubscriptionAdmin)
