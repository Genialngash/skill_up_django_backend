from dj_rest_auth.registration.serializers import (
    ResendEmailVerificationSerializer,
    VerifyEmailSerializer,
)
from dj_rest_auth.serializers import (
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
)
from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)

from . import serializers


# Docs Fixes
class FixLoginView(OpenApiViewExtension):
    target_class = 'users.views.CustomLoginView'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = serializers.CustomLoginSerializer
            @extend_schema(
                request=serializers.CustomLoginSerializer,
                responses={
                     200: OpenApiResponse(
                        response=serializers.LoginSuccessSerializer,
                        description='User login success.' 
                    ),
                    400: OpenApiResponse(
                        response=serializers.GenericErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).\
                            Errors messages are set for each specific field if any.'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed

class FixRegisterView(OpenApiViewExtension):
    target_class = 'users.views.CustomRegisterView'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = serializers.CustomRegisterSerializer
            @extend_schema(
                request=serializers.CustomRegisterSerializer,
                responses={
                    201: OpenApiResponse(
                        response=serializers.RegisterSuccessResponseSerializer,
                        description='User created successfully.' 
                    ),
                    400: OpenApiResponse(
                        response=serializers.GenericErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed

class FixVerifyEmailView(OpenApiViewExtension):
    target_class = 'users.views.CustomVerifyEmailView'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = VerifyEmailSerializer
            @extend_schema(
                request=VerifyEmailSerializer,
                responses={
                    200: OpenApiResponse(
                        response=serializers.VerifyEmailSuccessResponseSerializer,
                        description='Email verified successfully.' 
                    ),
                    400: OpenApiResponse(
                        response=serializers.GenericErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed

class FixResendVerificationEmailView(OpenApiViewExtension):
    target_class = 'users.views.CustomResendEmailVerificationView'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = ResendEmailVerificationSerializer
            @extend_schema(
                request=ResendEmailVerificationSerializer,
                responses={
                    200: OpenApiResponse(
                        response=serializers.GenericSuccessResponseSerializer,
                        description='Resend verification success.' 
                    ),
                    400: OpenApiResponse(
                        response=serializers.GenericErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed

class FixLogoutView(OpenApiViewExtension):
    target_class = 'users.views.CustomLogoutView'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = serializers.LogoutSerializer
            @extend_schema(
                request=serializers.LogoutSerializer,
                responses={
                    200: OpenApiResponse(
                        response=serializers.GenericSuccessResponseSerializer,
                        description='Logout success.' 
                    ),
                    400: OpenApiResponse(
                        response=serializers.GenericErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed

class FixPasswordChangeView(OpenApiViewExtension):
    target_class = 'users.views.CustomPasswordChangeView'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = PasswordChangeSerializer
            @extend_schema(
                request=PasswordChangeSerializer,
                responses={
                    200: OpenApiResponse(
                        response=serializers.GenericSuccessResponseSerializer,
                        description='Password change success.' 
                    ),
                    400: OpenApiResponse(
                        response=serializers.GenericErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed


class FixPasswordResetView(OpenApiViewExtension):
    target_class = 'users.views.CustomPasswordResetView'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = serializers.PasswordResetSerializer
            @extend_schema(
                request=serializers.PasswordResetSerializer,
                responses={
                    200: OpenApiResponse(
                        response=serializers.GenericSuccessResponseSerializer,
                        description='Password reset success.' 
                    ),
                    400: OpenApiResponse(
                        response=serializers.GenericErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed

class FixPasswordResetConfirmView(OpenApiViewExtension):
    target_class = 'users.views.CustomPasswordResetConfirmView'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = PasswordResetConfirmSerializer
            @extend_schema(
                request=PasswordResetConfirmSerializer,
                responses={
                    200: OpenApiResponse(
                        response=serializers.GenericSuccessResponseSerializer,
                        description='Password reset confirm success.' 
                    ),
                    400: OpenApiResponse(
                        response=serializers.GenericErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed


class FixCustomUserDetailsViewSet(OpenApiViewExtension):
    target_class = 'users.views.CustomUserDetailsViewSet'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = serializers.CustomUserDetailsSerializer
            @extend_schema(
                request=serializers.CustomUserDetailsSerializer,
                responses={
                     200: OpenApiResponse(
                        response=serializers.CustomUserDetailsSerializer,
                        description='Success fetching common user details.' 
                    ),
                    400: OpenApiResponse(
                        response=serializers.GenericErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).\
                            Errors messages are set for each specific field if any.'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed


class FixLoginStateView(OpenApiViewExtension):
    target_class = 'users.views.LoginStateView'

    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = serializers.LoginStateSerializer
            @extend_schema(
                request=serializers.LoginStateSerializer,
                responses={
                     200: OpenApiResponse(
                        response=serializers.GenericSuccessResponseSerializer,
                        description='Success fetching common user details.' 
                    ),
                    400: OpenApiResponse(
                        response=serializers.GenericErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).\
                            Errors messages are set for each specific field if any.'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed
