from django.urls import path

from .views import (
    EmailNotificationSubscriptionView,
    MarkAllNotificationsAsReadView,
    NotificationViewSet,
)

notifications_list = NotificationViewSet.as_view({'get': 'list'})

urlpatterns = [
    path(
        'mark-all/',
        MarkAllNotificationsAsReadView.as_view(),
        name='mark_all_notifications_as_read'
    ),
    path(r'list/', notifications_list, name='user_notifications_list'),
    path(
        'email/subscription/',
        EmailNotificationSubscriptionView.as_view(),
        name='email_notifications_update'
    ),
]

#https://stackoverflow.com/questions/45205446/when-to-map-http-methods-to-view-methods-django-rest-framework
