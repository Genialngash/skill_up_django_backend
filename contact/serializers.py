from email.policy import default

from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers


class CHANNEL_CHOICES(models.TextChoices):
    SMS = "sms", "sms"
    CALL = "call", "call"


# Get Code
class ContactVerificationCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    channel = serializers.ChoiceField(
        choices=CHANNEL_CHOICES,  
        required=True,
    )

class GetVerificationCodeSuccessResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    status_code = serializers.IntegerField()


class GetVerificationCodeErrorResponseSerializer(serializers.Serializer):
    error_code = serializers.CharField()
    status = serializers.CharField()
    status_code = serializers.IntegerField()
    phone_number = serializers.CharField()
    channel = serializers.CharField()
    payload = serializers.CharField()
    method = serializers.CharField()
    authentication = serializers.CharField()


# Verification confirm
class ConfirmVerificationSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=6, required=True)


class ConfirmVerificationSuccessResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    status_code = serializers.IntegerField()


class ConfirmVerificationErrorResponseSerializer(serializers.Serializer):
    error_code = serializers.CharField()
    status = serializers.CharField()
    status_code = serializers.IntegerField()
    verification_code = serializers.CharField()
    payload = serializers.CharField()
    method = serializers.CharField()
    authentication = serializers.CharField()
