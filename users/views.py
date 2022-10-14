
import datetime
import email
from curses import meta
from datetime import datetime, timedelta
from pprint import pprint
from secrets import choice

import googlemaps
import h3
from allauth.account import app_settings as allauth_settings
from allauth.account.models import EmailAddress
from dj_rest_auth.app_settings import (
    JWTSerializer,
    JWTSerializerWithExpiration,
    TokenSerializer,
)
from dj_rest_auth.registration.serializers import (
    ResendEmailVerificationSerializer,
    VerifyEmailSerializer,
)
from dj_rest_auth.registration.views import (
    RegisterView,
    ResendEmailVerificationView,
    VerifyEmailView,
)
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    UserDetailsView,
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from establishments.permissions import IsAuthenticatedAndIsEmployer
from payments.models import AccessPackage
from profile_unlock.models import UserAccessCredit
from profile_unlock.profile_unlock_utilities import generate_random_code
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenVerifyView

from users.serializers import (
    CustomUserDetailsSerializer,
    EmployerProfileSerializer,
    JobseekerCompleteDetailSerializer,
)
from users.view_fixes import *
from utils.common import calculate_profile_completeness, get_date_suffix
from utils.models import JobCardZoneMetadata, JobseekerZoneMetadata, h3_resolutions

from . import serializers
from .models import EmployerProfile, JobseekerProfile
from .tasks import send_user_signup_credits

User = get_user_model()
gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

# Custom Views
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': _('Password change success.'),
            'status': _('ok'),
            'status_code': 200,},
            status=status.HTTP_200_OK
        )

