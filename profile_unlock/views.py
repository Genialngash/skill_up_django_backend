from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.response import Response
from users.models import JobseekerProfile
from users.serializers import JobseekerCompleteDetailSerializer
from utils.pagination import VeetaBasePaginationSet

from profile_unlock.models import UnlockedProfile

from .models import UnlockedProfile, UserAccessCredit
from .profile_unlock_utilities import check_code_expiry
from .serializers import UnlockedProfileSerializer, UnlockProfileSerializer


class UnlockProfileView(views.APIView):
    serializer_class = UnlockProfileSerializer

    def post(self, request, format=None):
        serializer = UnlockProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jobseeker = serializer.validated_data['jobseeker']

        # handle anonymous unlocks
        if request.user.is_anonymous:
            try:
                access_credit = UserAccessCredit.objects.get(
                    unlock_code=request.data['unlock_code']
                )

                if not access_credit.is_valid:
                    return Response({
                        'message': 'Looks like your code is invalid.',
                        'status': 'error',
                        'status_code': 400,
                        'error_code': 'invalid'
                    }, status=status.HTTP_400_BAD_REQUEST)


                total_unlocks = access_credit.total_unlocks

                # check if there are any unlock credits
                if total_unlocks == 0:
                    return Response({
                        'message': 'Looks like you have exhausted your unlock codes.',
                        'status': 'error',
                        'status_code': 400,
                        'error_code': 'zero_codes_left'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # check if code has expired
                code_is_expired = check_code_expiry(access_credit)

                if code_is_expired:
                    access_credit.is_valid = False
                    access_credit.save()

                    return Response({
                        'message': 'Looks like your access credits have expired.',
                        'status': 'error',
                        'status_code': 400,
                        'error_code': 'expired_code'
                    }, status=status.HTTP_400_BAD_REQUEST)

                if not code_is_expired:
                    try:
                        profile = JobseekerProfile.objects.get(id=jobseeker)
                        serializer = JobseekerCompleteDetailSerializer(profile)
                    except JobseekerProfile.DoesNotExist:
                        return Response({
                                'message': 'Looks like the profile you are looking for does not exist.',
                                'status': 'error',
                                'status_code': 400,
                                'error_code': 'not_found'
                            }, status=status.HTTP_400_BAD_REQUEST)


                    # check if the contact has already been unlocked
                    try:
                        unlocked_profile = UnlockedProfile.objects.get(
                            profile=jobseeker,
                            access_credit=access_credit,
                        )

                        if unlocked_profile:
                            return Response({
                                'data': serializer.data,
                                'message': 'Looks like you already unlocked this profile.',
                                'status': 'ok',
                                'status_code': 200,
                            }, status=status.HTTP_200_OK)
                    
                    except UnlockedProfile.DoesNotExist:
                        # deduct the unlocks
                        access_credit.total_unlocks = total_unlocks - 1
                        access_credit.save()
                        UnlockedProfile.objects.create(profile=profile, access_credit=access_credit,)

                        return Response({
                            'data': serializer.data,
                            'message': 'Successfully fetched profile.',
                            'status': 'ok',
                            'status_code': 200,
                        }, status=status.HTTP_200_OK)

            except UserAccessCredit.DoesNotExist:
                return Response({
                    'message': 'Invalid. Code does not exist.',
                    'status': 'error',
                    'status_code': 400,
                    'error_code': 'invalid_code'
                }, status=status.HTTP_400_BAD_REQUEST)


        # handle authenticated user unlock requests
        if not request.user.is_anonymous and request.user.u_type == 'General':
            try:
                access_credit = UserAccessCredit.objects.get(
                    unlock_code=request.data['unlock_code'],
                    is_valid=True
                )
                total_unlocks = access_credit.total_unlocks

                if total_unlocks == 0:
                    return Response({
                        'message': 'Looks like you have exhausted your unlock codes.',
                        'status': 'error',
                        'status_code': 400,
                        'error_code': 'zero_codes_left'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # check if code has expired
                code_is_expired = check_code_expiry(access_credit)

                if code_is_expired:
                    access_credit.is_valid = False
                    access_credit.save()

                    return Response({
                        'message': 'Looks like your unlock code has already expired.',
                        'status': 'error',
                        'status_code': 400,
                        'error_code': 'expired_code'
                    }, status=status.HTTP_400_BAD_REQUEST)

                if not code_is_expired:
                    try:
                        profile = JobseekerProfile.objects.get(id=jobseeker)
                        serializer = JobseekerCompleteDetailSerializer(profile)
                    except JobseekerProfile.DoesNotExist:
                        return Response({
                                'message': 'Looks like the profile you are looking for does not exist.',
                                'status': 'error',
                                'status_code': 400,
                                'error_code': 'not_found'
                            }, status=status.HTTP_400_BAD_REQUEST)


                    # check if the contact has already been unlocked
                    try:
                        unlocked_profile = UnlockedProfile.objects.get(
                            profile=jobseeker,
                            access_credit=access_credit,
                        )

                        if unlocked_profile:
                            return Response({
                                'data': serializer.data,
                                'message': 'Looks like you already unlocked this profile.',
                                'status': 'invalid',
                                'status_code': 400,
                            }, status=status.HTTP_200_OK)
                    
                    except UnlockedProfile.DoesNotExist:
                        # deduct the unlocks
                        access_credit.total_unlocks = total_unlocks - 1
                        access_credit.save()
                        UnlockedProfile.objects.create(profile=profile, access_credit=access_credit,)

                        return Response({
                            'data': serializer.data,
                            'message': 'Successfully fetched profile.',
                            'status': 'ok',
                            'status_code': 200,
                        }, status=status.HTTP_200_OK)

            except UserAccessCredit.DoesNotExist:
                return Response({
                    'message': 'Invalid. Code does not exist.',
                    'status': 'error',
                    'status_code': 400,
                    'error_code': 'invalid_code'
                }, status=status.HTTP_400_BAD_REQUEST)


class UnlockedProfilesListView(generics.ListAPIView):
    pagination_class = VeetaBasePaginationSet
    serializer_class = UnlockedProfileSerializer
    queryset = UnlockedProfile.objects.none()


    def get_queryset(self):
        unlock_code = self.kwargs['unlock_code']
        access_credit = get_object_or_404(UserAccessCredit, unlock_code=unlock_code)
        qs = UnlockedProfile.objects.filter(
            access_credit=access_credit.id
        )
        return qs


    def get(self, request, *args, **kwargs):
        unlock_code = self.kwargs.get('unlock_code', None)

        try:
            access_credit = UserAccessCredit.objects.get(unlock_code=unlock_code)
            code_is_expired = check_code_expiry(access_credit)        

            if not code_is_expired:
                unlocked_profiles = UnlockedProfile.objects.filter(
                    access_credit=access_credit.id
                )

                page = self.paginate_queryset(unlocked_profiles)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = UnlockedProfile(unlocked_profiles, many=True)
                return Response({
                    'data': serializer.data,
                    'message': 'Success.',
                    'status': 'ok',
                    'status_code': 200,
                }, status=status.HTTP_200_OK)

            if code_is_expired:
                access_credit.is_valid = False
                access_credit.save()

                return Response({
                    'message': 'Looks like your unlock code has already expired.',
                    'status': 'error',
                    'status_code': 400,
                    'error_code': 'expired_code'
                }, status=status.HTTP_400_BAD_REQUEST)

        except UserAccessCredit.DoesNotExist:
            return Response({
                'message': 'Invalid. Code does not exist.',
                'status': 'error',
                'status_code': 400,
                'error_code': 'invalid_code'
            }, status=status.HTTP_400_BAD_REQUEST)

