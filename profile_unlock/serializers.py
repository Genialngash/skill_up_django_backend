from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import JobseekerProfile

from .models import UnlockedProfile, UserAccessCredit

User = get_user_model()


class UnlockProfileSerializer(serializers.Serializer):
    unlock_code = serializers.CharField(required=True, allow_null=False)
    jobseeker = serializers.IntegerField(required=True, allow_null=False)


class UserAccessCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccessCredit
        fields = (
            'id', 'unlock_code', 'total_unlocks', 
            'job_cards', 'is_valid', 'expires_on',
        )


class UnlockedUserGeneralDataSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 
            'avatar', 'email', 'phone_number',
            'contact_is_verified'
        )

class UnlockedUserProfileSerializer(serializers.ModelSerializer):
    user = UnlockedUserGeneralDataSlimSerializer(read_only=True)
    class Meta:
        model = JobseekerProfile
        fields = (
            'user', 'profession', 'hourly_rate',
            'avg_rating', 'total_ratings'
        )


class UnlockedProfileSerializer(serializers.ModelSerializer):
    profile = UnlockedUserProfileSerializer(read_only=True)

    class Meta:
        model = UnlockedProfile
        fields = (
            'id', 'profile', 'created_on'
        )
