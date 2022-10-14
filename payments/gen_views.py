from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView


class StripeConfig(APIView):
    @csrf_exempt
    @extend_schema(
        request=None, 
        responses=inline_serializer(
            name='StripeConfigSerializer', 
            fields={
                'data': inline_serializer( 
                    name='StripePublicAPIKeySerializer', 
                    fields={ 
                        'public_key': serializers.CharField()
                    }
                ),
                'message': serializers.CharField(), 
                'status': serializers.CharField(), 
                'status_code': serializers.IntegerField()
            }
        ) 
    )
    def get(self, request, format=None):
        """
        Return the Stripe Publishable Key
        """
        payload = {
            'data': {
                'public_key': settings.STRIPE_PUBLISHABLE_KEY
            },
            'message': 'Success.',
            'status': 'ok',
            'status_code': 200
        }

        return Response(payload, status=status.HTTP_200_OK)
