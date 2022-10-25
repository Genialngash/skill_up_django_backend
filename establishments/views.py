from django.http import request
from django.http.request import QueryDict
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from users.models import EmployerProfile,JobseekerProfile
from utils.pagination import VeetaBasePaginationSet

from establishments import pagination, permissions, serializers

from .filters import CompanyListFilter
from .models import Company, Employee,CourseCard, LessonsModule, Completed,Enrolments,Checker
from .permissions import IsAuthenticatedAndIsEmployer, IsAuthenticatedAndIsJobseeker
from .serializers import CompanySerializer, EmployeeSerializer, CourseCardSerializer, CheckerSerializer, LessonsModuleSerializer,CompletedSerializer, EnrolmentSerializer


# COMPANY VIEWS
class UserCompaniesListView(viewsets.ViewSet):
    """
    List all the companies owned by a user. Returns all the companies owned by the authenticated user
    """
    serializer_class = serializers.CompanySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.u_type == 'Jobseeker':
            return Response({
                'status': 'error',
                'status_code': 401,
                'message': 'Only employers are allowed to own companies.',
            }, status=status.HTTP_401_UNAUTHORIZED)

        queryset = Company.objects.filter(hiring_manager=user.id)
        serializer = serializers.CompanySerializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'status': 'success',
            'status_code': 200,
            'message': 'Success.',
        })

class CoursesViewSet(viewsets.ViewSet):
    serializer_class = CourseCardSerializer
    queryset = CourseCard.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CourseCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
                'data': serializer.data,
                'status': 'ok',
                'status_code': 201,
                'message': 'Course created successfully.',
            }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = CourseCard.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({
            'data': serializer.data,
            'status': 'success',
            'status_code': 200,
            'message': 'Success.',
        })

    def get_object(self):
        completed_id = self.kwargs.get('pk')
        instance = EmployerProfile(id=completed_id)
        courses = CourseCard.objects.filter(proffesional=instance)
        return courses

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CourseCardSerializer(instance,many=True)
        return Response({
            'data': serializer.data,
            'message': 'Success.',
            'status_code': 200,
            'status': 'ok'
        })

class LessonsViewSet(viewsets.ViewSet):
    serializer_class = LessonsModuleSerializer
    queryset = LessonsModule.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = LessonsModuleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
                'data': serializer.data,
                'status': 'ok',
                'status_code': 201,
                'message': 'Lesson created successfully.',
            }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = LessonsModule.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({
            'data': serializer.data,
            'status': 'success',
            'status_code': 200,
            'message': 'Success.',
        })
    def get_object(self):
        completed_id = self.kwargs.get('pk')
        instance = CourseCard(id=completed_id)
        lessons = LessonsModule.objects.filter(course=instance)
        return lessons

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = LessonsModuleSerializer(instance,many=True)
        return Response({
            'data': serializer.data,
            'message': 'Success.',
            'status_code': 200,
            'status': 'ok'
        })

class EnrolmentViewSet(viewsets.ViewSet):
    serializer_class = EnrolmentSerializer
    queryset = Enrolments.objects.all()

    def create(self, request, *args, **kwargs):
        print(request.user)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
                'data': serializer.data,
                'status': 'ok',
                'status_code': 201,
                'message': 'Lesson created successfully.',
            }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = Enrolments.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({
            'data': serializer.data,
            'status': 'success',
            'status_code': 200,
            'message': 'Success.',
        })

    def get_object(self):
        completed_id = self.kwargs.get('pk')
        instance = JobseekerProfile(id=completed_id)
        enrolments = Enrolments.objects.filter(by=instance)
        return enrolments

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EnrolmentSerializer(instance,many=True)
        return Response({
            'data': serializer.data,
            'message': 'Success.',
            'status_code': 200,
            'status': 'ok'
        })
    def get_course_object(self):
        completed_id = self.kwargs.get('pk')
        instance = CourseCard(id=completed_id)
        enrolments = Enrolments.objects.filter(course=instance)
        return enrolments

    def course_retrieve(self, request, *args, **kwargs):
        instance = self.get_course_object()
        serializer = EnrolmentSerializer(instance,many=True)
        return Response({
            'data': serializer.data,
            'message': 'Success.',
            'status_code': 200,
            'status': 'ok'
        })

