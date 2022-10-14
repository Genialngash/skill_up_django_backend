from dj_rest_auth.registration.serializers import (
    ResendEmailVerificationSerializer,
    VerifyEmailSerializer,
)
from dj_rest_auth.serializers import (
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
)
from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from users.serializers import (
    GenericErrorResponseSerializer,
    JobseekerIncompleteDetailSerializer,
    JobseekerSlimSerializer,
)

from . import serializers


# Docs Fixes
class FixCertificationViewSet(OpenApiViewExtension):
    target_class = 'jobseekers.views.CertificationViewSet'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = serializers.JobseekerCertificationSerializer
            @extend_schema(
                request=serializers.JobseekerCertificationSerializer,
                responses={
                     200: OpenApiResponse(
                        response=serializers.JobseekerCertificationSerializer,
                        description='Success fetching a certification.' 
                    ),
                    400: OpenApiResponse(
                        response=GenericErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).\
                            Errors messages are set for each specific field if any.'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed


class FixLanguageViewSet(OpenApiViewExtension):
    target_class = 'jobseekers.views.LanguageViewSet'
    def view_replacement(self):
        class Fixed(self.target_class):
            serializer_class = serializers.JobseekerLanguageSerializer
            @extend_schema(
                request=serializers.JobseekerLanguageSerializer,
                responses={
                     200: OpenApiResponse(
                        response=serializers.JobseekerLanguageSerializer,
                        description='Success fetching a jobseeker language.' 
                    ),
                    400: OpenApiResponse(
                        response=GenericErrorResponseSerializer,
                        description='Bad request (Invalid payload or misssing required values).\
                            Errors messages are set for each specific field if any.'
                    ),
                }
            )
            def post(self, request, *args, **kwargs):
                pass
        return Fixed
