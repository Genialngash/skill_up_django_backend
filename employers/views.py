from establishments.models import Company, JobApplication, JobCard
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.pagination import VeetaBasePaginationSet

from jobs.serializers import JobApplicationsListSerializer, JobCardSerializer

from .serializers import JobOfferCreateSerializer


class EmployerListAllJobCardsView(generics.ListAPIView):
    """
    List all jobcards posted by an employer.
    """
    serializer_class = JobCardSerializer
    pagination_class = VeetaBasePaginationSet
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return JobCard.objects.none()

        companies = Company.objects.filter(hiring_manager=user)
        co_ids = []
        for co in companies:
            co_ids.append(co.id)

        job_cards = JobCard.objects.prefetch_related(
            'responsibilities',
            'company'
        ).filter(company__in=co_ids)

        return job_cards


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'data': serializer.data,
            'message': 'Success.',
            'status_code': 200,
            'status': 'ok'
        })


class EmployerJobCardListView(generics.ListAPIView):
    serializer_class = JobCardSerializer
    pagination_class = VeetaBasePaginationSet
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        if company_id:
            qs = JobCard.objects.prefetch_related(
                'responsibilities',
                'company'
            ).filter(company=company_id)
            return qs

        return JobCard.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Success.',
            'status_code': 200,
            'status': 'ok'
        })



class EmployerJobApplicationsListView(generics.ListAPIView):
    serializer_class = JobApplicationsListSerializer
    pagination_class = VeetaBasePaginationSet
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        job_card_id = self.kwargs.get('job_card_id')

        if job_card_id:
            qs = JobApplication.objects.filter(job_card=job_card_id)
            return qs

        return JobApplication.objects.none()


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Success.',
            'status_code': 200,
            'status': 'ok'
        })


from django.contrib.auth import get_user_model
from notifications.models import Notification, NotificationTagChoices

User = get_user_model()

class JobOfferViewSet(viewsets.ViewSet):
    serializer_class = JobOfferCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = JobOfferCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Create a notification for the jobseeker
        job_card = JobCard.objects.get(id=serializer.validated_data['job_card'].id)
        applicant = User.objects.get(id=serializer.validated_data['applicant'].id)
        msg = f"New job offer from {job_card.company.name}."

        Notification.objects.create(
            user=applicant,
            message=msg,
            tag=NotificationTagChoices.NEW_JOB_OFFER,
        )

        # TODO Send the jobseeker an email

        return Response({
            'message': 'Job offer created.',
            'status_code': 201,
            'status': 'ok'
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()



# {
#   "data": {
#     "current_page": 1,
#     "previous_page": None,
#     "next_page": None,
#     "count": 6,
#     "results": [
#       {
#         "id": 6,
#         "user": {
#           "id": 4,
#           "first_name": "Melissa",
#           "last_name": "Jones",
#           "avatar": "http://localhost:8000/media/default.jpg",
#           "email": "melissa.jones@yopmail.com",
#           "contact_is_verified": true,
#           "phone_number": "+16135550120",
#           "profile": {
#             "id": 4,
#             "profession": "Merchandiser, retail",
#             "total_ratings": 12,
#             "avg_rating": "1.00",
#             "hourly_rate": 45
#           }
#         },
#         "job_card": {
#           "id": 10,
#           "role": "Air broker",
#           "company": {
#             "name": "Patel PLC"
#           }
#         }
#       },
#     }
# }