class CustomPasswordResetView(PasswordResetView):
    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        email = EmailAddress.objects.filter(**serializer.validated_data).first()
        if email:
            # Send reset email
            # Return the success message with OK HTTP status
            return Response(
                {
                'message': _('Password reset e-mail has been sent.'),
                'status': _('ok'),
                'status_code': 200,                
                },
                status=status.HTTP_200_OK,
            )

        # if email does not exxist
        return Response({
                'message': _('The provided email was not found.'),
                'status': _('error'),
                'status_code': 400,
                'error_code': 'invalid'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class CustomPasswordChangeView(PasswordChangeView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: old_password, new_password1 and new_password2.
    Returns the success/fail message.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': _('New password has been saved.'),
                'status': _('ok'),
                'status_code': 200
            },
            status=status.HTTP_200_OK
        )

class CustomResendEmailVerificationView(ResendEmailVerificationView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        email = EmailAddress.objects.filter(**serializer.validated_data).first()
        if email and not email.verified:
            email.send_confirmation(request)

            return Response(
                {
                    'message': _('Verification email has been sent.'),
                    'status': _('ok'),
                    'status_code': 200,
                },
                status=status.HTTP_200_OK
            )

        # if email does not exxist
        return Response(
            {
                'message': _('The provided email was not found.'),
                'status': _('error'),
                'status_code': 400,
                'error_code': 'invalid'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class CustomVerifyEmailView(VerifyEmailView):
    """
    Use this endpoint to verify an email. Accepts a key and if the key is valid,
    the email is verified and can be used to login.
    """
    def post(self, request, *args, **kwargs):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()

        confirmation.confirm(self.request)

        # Retrieve Sign Up Credits
        user_email = confirmation.email_address.email
        user = User.objects.get(email=user_email)

        if user.u_type == 'General':
            employer_trial_access_credit = UserAccessCredit.objects.get(
                email=user_email,
                tag='sign_up_trial_credits'
            )
            employer_trial_access_credit.is_valid = True
            employer_trial_access_credit.save()

            print('Code Created... Sending email')
            print(employer_trial_access_credit.unlock_code)

            # Send the employer an email with the code
            expire_month = employer_trial_access_credit.expires_on.strftime("%B") # 'December'
            expire_day = employer_trial_access_credit.expires_on.day
            expire_year = employer_trial_access_credit.expires_on.year
            date_suffix = get_date_suffix(employer_trial_access_credit.expires_on)

            mail_context = {
                'unlock_code': employer_trial_access_credit.unlock_code,
                'expire_month': expire_month,
                'expire_day': expire_day,
                'expire_year': expire_year,
                'date_suffix': date_suffix,
                'job_cards': employer_trial_access_credit.job_cards,
                'total_unlocks': employer_trial_access_credit.total_unlocks,
                'site_name': 'Veeta UK'
            }

            print(mail_context)

            # Send Email to User via Celery
            send_user_signup_credits \
                .delay(employer_trial_access_credit.email, mail_context)

            return Response(
                {
                    'data': {'email': user_email},
                    'message': _('Email verify success.'),
                    'status': _('ok'),
                    'status_code': 200,
                },
                status=status.HTTP_200_OK
            )


@extend_schema(parameters=[OpenApiParameter("id", int, OpenApiParameter.PATH)])
class CustomUserDetailsViewSet(viewsets.ViewSet):
    """
    Reads and updates UserModel fields Accepts GET, PUT, PATCH methods.
    Returns UserModel fields.
    """
    http_method_names = ['patch', 'head']
    serializer_class = CustomUserDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


    def get_object(self):
        user_id = int(self.kwargs.get('id'))
        try:
            user = User.objects.get(id=user_id)
            # from django.db.models import Prefetch
            # user = User.objects.prefetch_related(
            #     Prefetch(
            #         'access_credits',
            #         queryset=UserAccessCredit.objects.filter(is_valid=True),
            #         to_attr='filtered_access_credits'
            #     ),
            # ).get(id=user_id) 
            return user
        except User.DoesNotExist:
            return


    def retrieve(self, request, *args, **kwargs):
        user = request.user
        user_id = self.kwargs.get('pk')
        instance = self.get_object()

        if not instance:
            return Response({
                'message': 'User not found.',
                'status': 'error',
                'error_code': 'not_found',
                'status_code': 404,
            }, status=status.HTTP_404_NOT_FOUND)  


        serializer = CustomUserDetailsSerializer(instance)

        if instance.id != int(user_id) or user.id != int(user_id):
            return Response({
                'message': 'You are not authorized to make this request.',
                'status': 'error',
                'error_code': 'permission_denied',
                'status_code': 403,
            }, status=status.HTTP_403_FORBIDDEN)  


        return Response({
            'data':serializer.data,
            'message': "Success.",
            'status': 'ok',
            "status_code": 200
        })

    # @extend_schema(
    #     parameters=[
    #         OpenApiParameter("pk", OpenApiTypes.INT, OpenApiParameter.PATH), # path variable was overridden
    #     ],
    # )
    def update(self, request, *args, **kwargs):
        user = self.request.user
        user_id = self.kwargs.get('id')
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if int(user_id) != user.id or instance.id != user.id:
            return Response({
                'message': 'You are not authorized to make this request.',
                'status': 'error',
                'error_code': 'permission_denied',
                'status_code': 403,
            }, status=status.HTTP_403_FORBIDDEN)  

        if int(user_id) == user.id and instance.id == user.id:
            serializer = CustomUserDetailsSerializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)

            completeness = calculate_profile_completeness(user, user.jobseeker_profile)
            user.jobseeker_profile.profile_completeness = completeness
            user.jobseeker_profile.save()
            # TODO Delete this
            print("Completeness is: " + str(user.jobseeker_profile.profile_completeness))

            self.perform_update(serializer)

        
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({
            'data': serializer.data,
            'status': 'ok',
            'status_code': 200,
            'message': 'User details updated.'
        })

    def perform_update(self, serializer):
        serializer.save()


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class CustomRegisterView(RegisterView):
    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {
                'data': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                },
                'message': _('Verification e-mail sent.'),
                'status': 'ok',
                'status_code': 201,
            }

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
            }
            return JWTSerializer(data, context=self.get_serializer_context()).data
        elif getattr(settings, 'REST_SESSION_LOGIN', False):
            return None
        else:
            return TokenSerializer(user.auth_token, context=self.get_serializer_context()).data


class CustomLoginView(LoginView):
    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):

            if getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False):
                response_serializer = JWTSerializerWithExpiration
            else:
                response_serializer = serializers.LoginSuccessSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer


    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_simplejwt.settings import api_settings as jwt_settings
            access_token_expiration = (timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
            refresh_token_expiration = (timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME)
            return_expiration_times = getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False)

            # Save logged in as
            user = self.request.user
            if not user.is_anonymous and \
                user.u_type == 'General':
                data = self.request.data            
                user.logged_in_as = data['log_in_as']
                user.save()
                print(f"Logged is as {data['log_in_as']}")


            data = {
                'status': 'ok',
                'status_code': 200,
                'message': 'Successfully logged in.',
                'data': {
                    'access_token': self.access_token,
                    'refresh_token': self.refresh_token,
                    'user': self.user,
                }
            }

            if return_expiration_times:
                data['access_token_expiration'] = access_token_expiration
                data['refresh_token_expiration'] = refresh_token_expiration

            serializer = serializer_class(
                instance=data,
                context=self.get_serializer_context(),
            )
        elif self.token:
            serializer = serializer_class(
                instance=self.token,
                context=self.get_serializer_context(),
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from dj_rest_auth.jwt_auth import set_jwt_cookies
            set_jwt_cookies(response, self.access_token, self.refresh_token)

        return response

class CustomLogoutView(LogoutView):
    """
    Calls Django logout method and deletes the Token object assigned to the current User object.
    Accepts refresh as an optional payload.

    If no refresh is supplied in the request body, it falls back to the refresh cookie.
    """
    serializer_class = serializers.LogoutSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')


    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response(
            {
                'message': _('Successfully logged out.'),
                'status': 'ok',
                'status_code': 200,
            },
            status=status.HTTP_200_OK,
        )

        if getattr(settings, 'REST_USE_JWT', False):
            # NOTE: this import occurs here rather than at the top level
            # because JWT support is optional, and if `REST_USE_JWT` isn't
            # True we shouldn't need the dependency
            from dj_rest_auth.jwt_auth import unset_jwt_cookies
            from rest_framework_simplejwt.exceptions import TokenError
            from rest_framework_simplejwt.tokens import RefreshToken
            cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)

            unset_jwt_cookies(response)

            if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
                # Add refresh token to blacklist
                try:
                    tokens = {}
                    if 'refresh' in request.data:
                        print('In Body')
                        tokens['refresh'] = request.data['refresh']
    
                    if not 'refresh' in request.data and \
                        'refresh' in request.COOKIES:
                        print('In Cookie')
                        tokens['refresh'] = request.COOKIES['refresh']

                    token = RefreshToken(tokens['refresh'])
                    token.blacklist()
                except KeyError:
                    response.data = {
                        'status': 'error',
                        'status_code': 401,
                        'error_code': 'invalid',
                        'message': _('Refresh token was not included in the request.'),
                    }
                    response.status_code =status.HTTP_401_UNAUTHORIZED
                except (TokenError, AttributeError, TypeError) as error:
                    if hasattr(error, 'args'):
                        if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                            response.data = {
                                'status': 'error',
                                'status_code': 401,
                                'error_code': 'invalid',
                                'message': _(f'{error.args[0]}.'),
                            }
                            response.status_code = status.HTTP_401_UNAUTHORIZED
                        else:
                            response.data = {
                                'status': 'error',
                                'status_code': 500,
                                'error_code': 'invalid',
                                'message': _('Something went wrong logging you out.'),
                            }
                            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

                    else:
                        response.data = {
                            'message': _('An error has occurred.'),
                            'status': 'error',
                            'status_code': 500,
                            'error_code': 'invalid',
                        }
                        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            elif not cookie_name:
                message = _(
                    'Neither cookies or blacklist are enabled, so the token '
                    'has not been deleted server side. Please make sure the token is deleted client side.',
                )
                response.data = {'detail': message}
                response.status_code = status.HTTP_200_OK
        return response

