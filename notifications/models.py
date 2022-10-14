from datetime import datetime

import timeago
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from establishments.models import JobApplication
from pyexpat import model
from rest_framework import serializers

# https://github.com/encode/django-rest-framework/discussions/7850

class NotificationTagChoices(models.TextChoices):
    NEW_CHAT_MESSAGE = "new_chat_message", "new_chat_message"
    NEW_JOB_APPLICATION = "new_job_application", "new_job_application"
    NEW_JOB_OFFER = "new_job_offer", "new_job_offer"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='notifications',
        on_delete=models.CASCADE
    )

    message = models.TextField()
    mark_as_read = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(
        choices=NotificationTagChoices.choices, 
        null=False, blank=False,
        max_length=64
    )

    job_application = models.OneToOneField(
        JobApplication,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return f'{self.message}'

    @property
    def time_since(self):
        now = datetime.now()
        time_ago = timeago.format(self.created_on.replace(tzinfo=None), now)
        return str(time_ago)

    class Meta:
        ordering = ['-id']
        verbose_name = "User Notification"
        verbose_name_plural = "User Notifications"


class EmailNotificationSubscription(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='email_notification_subscriptions',
        on_delete=models.CASCADE
    )

    # Email user when
    new_job_application = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} email notifications settings.'

    class Meta:
        ordering = ['-id']
        verbose_name = "Email Notification Subscription"
        verbose_name_plural = "Email Notification Subscriptions"





# # Signals
# def send_user_notification(sender, instance, created, **kwargs):
#     # allocate task to celery
#     if created:
#         ser = NotificationSerializer(instance)
#         return broadcast_notification_to_user.delay(ser.data)

# post_save.connect(send_user_notification, sender=Notification)
