from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from .serializers import (
    ConfirmVerificationErrorResponseSerializer,
    ConfirmVerificationSerializer,
    ConfirmVerificationSuccessResponseSerializer,
    ContactVerificationCodeSerializer,
    GetVerificationCodeErrorResponseSerializer,
    GetVerificationCodeSuccessResponseSerializer,
)


class FixContactVerificationCodeView(OpenApiViewExtension):
    target_class = 'contact.views.GetContactVerificationCode'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = ContactVerificationCodeSerializer
            @extend_schema(
                request=ContactVerificationCodeSerializer,
                responses={
                    200: OpenApiResponse(
                        response=GetVerificationCodeSuccessResponseSerializer,
                        description='Get verification code success.' 
                    ),
                    400: OpenApiResponse(
                        response=GetVerificationCodeErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).\
                            Errors messages are set for each specific field if any.'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed

class FixConfirmVerificationCodeView(OpenApiViewExtension):
    target_class = 'contact.views.ConfirmContactVerificationView'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = ConfirmVerificationSerializer
            @extend_schema(
                request=ConfirmVerificationSerializer,
                responses={
                    200: OpenApiResponse(
                        response=ConfirmVerificationSuccessResponseSerializer,
                        description='Contact verification success.' 
                    ),
                    400: OpenApiResponse(
                        response=ConfirmVerificationErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).\
                            Errors messages are set for each specific field if any.'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed


class GetContactVerificationCode(views.APIView):
    serializer_class = ContactVerificationCodeSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def post(self, request, format=None):
        user = request.user

        serializer = ContactVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if user.phone_number is None:
            user.verified = False
            user.phone_number = serializer.data['phone_number']
            user.save()

        if user.phone_number is not None:
            user.verified = False
            user.phone_number = serializer.data['phone_number']
            user.save()

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        try:
            verification_check = client.verify \
                .services(settings.TWILIO_VERIFY_SERVICE_ID) \
                .verifications \
                .create(
                    to=serializer.data['phone_number'], 
                    channel=serializer.data['channel']
                )
            return Response({
                    'status': 'ok',
                    'message': 
                        f'Verification code request successful. Phone number state is currently {verification_check.status}.',
                    'status_code': 200,
                },
                status=status.HTTP_200_OK
            )
        except TwilioRestException as e:
            return Response(
                {
                    'message': e.msg,
                    'status_code': e.code,
                    'status': 'error',
                }
            )

class ConfirmContactVerificationView(views.APIView):
    """
    Confirms the phone number by matching the verfication code with the one
    registered by Twilio.
    """
    serializer_class = ConfirmVerificationSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def post(self, request, format=None):
        user = request.user
        serializer = ConfirmVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        if user.phone_number is None:
            user.contact_is_verified = False
            user.save()

            return Response(
                {
                    'error_code': 'invalid',
                    'status': 'error',
                    'status_code': 400,
                    'message': 'No contact was found for your account.',
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.phone_number is not None:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            try:
                verification_check = client.verify \
                    .services(settings.TWILIO_VERIFY_SERVICE_ID) \
                    .verification_checks \
                    .create(
                        to=str(user.phone_number), 
                        code=serializer.data['verification_code'])

                if verification_check.status == 'approved':
                    user.contact_is_verified = True
                    user.save()

                    return Response({
                        'message': f'Contact status is {verification_check.status}',
                        'status': verification_check.status,
                        'status_code': 200,

                    }, status=status.HTTP_200_OK)

                if verification_check.status != 'approved':
                    user.contact_is_verified = False
                    user.save()

                    return Response({
                        'error_code': 'invalid',
                        'status': 'error',
                        'status_code': 400,
                        'message': f'Contact verification failure. Phone number state is currently {verification_check.status}.',
                    }, status=status.HTTP_400_BAD_REQUEST)            
            except TwilioRestException as e:
                if 'unable to create record' in e.msg.lower():
                    msg = "Unable to create record. The requested resource was not found."
                else: 
                    msg = "Something went wrong."

                return Response(
                    {
                        'message': msg,
                        'status_code': e.code,
                        'status': 'error',
                        'error_code': 'unkown',
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response({
                'error_code': 'invalid',
                'status': 'error',
                'status_code': 400,
                'message': 'No contact was found for your account.',
            }, status=status.HTTP_400_BAD_REQUEST
        )
