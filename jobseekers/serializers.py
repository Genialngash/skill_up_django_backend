from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from pkg_resources import require
from rest_framework import serializers
from users.model_choices import MONTHS_OF_THE_YEAR

from jobseekers.models import JobseekerCertification, JobseekerLanguage, WorkExperience

from .prof_info_validation.info_helpers import (
    validate_end_year_payload,
    validate_month,
    validate_start_month_payload,
    validate_year,
)


class WorkExperienceSoloCompleteSerializer(serializers.ModelSerializer):
    """
    Used when user is NOT currently working in the workplace entry being saved.
    """

    end_year = serializers.IntegerField(
        allow_null=False,
        required=True,
    )
    end_month = serializers.ChoiceField(
        choices=MONTHS_OF_THE_YEAR.choices,
        allow_blank=False,
        required=True,
        allow_null=False,
    )
    currently_working_here = serializers.BooleanField(required=True)


    def validate_start_year(self, value):
        year = validate_year(value)
        if year is None:
            raise serializers.ValidationError("Invalid start year.")

        return value


    def validate_start_month(self, value):
        month = validate_start_month_payload(self)
        if month is None:
            raise serializers.ValidationError("Invalid start month.")

        return value


    def validate_end_year(self, value):
        year = validate_end_year_payload(self)
        if year is None:
            raise serializers.ValidationError("Invalid end year.")
        return value


    def validate_end_month(self, value):
        month = validate_month(self, month=self.initial_data['end_month'])
        if month is None:
            raise serializers.ValidationError("Invalid end month.")
        return value

    class Meta:
        model = WorkExperience
        fields = [
            'profile', 'company_name', \
            'start_month', 'start_year', 'end_month', \
            'end_year', 'currently_working_here'
        ]

class WorkExperienceSoloIncompleteSerializer(serializers.ModelSerializer):
    """
    Used when user currently works in the workplace entry being saved.
    """

    def validate_start_year(self, value):
        year = validate_year(value)
        if year is None:
            raise serializers.ValidationError("Invalid start year.")

        return value


    def validate_start_month(self, value):
        month = validate_start_month_payload(self)
        if month is None:
            raise serializers.ValidationError("Invalid start month.")

        return value

    class Meta:
        model = WorkExperience
        fields = [
            'profile', 'company_name', \
            'start_month', 'start_year', \
            'currently_working_here'
        ]



class WorkExperienceSoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = [
            'id', 'profile', 'company_name', \
            'start_month', 'start_year', 'end_month', \
            'end_year', 'currently_working_here'
        ]



class WorkExperienceSerializer(serializers.ModelSerializer):
    end_year = serializers.IntegerField(required=False)
    end_month = serializers.ChoiceField(
        choices=MONTHS_OF_THE_YEAR.choices,
        allow_blank=False,
        required=False
    )
    currently_working_here = serializers.BooleanField(required=True)

    class Meta:
        model = WorkExperience
        fields = [
            'company_name', 'start_month', \
            'start_year', 'end_month', \
            'end_year', 'currently_working_here'
        ]

    def validate_start_year(self, value):
        year = validate_year(value)
        if year is None:
            raise serializers.ValidationError("Invalid start year.")
        return value

    def validate_end_year(self, value):
        year = validate_year(value)
        if year is None:
            raise serializers.ValidationError("Invalid end year.")
        return value

    def validate_end_month(self, value):
        month = validate_month(self, month=self.initial_data['end_month'])
        if month is None:
            raise serializers.ValidationError("Invalid end month.")
        return value


class JobseekerLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobseekerLanguage
        fields = ['name', 'proficiency_level']


class JobseekerCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobseekerCertification
        fields = ['title', 'certification_year']

    def validate_certification_year(self, value):
        year = validate_year(value)
        if year is None:
            raise serializers.ValidationError("Invalid certification year.")
        return value


class JobseekerProfessionalInfoSerializer(serializers.Serializer):
    languages = serializers.ListField(
        child=JobseekerLanguageSerializer(), 
        allow_empty=False,
    )
    certifications = serializers.ListField(
        child=JobseekerCertificationSerializer(), 
        allow_empty=False,
    )
    work_experience = serializers.ListField(
        child=WorkExperienceSerializer(), 
        allow_empty=False,
    )


# Job Offer Serializer


# END Job Offer Serializer