class CompletedViewSet(viewsets.ViewSet):
    serializer_class = CompletedSerializer
    queryset = Completed.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CompletedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
                'data': serializer.data,
                'status': 'ok',
                'status_code': 201,
                'message': 'Marked Complete.',
            }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = Completed.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({
            'data': serializer.data,
            'status': 'success',
            'status_code': 200,
            'message': 'Success.',
        })

    def get_object(self):
        completed_id = self.kwargs.get('pk')
        instance = Enrolments(id=completed_id)
        enrolments = Completed.objects.filter(enrolment=instance)
        return enrolments

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CompletedSerializer(instance,many=True)
        return Response({
            'data': serializer.data,
            'message': 'Success.',
            'status_code': 200,
            'status': 'ok'
        })

class CheckerViewSet(viewsets.ViewSet):
    serializer_class = CheckerSerializer
    queryset = Checker.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
                'data': serializer.data,
                'status': 'ok',
                'status_code': 201,
                'message': 'Check set successfully.',
            }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = Checker.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({
            'data': serializer.data,
            'status': 'success',
            'status_code': 200,
            'message': 'Success.',
        })

    def get_object(self):
        completed_id = self.kwargs.get('pk')
        instance = Enrolments(id=completed_id)
        enrolments = Checker.objects.filter(enrolment=instance)
        return enrolments

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CheckerSerializer(instance,many=True)
        return Response({
            'data': serializer.data,
            'message': 'Success.',
            'status_code': 200,
            'status': 'ok'
        })

class CompanyViewSet(viewsets.ViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticatedAndIsEmployer]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Creates a new company.
        Companies can only be created for the currently authenticated user.
        The hiring manager represents the user id of the employer.
        """
        user = request.user
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if user.u_type == 'General' and user.logged_in_as == 'Employer':
            if serializer.validated_data['hiring_manager'] != user:
                return Response({
                    'message': 'You can only create a company for yourself.',
                    'status': 'error',
                    'status_code': 400,
                    'error_code': 'unauthorized'
                }, status=status.HTTP_400_BAD_REQUEST)

            user_companies = Company.objects.filter(hiring_manager=user)
            if len(user_companies) >= 3:
                return Response({
                    'data': serializer.data,
                    'status': 'permission_denied',
                    'status_code': 400,
                    'message': 'You have reached the maximum limit. Only 3 companies are allowed for one account.',
                }, status=status.HTTP_400_BAD_REQUEST)


    
            self.perform_create(serializer)
            return Response({
                'data': serializer.data,
                'status': 'ok',
                'status_code': 201,
                'message': 'Company created successfully.',
            }, status=status.HTTP_201_CREATED)

        if user.logged_in_as == 'Jobseeker':
            return Response({
                'message': 'Switch to your jobseeker profile to add a company.',
                'status': 'error',
                'status_code': 400,
                'error_code': 'unauthorized'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        company_id = self.kwargs.get('pk')
        company = get_object_or_404(Company, id=company_id)
        return company

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CompanySerializer(instance)
        return Response({
            'data': serializer.data,
            'message': 'Success.',
            'status_code': 200,
            'status': 'ok'
        })

    def update(self, request, *args, **kwargs):
        user = self.request.user
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = CompanySerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance and instance.hiring_manager == user:
            # Make update
            self.perform_update(serializer)
        else:
            return Response({
                    'message': 'You can only modify your company details.',
                    'status': 'error',
                    'status_code': 401,
                    'error_code': 'unauthorized'
                }, status=status.HTTP_401_UNAUTHORIZED
            )

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({
            'data': serializer.data,
            'status': 'ok',
            'status_code': 200,
            'message': 'Company update success.'
        })

    def perform_update(self, serializer):
        serializer.save()


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        if instance and instance.hiring_manager == user:
            # Make update
            self.perform_destroy(instance)
        else:
            return Response({
                    'message': "You cannot delete another user's company.",
                    'status': 'error',
                    'status_code': 401,
                    'error_code': 'unauthorized'
                }, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            'message': "Company deleted successfully.",
            'status': 'ok',
            'status_code': 200,
        }, status=status.HTTP_200_OK)


class EmployeesListView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticatedAndIsEmployer]
    pagination_class = VeetaBasePaginationSet


    def get_queryset(self):
        user = self.request.user
        companies = Company.objects.filter(hiring_manager=user)
        co_ids = []
        for co in companies:
            co_ids.append(co.id)
        emps = Employee.objects.filter(company__in=co_ids)
        return emps


    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
