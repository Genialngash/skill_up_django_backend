from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, inline_serializer
from establishments.models import Company, JobApplication, JobCard, JobResponsibility
from establishments.permissions import IsAuthenticatedAndIsJobseeker
from notifications.models import (
    EmailNotificationSubscription,
    Notification,
    NotificationTagChoices,
)
from profile_unlock.models import UserAccessCredit
from profile_unlock.profile_unlock_utilities import check_code_expiry
from rest_framework import generics, serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from users.serializers import (
    GenericErrorResponseSerializer,
    GenericSuccessResponseSerializer,
    JobseekerCompleteDetailSerializer,
)
from utils.pagination import VeetaBasePaginationSet

from .filters import JobApplicationsFilter, JobCardFilter
from .serializers import (
    JobApplicationApproveSerializer,
    JobApplicationCreateSerializer,
    JobApplicationGetDetailSerializer,
    JobApplicationsListSerializer,
    JobCardCreateModifySerializer,
    JobCardSerializer,
    JobCardSlimSerializer,
)

User = get_user_model()

class JobsListView(generics.ListAPIView):
    serializer_class = JobCardSlimSerializer
    pagination_class = VeetaBasePaginationSet
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = JobCardFilter


    def get_queryset(self):
        queryset = JobCard.objects.prefetch_related('responsibilities').filter(is_published=True)
        return queryset


    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        queryset = JobCardFilter(self.request.GET, queryset=qs).qs
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Success',
            'status': 'ok.',
            'status_code': 200,
        })

# TODO Depracate this
class AprroveJobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationApproveSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = JobApplicationsFilter
    http_method_names = ['patch', 'head']


    def get_queryset(self):
        application_id = self.kwargs.get('pk')
        qs = JobApplication.objects.filter(
            id=application_id
        )
        return qs

    def get_object(self):
        application_id = self.kwargs.get('pk')
        application = get_object_or_404(JobApplication, id=application_id)
        return application


    def perform_update(self, serializer):
        serializer.save()


    def update(self, request, *args, **kwargs):
        user = request.user
        if user.u_type != 'Employer':
            return Response({
                'message': 'Operation not allowed.',
                'status_code': 401,
                'status': 'error',
                'error_code': 'unauthorized',
            }, status=status.HTTP_401_UNAUTHORIZED)


        partial = kwargs.pop('partial', False)
        instance = self.get_object() # application instance
        job_card = get_object_or_404(JobCard, id=instance.card.id, company__hiring_manager=user)

        if job_card:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)

            if not 'approved' in serializer.validated_data:
                return Response({
                    'message': 'Approval status is a required field.',
                    'status_code': 400,
                    'status': 'error',
                    'error_code': 'invalid',
                }, status=status.HTTP_400_BAD_REQUEST)

            instance.approved = serializer.data['approved']
            instance.save()

            return Response({
                'message': 'Application approval success.',
                'status_code': 200,
                'status': 'ok',
            }, status=status.HTTP_200_OK)

        return Response({
            'message': "You do not have the permissions to make this changes.",
            'status_code': 401,
            'status': 'error',
            'error_code': 'unauthorized',
        }, status=status.HTTP_401_UNAUTHORIZED)

