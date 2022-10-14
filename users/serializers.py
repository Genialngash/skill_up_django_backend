from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import (
    JWTSerializer,
    LoginSerializer,
    UserDetailsSerializer,
)
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_field,
    extend_schema_serializer,
)
from jobseekers.serializers import (
    JobseekerCertificationSerializer,
    JobseekerLanguageSerializer,
    WorkExperienceSerializer,
    WorkExperienceSoloSerializer,
)
from profile_unlock.models import UserAccessCredit
from profile_unlock.serializers import UserAccessCreditSerializer
from rest_framework import serializers
from stripe import Source

from .api_schema_examples import employer_examples, jobseeker_examples
from .model_choices import USER_TYPES
from .models import EmployerProfile, JobseekerProfile

User = get_user_model()

class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True, allow_blank=False)
    log_in_as = serializers.ChoiceField(
        choices=['Jobseeker', 'Employer'],
        required=True,
        allow_blank=False
    )

class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom registration serializer that adds on the extra
    user type field
    """
    username = None
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    u_type = serializers.ChoiceField(
        choices = USER_TYPES,
        required = True, 
        error_messages={'required': 'This is a required field.'})


    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'u_type': self.validated_data.get('u_type', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)

        try:
            adapter.clean_password(self.cleaned_data['password1'], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exc)
            )

        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class UserDetailSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 
            'last_name', 'avatar', 
            'gender', 'contact_is_verified'
        )


class CustomUserDetailsSerializer(UserDetailsSerializer):
    """
    Custom user details serializer that adds on the extra
    user type field
    """
    class Meta:
        extra_fields = []
        # We need to check whether the auth model has the attribute or not
        if hasattr(User, 'USERNAME_FIELD'):
            extra_fields.append(User.USERNAME_FIELD)
        if hasattr(User, 'EMAIL_FIELD'):
            extra_fields.append(User.EMAIL_FIELD)
        if hasattr(User, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(User, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(User, 'u_type'):
            extra_fields.append('u_type')
        if hasattr(User, 'avatar'):
            extra_fields.append('avatar')
        if hasattr(User, 'phone_number'):
            extra_fields.append('phone_number')
        if hasattr(User, 'phone_number'):
            extra_fields.append('phone_number')
        if hasattr(User, 'contact_is_verified'):
            extra_fields.append('contact_is_verified')
        if hasattr(User, 'birthday'):
            extra_fields.append('birthday')
        if hasattr(User, 'logged_in_as'):
            extra_fields.append('logged_in_as')
        if hasattr(User, 'gender'):
            extra_fields.append('gender')
        if hasattr(User, 'publish_jobseeker_profile'):
            extra_fields.append('publish_jobseeker_profile')
        if hasattr(User, 'unread_notifications'):
            extra_fields.append('unread_notifications')

        model = User
        fields = ('id', *extra_fields)
        read_only_fields = (
            'email', 'u_type', 
            'phone_number', 'contact_is_verified', 
            'unread_notifications'
        )


class UserUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

# Custom Model Serializers
class UserExtraSlimSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'u_type')

class UserUnlockedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'u_type')

class JobseekerSlimSerializer(serializers.ModelSerializer):
    user = UserExtraSlimSerializer()

    class Meta:
        model = JobseekerProfile
        read_only_fields = (
            'user', 'avg_rating', 'total_ratings')
        fields = [
            'user', 'bio', 'country', 'location', 'avg_rating', \
            'total_ratings', 'profession', 'education_level', 'hourly_rate'
        ]


class JobseekerCompleteDetailSerializer(serializers.ModelSerializer):
    languages = JobseekerLanguageSerializer(many=True,)
    certifications = JobseekerCertificationSerializer(many=True, source='jobseeker_certifications')
    work_experience = WorkExperienceSoloSerializer(many=True, source='jobseeker_experience')
    user = CustomUserDetailsSerializer()
    class Meta:
        model = JobseekerProfile
        read_only_fields = (
            'user', 'avg_rating', 'total_ratings', 'contact_is_verified', \
            'languages', 'certifications', 'work_experience', \
            'profile_completeness'
        )
        fields = [
            'id', 'bio', 'country', 'location', 'avg_rating', \
            'total_ratings', 'profession', \
            'hourly_rate', \
            'education_level', 'user', 'certifications', \
            'work_experience', 'languages'
        ]



class JobseekerLoggedInProfileSerializer(JobseekerCompleteDetailSerializer):
    class Meta:
        model = JobseekerProfile
        read_only_fields = (
            'user', 'avg_rating', 'total_ratings', 'contact_is_verified', \
            'languages', 'certifications', 'work_experience', \
            'profile_completeness'
        )
        fields = [
            'id', 'bio', 'country', 'location', 'avg_rating', \
            'total_ratings', 'profession', \
            'hourly_rate', 'education_level', 
            'profile_completeness', 'user', 'certifications', \
            'work_experience', 'languages',
        ]


class JobseekerIncompleteDetailSerializer(serializers.ModelSerializer):
    languages = JobseekerLanguageSerializer(many=True,)
    certifications = JobseekerCertificationSerializer(many=True, source='jobseeker_certifications')
    work_experience = WorkExperienceSerializer(many=True, source='jobseeker_experience')
    user = UserDetailSlimSerializer(read_only=True)
    contact_preview = serializers.SerializerMethodField('get_contact_preview')


    @extend_schema_field(OpenApiTypes.STR)
    def get_contact_preview(self, jobseeker_profile):
        try:
            phone_number = jobseeker_profile.user.phone_number
            preview = f"+{str(phone_number.country_code)}"
            return preview 
        except:
            return

    class Meta:
        model = JobseekerProfile
        read_only_fields = (
            'user', 'avg_rating', 'total_ratings',
            'languages', 'certifications', 'work_experience',
        )
        fields = [
            'id', 'bio', 'country', 'location', 'avg_rating', 'contact_preview', \
            'total_ratings', 'profession', 'hourly_rate', 'education_level', \
            'user', 'certifications', 'work_experience', 'languages'
        ]

@extend_schema_serializer(
    examples = jobseeker_examples
)
class JobseekerProfileModSerializer(serializers.ModelSerializer):
    """
    Joins the user model with the jobseeker's profile.
    """
    user = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = JobseekerProfile
        read_only_fields = (
            'avg_rating', 'total_ratings', 'phone_number', 
            'contact_is_verified',
        )
        fields = [
            'user', 'bio', 'country', 'location', 'avg_rating', \
            'total_ratings', 'profession', 'education_level', \
            'hourly_rate'
        ]

    def update(self, instance, validated_data):
        # Save the main jobseeker profile instance
        return super(JobseekerProfileModSerializer, self).update(instance, validated_data)

# access_code = serializers.ListSerializer(
#     child=UserAccessCreditSerializer(),
#     # source='access_code',
# )

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_field,
    extend_schema_serializer,
)


@extend_schema_serializer(
    examples = employer_examples
)
class EmployerProfileSerializer(serializers.ModelSerializer):
    """
    Returns the user details and also the employer's profile details.
    """
    access_credits = serializers.SerializerMethodField('get_access_credits')
    user = CustomUserDetailsSerializer(read_only=True)

    @extend_schema_field(OpenApiTypes.STR)
    def get_access_credits(self, profile):
        credits = UserAccessCredit.objects.filter(email=profile.user.email, is_valid=True)
        serializer = UserAccessCreditSerializer(credits, many=True)
        return serializer.data

    class Meta:
        model = EmployerProfile
        read_only_fields = ['access_credits']
        fields = [ 'id', 'stripe_customer_id', 'user', 'access_credits']

    def update(self, instance, validated_data):
        # Save the main employer profile instance
        return super(EmployerProfileSerializer, self).update(instance, validated_data)

from django.db import models


class LOG_IN_AS_CHOICES(models.TextChoices):
    JOBSEEKER = "Jobseeker", "Jobseeker"
    EMPLOYER = "Employer", "Employer"

class LoginStateSerializer(serializers.Serializer):
    log_in_as = serializers.ChoiceField(
        choices=LOG_IN_AS_CHOICES,  
        required=True,
    )


# Resend Verification Email
class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

# Logout
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=False)

# Verify Email
class CustomVerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()

class VerifyEmailSuccessData(serializers.Serializer):
    email = serializers.EmailField(required=True)


# Unlocked Profiles


# Response Serializers
class VerifyEmailSuccessResponseSerializer(serializers.Serializer):
    data = VerifyEmailSuccessData()
    message = serializers.CharField()
    status = serializers.CharField()
    status_code = serializers.CharField()

# User Login
class LoginSuccessSerializer(serializers.Serializer):
    data = JWTSerializer()
    message = serializers.CharField()
    status = serializers.CharField()
    status_code = serializers.IntegerField()

# Password Reset
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

# Generic Response Serializers
class GenericErrorResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    status = serializers.CharField()
    status_code = serializers.IntegerField()
    error_code = serializers.CharField()

class GenericSuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    status = serializers.CharField()
    status_code = serializers.CharField()

class UserSlimSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()


class RegisterSuccessResponseSerializer(serializers.Serializer):
    data = UserSlimSerializer()
    message = serializers.CharField()
    status = serializers.CharField()
    status_code = serializers.CharField()