class JobseekerProfileViewSet(viewsets.ViewSet):
    """
    Returns and updates the profile related to the Jobseeker user type. 
    The {id} represesnts the User ID and is a required field.
    """
    queryset = JobseekerProfile.objects.all()
    serializer_class = serializers.JobseekerProfileModSerializer


    def get_object(self):
        user_id = self.kwargs.get('pk')
        profile = get_object_or_404(JobseekerProfile, user=user_id)
        return profile

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        user_id = self.kwargs.get('pk')
        instance = self.get_object()
        serializer = serializers.JobseekerIncompleteDetailSerializer(instance)

        # Show all the info if the user is the owner of the profile
        if not user.is_anonymous and \
            user.u_type == 'General' and \
            user.jobseeker_profile.user.id == int(user_id):
            serializer = serializers.JobseekerLoggedInProfileSerializer(instance)

        return Response(
          {
            'data': serializer.data,
            'message': 'Success.',
            'status_code': 200,
            'status': 'ok'
          }, status=status.HTTP_200_OK
        )


    def update(self, request, *args, **kwargs):
        user = self.request.user
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if user.is_anonymous:
            return Response({
                'message': 'Authentication credentials missing.',
                'status': 'error',
                'error_code': 'permission_denied',
                'status_code': 403,
            }, status=status.HTTP_403_FORBIDDEN)   


        if user.u_type != 'General':
            return Response({
                'message': 'You do not have the permissions to make this request.',
                'status': 'error',
                'error_code': 'permission_denied',
                'status_code': 403,
            }, status=status.HTTP_403_FORBIDDEN)   


        if instance.user.id != user.id:
            return Response({
                'message': 'You are not authorized to make this request.',
                'status': 'error',
                'error_code': 'permission_denied',
                'status_code': 403,
            }, status=status.HTTP_403_FORBIDDEN)             

        if instance.user.id == user.id:
            serializer = serializers.JobseekerProfileModSerializer(
                instance, 
                data=request.data, 
                partial=partial
            )
            serializer.is_valid(raise_exception=True)

            if 'location' in serializer.validated_data:
                # Populate locations
                saved_loc = instance.location
                new_location = serializer.validated_data['location']

                if saved_loc != new_location:
                    # Make update
                    print('Location Update from the view...')
                    try:
                        geocode_result = gmaps.geocode(new_location)
                        lat = geocode_result[0]['geometry']['location']['lat']
                        lng = geocode_result[0]['geometry']['location']['lng']

                        try:
                            metadata = JobseekerZoneMetadata.objects.get(profile=instance)
                            metadata.zone_one=h3.geo_to_h3(lat, lng, h3_resolutions['one'])
                            metadata.zone_two=h3.geo_to_h3(lat, lng, h3_resolutions['two'])
                            metadata.zone_three=h3.geo_to_h3(lat, lng, h3_resolutions['three'])
                            metadata.zone_four=h3.geo_to_h3(lat, lng, h3_resolutions['four'])
                            metadata.zone_five=h3.geo_to_h3(lat, lng, h3_resolutions['five'])
                            metadata.zone_six=h3.geo_to_h3(lat, lng, h3_resolutions['six'])
                            metadata.zone_seven=h3.geo_to_h3(lat, lng, h3_resolutions['seven'])
                            metadata.save()
                        except JobseekerZoneMetadata.DoesNotExist:
                            JobseekerZoneMetadata.objects.create(
                                profile=instance,
                                zone_one=h3.geo_to_h3(lat, lng, h3_resolutions['one']),
                                zone_two=h3.geo_to_h3(lat, lng, h3_resolutions['two']),
                                zone_three=h3.geo_to_h3(lat, lng, h3_resolutions['three']),
                                zone_four=h3.geo_to_h3(lat, lng, h3_resolutions['four']),
                                zone_five=h3.geo_to_h3(lat, lng, h3_resolutions['five']),
                                zone_six=h3.geo_to_h3(lat, lng, h3_resolutions['six']),
                                zone_seven=h3.geo_to_h3(lat, lng, h3_resolutions['seven']),
                            )
                    except:
                        pass

            # Update the profile
            self.perform_update(serializer)

            # Update profile completeness
            completeness = calculate_profile_completeness(user, user.jobseeker_profile)
            user.jobseeker_profile.profile_completeness = completeness
            user.jobseeker_profile.save()
            print("Completeness is: " + str(user.jobseeker_profile.profile_completeness))

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # return updated data
        profile = JobseekerProfile.objects.get(id=instance.id)
        serialized_profile = serializers.JobseekerProfileModSerializer(profile)

        return Response(
            {
                'data': serialized_profile.data,
                'message': 'Profile update success.',
                'status': 'ok',
                'status_code': 200
            }, status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class EmployerProfileViewSet(viewsets.ViewSet):
    """
    Returns and updates the profile related to the Employer user type. 
    The {id} represesnts the User ID and is a required field.
    """
    queryset = EmployerProfile.objects.all()
    http_method_names = ['get', 'head']
    serializer_class = serializers.EmployerProfileSerializer
    permission_classes = [IsAuthenticatedAndIsEmployer]

    def get_object(self):
        try:
            user_id = int(self.kwargs.get('pk'))
            # profile = EmployerProfile.objects.prefetch_related('user__access_code') \
            #     .get(user=int(user_id))

            profile = EmployerProfile.objects.get(user=user_id)
            return profile
        except EmployerProfile.DoesNotExist:
            return EmployerProfile.objects.none()


    def retrieve(self, request, *args, **kwargs):
        user = request.user
        user_id = self.kwargs.get('pk')

        if user.employer_profile.user.id != int(user_id) or user.id != int(user_id):
            return Response({
                'message': 'You are not authorized to make this request.',
                'status': 'permission_denied',
                'status_code': 403,
            }, status=status.HTTP_403_FORBIDDEN)   

        # Only show employer profile to owner
        if user.u_type == 'General' and \
            user.employer_profile.user.id == int(user_id):
            instance = self.get_object()
            serializer = serializers.EmployerProfileSerializer(instance)

            return Response({
                'data': serializer.data,
                'message': 'Success.',
                'status': 'ok',
                'status_code': 200,
            })


from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenVerifyView


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        res = {
            'message': 'Token is valid.',
            'status': 'ok',
            'status_code': 200
        }
        return Response(res, status=status.HTTP_200_OK)


from rest_framework import serializers as rserializers
from rest_framework.views import APIView


class LoginStateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class =  serializers.LoginStateSerializer

    @extend_schema(
        responses = {
            200: inline_serializer(
                name='LoginStateSerializer', 
                fields={
                    'message': rserializers.CharField(), 
                    'status': rserializers.CharField(), 
                    'status_code': rserializers.IntegerField()
                }
            ) 
        },
    )

    def patch(self, request, *args, **kwargs):
        user = request.user 
        serializer = serializers.LoginStateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.logged_in_as = serializer.validated_data['log_in_as']
        user.save()

        jobseeker_profile = JobseekerCompleteDetailSerializer(user.jobseeker_profile)
        employer_profile = EmployerProfileSerializer(user.employer_profile)

        data = jobseeker_profile.data
        if serializer.validated_data['log_in_as'] == 'Employer':
            data = employer_profile.data

        return Response({
            'data': data,
            'message': f"Successfully logged in as {serializer.validated_data['log_in_as'].lower()}.",
            'status': 'ok',
            'status_code': 200
        }, status=status.HTTP_200_OK)


class DeleteUserAccountView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def get_object(self):
        user = User.objects.get(id=self.request.user.id)
        return user

    def get_queryset(self):
        return User.objects.none()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Delete all bought access codes
        user_credits = UserAccessCredit.objects.filter(
            email=instance.email
        )

        for cred in user_credits:
            cred.delete()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
