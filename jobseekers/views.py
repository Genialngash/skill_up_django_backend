from datetime import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters import rest_framework as filters
from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from establishments.permissions import IsAuthenticatedAndIsJobseeker
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import JobseekerProfile
from users.serializers import (
    GenericErrorResponseSerializer,
    JobseekerIncompleteDetailSerializer,
    JobseekerSlimSerializer,
)
from utils.pagination import VeetaBasePaginationSet

import jobseekers
from jobseekers import pagination
from jobseekers.models import JobseekerCertification, WorkExperience

from . import serializers
from .filters import JobseekerFilters
from .prof_info_validation import professional_info
from .view_fixes import *


class JobseekersListView(generics.ListAPIView):
    """
    List all jobseekers. Returns all jobseekers with verified contacts.
    """
    serializer_class = JobseekerIncompleteDetailSerializer
    pagination_class = VeetaBasePaginationSet
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = JobseekerFilters

    def get_queryset(self):
        queryset = JobseekerProfile.objects \
            .prefetch_related(
                'languages',
                'jobseeker_certifications',
                'jobseeker_experience',
                'user'
            ).filter(user__contact_is_verified=True)

        # queryset = JobseekerProfile.objects.filter(contact_is_verified=True)
        return queryset


    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        queryset = JobseekerFilters(self.request.GET, queryset=qs).qs
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Success.',
            'status': 'ok.',
            'status_code': 200,
        })


from jobseekers.models import JobseekerCertification, JobseekerLanguage, WorkExperience


class JobseekerLanguagesListView(generics.ListAPIView):
    serializer_class = serializers.JobseekerLanguageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_anonymous:
            return JobseekerLanguage.objects.none()
        
        jobseeker_profile = user.jobseeker_profile
        queryset = JobseekerLanguage.objects.filter(profile=jobseeker_profile)
        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'status': 'ok',
            'message': 'Success.',
            'status_code': 200
        }, status=status.HTTP_200_OK)


class LanguageViewSet(viewsets.ViewSet):
    serializer_class = serializers.JobseekerLanguageSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']
    lookup_field = 'id'

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def get_object(self):
        user = self.request.user
        jobseeker_profile = user.jobseeker_profile
        lang_id = self.kwargs.get('pk')
        obj = get_object_or_404(JobseekerLanguage, id=lang_id, profile=jobseeker_profile)
        return obj


    def retrieve(self, request, pk=None):
        queryset = JobseekerLanguage.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = serializers.JobseekerLanguageSerializer(user)

        return Response({
            'data': serializer.data,
            'status': 'ok',
            'message': 'Success.',
            'status_code': 200
        }, status=status.HTTP_200_OK)


    def create(self, request):
        serializer = serializers.JobseekerLanguageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if it exists
        try:
            obj = JobseekerLanguage.objects.get(
                name=serializer.validated_data['name'],
                profile=serializer.validated_data['profile'],
            )

            if obj:
                return Response({
                    'message': 'Language already exists.',
                    'status': 'error',
                    'status_code': 400
                }, status=status.HTTP_400_BAD_REQUEST)

        except JobseekerLanguage.DoesNotExist:
            obj = JobseekerLanguage.objects.create(
                name=serializer.validated_data['name'],
                profile=serializer.validated_data['profile'],
                proficiency_level=serializer.validated_data['proficiency_level'],
            )

            res_serializer = serializers.JobseekerLanguageSerializer(obj)
            return Response({
                'data': res_serializer.data,
                'status': 'ok',
                'message': 'Language saved.',
                'status_code': 201
            }, status=status.HTTP_201_CREATED)


    def update(self, request, pk=None):
        serializer = serializers.JobseekerLanguageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'data': serializer.data,
            'status': 'ok',
            'message': 'Language updated successfully.',
            'status_code': 200
        }, status=status.HTTP_200_OK)


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


    def destroy (self, request, pk=None, *args, **kwargs):
        user = self.request.user
        jobseeker_profile = user.jobseeker_profile
        instance = self.get_object()

        if instance and instance.profile == jobseeker_profile:
            # Make deletion
            self.perform_destroy(instance)
        else:
            return Response({
                    'message': "You cannot modify another user's profile data.",
                    'status': 'error',
                    'status_code': 401,
                    'error_code': 'unauthorized'
                }, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            'message': "Language entry deleted successfully.",
            'status': 'ok',
            'status_code': 200,
        }, status=status.HTTP_200_OK)



# Certifications


