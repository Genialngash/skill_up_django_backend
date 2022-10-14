from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from establishments.models import Employee
from establishments.permissions import IsAuthenticatedAndIsEmployer
from rest_framework import generics, status
from rest_framework.response import Response

from ratings.models import JobseekerRating

User = get_user_model()

from .serializers import JobseekerRatingSerializer


class JobseekerRatingView(generics.CreateAPIView):
    """
    Saves a jobseeker rating. Only employers can rate jobskeekers on condition that
    they appear in their employees list. Also, an employer can only rate a jobseeker once.
    """
    serializer_class = JobseekerRatingSerializer
    permission_classes = [IsAuthenticatedAndIsEmployer]

    def create(self, request, *args, **kwargs):
        user = request.user
        hiring_manager = get_object_or_404(User, id=user.id, u_type='Employer')
        companies = hiring_manager.companies

        company_ids = []
        for co in companies:
            company_ids.append(co.id)

        company_employees = Employee.objects.filter(company__in=company_ids)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        for employee in company_employees:
            if employee.user.id == serializer.validated_data['jobseeker'].id and \
                user.id == serializer.validated_data['employer'].id:
                saved_ratings = JobseekerRating.objects.filter(
                    employer=hiring_manager.id,
                    jobseeker=serializer.validated_data['jobseeker'].id
                )

                if not saved_ratings.exists():
                    # Rate the worker
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    return Response({
                            'message': 'User rating saved successfully.',
                            'status': 'ok',
                            'status_code': 201,
                        }, status=status.HTTP_201_CREATED, headers=headers
                    )

                if saved_ratings.exists():
                    return Response({
                            'message': 'You can only rate a user once.',
                            'status': 'error',
                            'status_code': 403,
                            'error_code': 'permission_denied'
                        }, status=status.HTTP_403_FORBIDDEN
                    )

        return Response({
            'message': 'You can only rate people you have worked with.',
            'status': 'error',
            'status_code': 400,
            'error_code': 'invalid',
        }, status=status.HTTP_400_BAD_REQUEST)
