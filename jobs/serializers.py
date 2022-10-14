
from django.utils.html import linebreaks
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_field,
    extend_schema_serializer,
)
from establishments.models import Company, JobApplication, JobCard, JobResponsibility
from establishments.serializers import CompanySlimSerializer
from rest_framework import serializers
from users.models import JobseekerProfile
from users.serializers import (
    JobseekerCompleteDetailSerializer,
    User,
    UserExtraSlimSerializer,
)

from .models import JobBookmark
from .swagger_jobs_examples import job_applications_examples, job_card_examples


@extend_schema_serializer(
    examples=job_applications_examples
)
class JobApplicationCreateSerializer(serializers.ModelSerializer):
    """A serializer for job applications. The user represents the job applicant."""
    class Meta:
        model = JobApplication
        fields = ['id', 'job_card', 'user']


class JobResponsibilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResponsibility
        fields = ('text',)


class JobCardCreateModifySerializer(serializers.ModelSerializer):
    responsibilities = JobResponsibilitiesSerializer(many=True)
    class Meta:
        model = JobCard
        fields = [
            'id', 'company', 'role', 'category', 'contract_type', 'responsibilities', \
            'description', 'location', 'created_on', 'updated_on', \
            'application_deadline', 'is_published', 'taken', 'pay', 'created_on', 'time_since'
        ]

    def create(self, validated_data):
        responsibilities = validated_data.pop('responsibilities')
        card = JobCard.objects.create(**validated_data)
        for res in responsibilities:
            JobResponsibility.objects.create(card=card, **res)
        return card


    def update(self, instance, validated_data):
        responsibilities = validated_data.pop('responsibilities')
        all_saved_responsibilities = JobResponsibility.objects.filter(card=instance)
        
        if len(all_saved_responsibilities) == 0:
            for res in responsibilities:
                JobResponsibility.objects.create(text=res['text'], card=instance)

        if len(responsibilities) == len(all_saved_responsibilities):
            for count, value in enumerate(all_saved_responsibilities):
                value.text = responsibilities[count]['text']
                value.save()
                print('Update Success')

        if len(responsibilities) != len(all_saved_responsibilities):
            old_limit = len(all_saved_responsibilities)
            new_total = len(responsibilities)

            if (old_limit - new_total) > 0:
                # diff = old_limit - new_total
                # print('New is shorter by ' + str(diff))
                to_del = list(range(new_total, old_limit))

                for index in to_del:
                    item = all_saved_responsibilities[index]
                    item.delete()

                rem = JobResponsibility.objects.filter(card=instance)
                
                for count, item in enumerate(rem):
                    item.text = responsibilities[count]['text']
                    item.save()

            if (old_limit - new_total) < 0:
                # diff = old_limit - new_total
                # print('New is longer by ' + str(diff))
                mod = list(range(old_limit, new_total))
                for item in mod:
                    JobResponsibility.objects.create(text=responsibilities[item]['text'], card=instance)

        # finally save the main jobseeker profile instance
        return super(JobCardSerializer, self).update(instance, validated_data)



@extend_schema_serializer(
    examples=job_card_examples
)
class JobCardSerializer(serializers.ModelSerializer):
    responsibilities = JobResponsibilitiesSerializer(many=True)
    time_since = serializers.SerializerMethodField('get_time_since')
    company = CompanySlimSerializer()

    @extend_schema_field(OpenApiTypes.STR)
    def get_time_since(self, card):
        return str(card.time_since)
    class Meta:
        model = JobCard
        fields = [
            'id', 'company', 'role', 'category', 'contract_type', 'responsibilities', \
            'description', 'location', 'created_on', 'updated_on', \
            'application_deadline', 'is_published', 'taken', 'pay', 'created_on', 'time_since'
        ]

class JobCardSlimSerializer(serializers.ModelSerializer):
    company = CompanySlimSerializer()
    time_since = serializers.SerializerMethodField('get_time_since')

    @extend_schema_field(OpenApiTypes.STR)
    def get_time_since(self, card):
        return str(card.time_since)

    class Meta:
        model = JobCard
        fields = [
            'id', 'role', 'category', 'description', \
            'contract_type', 'location', 'created_on', \
            'updated_on', 'application_deadline', \
            'is_published', 'company', 'time_since', \
            'positions_available', 'pay'
        ]

class JobApplicationGetDetailSerializer(serializers.ModelSerializer):
    """A serializer for getting or modifying job applications"""
    # card = JobCardSlimSerializer()
    applicant_profile = JobseekerCompleteDetailSerializer(source='user_profile')

    class Meta:
        model = JobApplication
        fields = ['id', 'job_card', 'applicant_profile',]


class JobApplicationApproveSerializer(serializers.Serializer):
    """A serializer for approving job applications"""
    approved = serializers.BooleanField(required=True)



class JobBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobBookmark
        fields = ('job_card', 'user',)


# Job Applicants List View Serializers
class ApplicantListCompanySlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name',]

class ApplicantListJobCardSlimSerializer(serializers.ModelSerializer):
    company = ApplicantListCompanySlimSerializer()
    class Meta:
        model = JobCard
        fields = ['id', 'role', 'company',]

class ApplicantProfileSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobseekerProfile
        fields = ('id', 'profession', 'total_ratings', 'avg_rating', 'hourly_rate')

class ApplicantDetailSerializer(serializers.ModelSerializer):
    profile = ApplicantProfileSlimSerializer(source='jobseeker_profile')

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'avatar', \
            'email', 'contact_is_verified', 'phone_number',
            'profile'
        )


@extend_schema_serializer(
    examples = [
         OpenApiExample(
            'List job applications',
            description=
                """This is the response you list job applications based on a specific job card""",
            value={
                "data": {
                    "current_page": 0,
                    "previous_page": None,
                    "next_page": None,
                    "count": 0,
                    "results": [
                      {
                        "id": 0,
                        "user": {
                          "id": 0,
                          "first_name": "string",
                          "last_name": "string",
                          "avatar": "string",
                          "email": "string",
                          "contact_is_verified": "bool",
                          "phone_number": "string",
                          "profile": {
                            "id": 0,
                            "profession": "string",
                            "total_ratings": 0,
                            "avg_rating": "1.00",
                            "hourly_rate": 0
                          }
                        },
                        "job_card": {
                          "id": 10,
                          "role": "string",
                          "company": {
                            "name": "string"
                          }
                        }
                      },
                    ]
                },
                "message": "string",
                "status": "string",
                "status_code": 200
            },
            request_only=False,
            response_only=True,
        ),
    ]
)
class JobApplicationsListSerializer(serializers.ModelSerializer):
    user = ApplicantDetailSerializer(read_only=True)
    job_card = ApplicantListJobCardSlimSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'user','job_card',]

# END Job Applicants List View Serializers
