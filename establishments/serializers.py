from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers
from users.serializers import UserExtraSlimSerializer
from users.serializers import JobseekerSlimSerializer,EmployerProfileSerializer
from .models import Company, Employee, CourseCard, LessonsModule, Completed,Enrolments, Checker


@extend_schema_serializer(
    examples = [
         OpenApiExample(
            'Create a company success',
            description=
                """This is the response you create a company successfully.""",
            value={
                "data": {
                    "id": 0,
                    "name": "Harper Ltd",
                    "email": "example-email@company.com",
                    "logo": "/media/default_logo.jpg",
                    "website_url": "https://harper-inc.com",
                    "bio": "Happy commercial need Mr close without. Bed clear dark air. Occur relationship possible a.",
                    "hiring_manager": 0
                },
                "message": "Company created successfully.",
                "status": "success",
                "status_code": 201
            },
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            'Create a company failure',
            description=
                """This is the response you get after an unsuccesfull attempt to create a company.""",

            value={
                "error_code": "string",
                "message": "string",
                "status": "error",
                "status_code": 400
            },
            
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            'List all user companies',
            description=
                """This is the response you get after an successfull attempt to list all companies belonging to a user.""",
            value={
                "data": [
                    {
                        "id": 0,
                        "name": "Harper Ltd",
                        "email": "example-email@company.com",
                        "logo": "/media/default_logo.jpg",
                        "website_url": "https://harper-inc.com",
                        "bio": "Happy commercial need Mr close without. Bed clear dark air. Occur relationship possible a.",
                        "hiring_manager": 0
                    }
                ],
                "message": "Sample message",
                "status": "success",
                "status_code": 200
            },
            request_only=False,
            response_only=True,
        ),
    ],
)
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'email', "logo", "location",
            'website_url', 'bio', 'hiring_manager'
        ]

class CompanySlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'logo', 'bio']

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserExtraSlimSerializer()
    company = CompanySlimSerializer()
    class Meta:
        model = Employee
        fields = ("id",'user', 'company', 'role', 'joined_on', 'is_active',)

class LessonsModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonsModule
        fields = ("id","course", "lesson_name","lesson_description")

class CourseCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCard
        fields = ("id","proffesional", "course_name","course_description")

class CompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Completed
        fields = ("lesson", "enrolment","id")

class CheckerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checker
        fields = ("lesson", "enrolment","id")

class EnrolmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Enrolments
        fields = ("id","course", "by")