class JobseekerCertificationsListView(generics.ListAPIView):
    serializer_class = serializers.JobseekerCertificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return JobseekerCertification.objects.none()
        
        jobseeker_profile = user.jobseeker_profile
        queryset = JobseekerCertification.objects.filter(profile=jobseeker_profile)

        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'status': 'ok',
            'message': 'Success.',
            'status_code': 200
        }, status=status.HTTP_200_OK)



class CertificationViewSet(viewsets.ViewSet):
    serializer_class = serializers.JobseekerCertificationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']
    lookup_field = 'id'

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def get_object(self):
        user = self.request.user
        jobseeker_profile = user.jobseeker_profile
        cert_id = self.kwargs.get('pk')
        obj = get_object_or_404(JobseekerCertification, id=int(cert_id), profile=jobseeker_profile)
        return obj


    def retrieve(self, request, pk=None):
        queryset = JobseekerLanguage.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = serializers.JobseekerCertificationSerializer(user)

        return Response({
            'data': serializer.data,
            'status': 'ok',
            'message': 'Success.',
            'status_code': 200
        }, status=status.HTTP_200_OK)


    def create(self, request):
        serializer = serializers.JobseekerCertificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if it exists
        try:
            obj = JobseekerCertification.objects.get(
                title=serializer.validated_data['title'],
                profile=serializer.validated_data['profile'],
            )

            if obj:
                return Response({
                    'message': 'Certification already exists.',
                    'status': 'error',
                    'status_code': 400
                }, status=status.HTTP_400_BAD_REQUEST)

        except JobseekerCertification.DoesNotExist:
            obj = JobseekerCertification.objects.create(
                title=serializer.validated_data['title'],
                profile=serializer.validated_data['profile'],
                certification_year=serializer.validated_data['certification_year'],
            )

            res_serializer = serializers.JobseekerCertificationSerializer(obj)
            return Response({
                'data': res_serializer.data,
                'status': 'ok',
                'message': 'Certification saved.',
                'status_code': 201
            }, status=status.HTTP_201_CREATED)


    def update(self, request, pk=None):
        serializer = serializers.JobseekerCertificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'data': serializer.data,
            'status': 'ok',
            'message': 'Certification updated successfully.',
            'status_code': 200
        }, status=status.HTTP_200_OK)


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


    def destroy (self, request, pk=None, *args, **kwargs):
        user = self.request.user
        jobseeker_profile = user.jobseeker_profile
        instance = self.get_object()

        if instance and instance.profile == jobseeker_profile:
            # Make deletion
            self.perform_destroy(instance)
        else:
            return Response({
                    'message': "You cannot modify another user's profile data.",
                    'status': 'error',
                    'status_code': 401,
                    'error_code': 'unauthorized'
                }, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            'message': "Certification entry deleted successfully.",
            'status': 'ok',
            'status_code': 200,
        }, status=status.HTTP_200_OK)




class JobseekerProfessionalInfoView(APIView):
    serializer_class = serializers.JobseekerProfessionalInfoSerializer
    permission_classes = [IsAuthenticated]


    def patch(self, request, *args, **kwargs):
        user = request.user
        profile = user.jobseeker_profile
        data = dict(request.data)

        return professional_info.handler(
            self,
            action='update',
            data=data,
            user=user,
            profile=profile,
            lang_serializer=serializers.JobseekerLanguageSerializer,
            cert_serializer=serializers.JobseekerCertificationSerializer,
            work_experience_serializer=serializers.WorkExperienceSerializer,
        )



# Work Experience Solo ViewSet
from .serializers import (
    WorkExperienceSerializer,
    WorkExperienceSoloCompleteSerializer,
    WorkExperienceSoloIncompleteSerializer,
)


class WorkExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WorkExperienceSoloSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete', 'options', 'head']
    lookup_url_kwarg = 'pk'
    lookup_field = 'pk'


    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


    def get_object(self):
        user = self.request.user
        jobseeker_profile = user.jobseeker_profile
        work_experience_id = self.kwargs.get('pk')
        obj = get_object_or_404(WorkExperience, id=work_experience_id, profile=jobseeker_profile)
        return obj


    def perform_create(self, serializer):
        serializer.save()


    def retrieve(self, request,  *args, **kwargs):
        work_experience = self.get_object()
        serializer = serializers.WorkExperienceSoloSerializer(work_experience)

        return Response({
            'data': serializer.data,
            'status': 'ok',
            'message': 'Success.',
            'status_code': 200
        }, status=status.HTTP_200_OK)


    def create(self, request):
        request_data = request.data

        if not 'currently_working_here' in request_data:
            return Response({
                'status': 'error',
                'message': 'currently_working_here is a required field.',
                'status_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)


        if 'currently_working_here' in request_data:
            # Omit end_month and end_year
            if request_data['currently_working_here']:
                serializer = WorkExperienceSoloIncompleteSerializer(data=request_data)
                serializer.is_valid(raise_exception=True)
            
                self.perform_create(serializer)
                return Response({
                    'data': serializer.data,
                    'status': 'ok',
                    'message': 'Work experience saved.',
                    'status_code': 201
                }, status=status.HTTP_201_CREATED)


            # All fields mandatory
            if not request_data['currently_working_here']:
                serializer = WorkExperienceSoloCompleteSerializer(data=request_data)
                serializer.is_valid(raise_exception=True)

                self.perform_create(serializer)
                return Response({
                    'data': serializer.data,
                    'status': 'ok',
                    'message': 'Work experience saved.',
                    'status_code': 201
                }, status=status.HTTP_201_CREATED)
                

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not 'currently_working_here' in request.data:
            return Response({
                'status': 'error',
                'message': 'currently_working_here is a required field.',
                'status_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        
        if 'currently_working_here' in request.data:
            # Omit end_month and end_year
            if request.data['currently_working_here']:
                serializer = WorkExperienceSoloIncompleteSerializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)

                self.perform_update(serializer)
                return Response({
                    'data': serializer.data,
                    'status': 'ok',
                    'message': 'Work experience updated successfully.',
                    'status_code': 200
                }, status=status.HTTP_200_OK)


            # All fields mandatory
            if not request.data['currently_working_here']:
                serializer = WorkExperienceSoloCompleteSerializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)

                self.perform_update(serializer)
                return Response({
                    'data': serializer.data,
                    'status': 'ok',
                    'message': 'Work experience updated successfully.',
                    'status_code': 200
                }, status=status.HTTP_200_OK)


    def destroy (self, request, pk=None, *args, **kwargs):
        user = self.request.user
        jobseeker_profile = user.jobseeker_profile
        instance = self.get_object()

        if instance and instance.profile == jobseeker_profile:
            # Make deletion
            self.perform_destroy(instance)
        else:
            return Response({
                    'message': "You cannot modify another user's profile data.",
                    'status': 'error',
                    'status_code': 401,
                    'error_code': 'unauthorized'
                }, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            'message': "Work experience entry deleted.",
            'status': 'ok',
            'status_code': 200,
        }, status=status.HTTP_200_OK)




from employers.models import JobOffer
from employers.serializers import AcceptJobOfferSerializer, JobOfferSerializer


class JobOffersListView(generics.ListAPIView):
    """
    List all job offers made to a jobseeker.
    """

    serializer_class = JobOfferSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = VeetaBasePaginationSet


    def get_queryset(self):
        qs = JobOffer.objects.filter(applicant=self.request.user)
        return qs


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
        }, status=status.HTTP_200_OK)


class JobOfferAcceptView(generics.UpdateAPIView):
    """
    Accept a job offer. 
    This endpoint allows a jobseeker to accept an offer made to them by an employer.
    """

    serializer_class = AcceptJobOfferSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ('PUT', 'OPTIONS', 'HEAD')

    def get_object(self):
        job_offer_id = self.kwargs.get('job_offer_id')

        if not job_offer_id:
            return JobOffer.objects.none()

        try:
            obj = JobOffer.objects.get(id=job_offer_id)
            return obj
        except JobOffer.DoesNotExist:
            return JobOffer.objects.none()


    def perform_update(self, serializer):
        serializer.save()


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if not instance:
            return Response({
                'message': 'Job offer not found!',
                'status_code': 400,
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)


        if instance.applicant.id != user.id:
            return Response({
                'message': 'You are not authorized to make this request.',
                'status_code': 403,
                'status': 'error'
            }, status=status.HTTP_403_FORBIDDEN)


        if instance.applicant.id == user.id:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)

            instance.accepted_at_timestamp = timezone.now()
            instance.is_accepted = serializer.validated_data['is_accepted']
            instance.save()

            # TODO Alert the employer

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response({
                'data': serializer.data,
                'message': 'Job offer accepted.',
                'status': 'ok',
                'status_code': 200
            }, status=status.HTTP_200_OK)


        return Response({
            'message': 'Oops! Something went wrong.',
            'status_code': 400,
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)
