from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_field,
    extend_schema_serializer,
)
from rest_framework import serializers

from .models import EmailNotificationSubscription, Notification


@extend_schema_serializer(
    examples = [
         OpenApiExample(
            'List all notifications',
            description=
                """This is the response you get for listing notifications successfully.""",
            value={
                "data": {
                    "current_page": 1,
                    "previous_page": None,
                    "next_page": None,
                    "count": 1,
                    "results": [
                        {
                            "id": 0,
                            "message": "string",
                            "job_application": 0,
                            "time_since": "string",
                            "mark_as_read": True
                        }
                    ]
                },
                "message": "Success.",
                "status": "ok",
                "status_code": 200
            },
            request_only=False,
            response_only=True,
        ),
    ],
)
class NotificationSerializer(serializers.ModelSerializer):
    time_since = serializers.SerializerMethodField('get_time_since')

    @extend_schema_field(OpenApiTypes.STR)
    def get_time_since(self, card):
        return str(card.time_since)

    class Meta:
        model = Notification
        fields = ['id', 'message', 'job_application', 'time_since', 'mark_as_read']


@extend_schema_serializer(
    examples = [
         OpenApiExample(
            'Mark all notifications as read',
            description=
                """This is the response you get after marking all notifications as read successfully.""",
            value={
                "message": "Successfully updated notifications read status.",
                "status": "ok",
                "status_code": 200
            },
            request_only=False,
            response_only=True,
        ),
    ],
)
class MarkAllNotificationAsReadSerializer(serializers.Serializer):
    mark_all_as_read = serializers.BooleanField(required=True, allow_null=False)


@extend_schema_serializer(
    examples = [
         OpenApiExample(
            'Mark single notification as read',
            description=
                """This is the response you get after marking a single notification as read successfully.""",
            value={
                "message": "Successfully updated the notification read status.",
                "status": "ok",
                "status_code": 200
            },
            request_only=False,
            response_only=True,
        ),
    ],
)
class MarkNotificationAsReadSerializer(serializers.Serializer):
    mark_as_read = serializers.BooleanField(required=True, allow_null=False)


class EmailNotificationSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotificationSubscription
        fields = ['new_job_application']