class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = VeetaBasePaginationSet
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = JobApplicationsFilter
    http_method_names = ['get', 'post', 'delete', 'head']


    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return JobApplication.objects.none()

        if user.logged_in_as == 'Jobseeker':
            applications = JobApplication.objects.filter(user=user)
            return applications

        if user.logged_in_as == 'Employer':
            companies = user.companies.all()
            co_ids = []
            for co in companies:
                co_ids.append(co.id)
            
            applications = JobApplication.objects.filter(card__company__in=co_ids)
            return applications


    def get_object(self):
        application_id = self.kwargs.get('pk')
        application = get_object_or_404(JobApplication, id=application_id)
        return application


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = JobApplicationGetDetailSerializer(instance)
        return Response({
            'data': serializer.data,
            'message': 'Success',
            'status': 'ok',
            'status_code': 200
        })


    def perform_create(self, serializer):
        serializer.save()


    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = JobApplicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if user.u_type != 'General':
            return Response(
                {
                    'error_code': 'unauthorized',
                    'message': "You are not authorized to make ths request.",
                    'status': 'error',
                    'status_code': 400 
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.validated_data['user'].id != user.id:
            return Response(
                {
                    'error_code': 'unauthorized',
                    'message': "You cannot make an application on behalf of someone else.",
                    'status': 'error',
                    'status_code': 401
                },      
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.u_type == 'General' and \
            serializer.validated_data['user'].id == user.id:
            
            # Check if the application exists
            applications = JobApplication.objects.filter(
                user=serializer.validated_data['user'], 
                job_card=serializer.validated_data['job_card']
            )

            if len(applications) > 0:
                # Submission already done
                return Response(
                    {
                        'error_code': 'duplicate',
                        'message': "Looks like you already made your application for this position.",
                        'status': 'error',
                        'status_code': 400
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
    
            if len(applications) == 0:
                # Submission NOT done
                # self.perform_create(serializer)
                application = JobApplication.objects.create(
                    job_card=serializer.validated_data['job_card'],
                    user=serializer.validated_data['user']
                )

                # Retrieve job card
                job_card = JobCard.objects.get(id=serializer.validated_data['job_card'].id)
                applicant = User.objects.get(id=serializer.validated_data['user'].id)
                employer = job_card.company.hiring_manager

                msg = f"{applicant.first_name} {applicant.last_name} made an application for the role of {job_card.role} at {job_card.company.name}."
                
                Notification.objects.create(
                    user=employer,
                    message=msg,
                    tag=NotificationTagChoices.NEW_JOB_APPLICATION,
                    job_application=application
                )

                # Update notifications count for the employer
                employer.unread_notifications = employer.unread_notifications + 1
                employer.save()

                # TODO Send employer an email

                return Response(
                    {
                        'message': 'Application submitted successfully.',
                        'status': 'ok',
                        'status_code': 201,
                    }, status=status.HTTP_201_CREATED
                )

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        queryset = JobApplicationsFilter(self.request.GET, queryset=qs).qs
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = JobApplicationGetDetailSerializer(page, many=True)
            if len(serializer.data) == 0:
                return Response({
                    'data': serializer.data,
                    'message': 'We did not find any application here.',
                    'status': 'not_found',
                    'status_code': 404,
                }, status=status.HTTP_404_NOT_FOUND)

            return self.get_paginated_response(serializer.data)

        serializer = JobApplicationGetDetailSerializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Success.',
            'status': 'ok.',
            'status_code': 200,
        })


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


    def destroy (self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        if instance and instance.user == user:
            # Make deletion
            self.perform_destroy(instance)
        else:
            return Response({
                    'message': "You cannot delete another user's job application.",
                    'status': 'error',
                    'status_code': 401,
                    'error_code': 'unauthorized'
                }, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            'message': "Job application deleted successfully.",
            'status': 'ok',
            'status_code': 200,
        }, status=status.HTTP_200_OK)


    def perform_destroy(self, instance):
        instance.delete()


class JobCardViewSet(viewsets.ViewSet):
    serializer_class = JobCardSerializer
    queryset = JobCard.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


    def create(self, request, *args, **kwargs):
        serializer = JobCardCreateModifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user_co = Company.objects.filter(
            hiring_manager=user,
            id=serializer.validated_data['company'].id
        )
        
        # Check if user is the owner of the co
        if not user_co.exists():
            return Response({
                'status': 'error',
                'error_code': 'unauthorized',
                'status_code': 401,
                'message': 'Looks like you do not won this company.',
            }, status=status.HTTP_401_UNAUTHORIZED)


        if len(serializer.validated_data['responsibilities']) == 0:
            return Response({
                'status': 'error',
                'error_code': 'action_required',
                'status_code': 400,
                'message': 'Please set some responsibilities regarding the job.',
            }, status=status.HTTP_400_BAD_REQUEST)


        if len(serializer.validated_data['responsibilities']) != 0:
            # Check if employer has credits
            user_credits = UserAccessCredit.objects.filter(email=user.email, is_valid=True)

            if len(user_credits) == 0:
                return Response({
                    'error_code': 'permission_denied',
                    'status': 'error',
                    'status_code': 403,
                    'message': 'Looks like you do not have active credits to create a job card.',
                }, status=status.HTTP_403_FORBIDDEN)

            if len(user_credits) > 0:
                # check if it is valid
                for access_credit in user_credits:
                    code_is_expired = check_code_expiry(access_credit)
                    if not code_is_expired:
                        if access_credit.job_cards > 0:
                            access_credit.job_cards = access_credit.job_cards - 1
                            access_credit.save()

                            self.perform_create(serializer)

                            return Response({
                                'data': serializer.data,
                                'status': 'ok',
                                'status_code': 201,
                                'message': 'Job card created successfully.',
                            }, status=status.HTTP_201_CREATED)

                        if access_credit.job_cards == 0:
                            return Response({
                                'error_code': 'permission_denied',
                                'status': 'error',
                                'status_code': 403,
                                'message': 'Looks like you you ran out of job card credits.',
                            }, status=status.HTTP_403_FORBIDDEN)


    def get_object(self):
        card_id = self.kwargs.get('pk')
        try:
            card = JobCard.objects.get(id=card_id)
            return card
        except JobCard.DoesNotExist:
            return JobCard.objects.none()

    def retrieve(self, request, *args, **kwargs):
        card_id = self.kwargs.get('pk')
        try:
            instance = JobCard.objects.prefetch_related('company').get(id=card_id)
            serializer = JobCardSerializer(instance)
            return Response({
                'data': serializer.data,
                'message': 'Success.',
                'status_code': 200,
                'status': 'ok'
            })

        except JobCard.DoesNotExist:
            return Response({
                'message': 'Job card not found.',
                'status_code': 404,
                'status': 'error'
            })


    def update(self, request, *args, **kwargs):
        user = self.request.user
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = JobCardSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance and instance.company.hiring_manager != user:
            return Response({
                    'message': "You cannot modify another user's job card.",
                    'status': 'error',
                    'status_code': 401,
                    'error_code': 'unauthorized'
                }, status=status.HTTP_401_UNAUTHORIZED
            )

        if instance and instance.company.hiring_manager == user:
            if 'responsibilities' in serializer.validated_data and \
                len(serializer.validated_data['responsibilities']) == 0:
                return Response({
                    'message': "Responsibilities cannot be blank.",
                    'status': 'error',
                    'status_code': 400,
                    'error_code': 'invalid'
                }, status=status.HTTP_400_BAD_REQUEST)

            # make update
            self.perform_update(serializer)


        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({
            'data': serializer.data,
            'status': 'ok',
            'status_code': 200,
            'message': 'Job card update success.'
        })

    def perform_update(self, serializer):
        serializer.save()


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


    def perform_destroy(self, instance):
        instance.delete()


    def destroy (self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        if instance and instance.company.hiring_manager == user:
            # make deletion
            self.perform_destroy(instance)
            return Response({
                'message': "Job card deleted successfully.",
                'status': 'ok',
                'status_code': 200,
            }, status=status.HTTP_200_OK)


        if instance and instance.company.hiring_manager != user:
            return Response({
                    'message': "You cannot delete another user's job card.",
                    'status': 'error',
                    'status_code': 401,
                    'error_code': 'unauthorized'
                }, status=status.HTTP_401_UNAUTHORIZED
            )



from django.shortcuts import get_object_or_404

# Bookmarks
from rest_framework.views import APIView
from utils.pagination import VeetaBasePaginationSet
from utils.serializers import JobBookmarkRerieveSerializer

from .models import JobBookmark
from .serializers import JobBookmarkSerializer


class JobseekerBookmarksListView(generics.ListAPIView):
    """
    List all jobseeker job bookmarks
    """
    
    serializer_class = JobBookmarkRerieveSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = VeetaBasePaginationSet

    def get_queryset(self):
        user = self.request.user
        if not user.is_anonymous:
            qs = JobBookmark.objects.filter(user=self.request.user)
            return qs
        return JobBookmark.objects.none()


    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Success',
            'status': 'ok.',
            'status_code': 200,
        })



class JobseekerBookmarksCreateView(generics.CreateAPIView):
    """
    Create a job bookmark
    """
    serializer_class = JobBookmarkSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if user.is_anonymous:
            return Response({
                'message': 'Unauthorized request.',
                'status': 'error',
                'status_code': 400,
                'error_code': 'invalid',
            }, status=status.HTTP_400_BAD_REQUEST)

       
        if user.id == serializer.validated_data['user'].id:
            # Check if the bookmark already exists
            book_marks = JobBookmark.objects.filter(user=user, job_card=serializer.validated_data['job_card'])

            if not book_marks.exists():
                # Create bookmark
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response({
                        'message': 'Bookmark saved successfully.',
                        'status': 'ok',
                        'status_code': 201,
                    }, status=status.HTTP_201_CREATED, headers=headers
                )
            else:
                return Response({
                        'message': 'Bookmark already exists.',
                        'status': 'error',
                        'status_code': 400,
                    }, status=status.HTTP_400_BAD_REQUEST
                )

        return Response({
                'message': 'You cannot create a bookmark for another user.',
                'status': 'error',
                'status_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST
        )


class JobseekerBookmarksDestroyView(generics.DestroyAPIView):
    """
    Delete a single job bookmark
    """

    serializer_class = JobBookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        book_mark_id = self.kwargs.get('id')
        obj = get_object_or_404(JobBookmark, id=book_mark_id)
        return obj


    def perform_destroy(self, instance):
        instance.delete()


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Bookmark deleted.',
            'status': 'ok',
            'status_code': 200
        }, status=status.HTTP_200_OK)


    @extend_schema(
        responses = {
            200: inline_serializer(
                name='BookmarkDeleteSerializer', 
                fields={
                    'message': serializers.CharField(), 
                    'status': serializers.CharField(), 
                    'status_code': serializers.IntegerField()
                }
            ) 
        },
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class JobseekerBookmarksClearView(APIView):
    """
    Delete all jobseeker job bookmarks
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = JobBookmark.objects.filter(user=self.request.user)
        return qs


    @extend_schema(
        responses = {
            200: inline_serializer(
                name='BookmarkClearSerializer', 
                fields={
                    'message': serializers.CharField(), 
                    'status': serializers.CharField(), 
                    'status_code': serializers.IntegerField()
                }
            ) 
        },
    )
    def delete(self, request, *args, **kwargs):
        bookmarks = self.get_queryset()

        if len(bookmarks) == 0:
            return Response({
                'message': 'You have no bookmarks saved.',
                'status': 'error',
                'status_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)

        else:
            for bookmark in bookmarks:
                bookmark.delete()

            return Response({
                'message': 'Bookmarks deleted successfully.',
                'status': 'ok',
                'status_code': 200,
            }, status=status.HTTP_200_OK)
