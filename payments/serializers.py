from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from .models import AccessPackage


@extend_schema_serializer(
    examples=[
         OpenApiExample(
        'List Unlock Packages',
        description=
            """This is the response you list the packages offered.""",
        value={
            "data": [
                {
                    "id": 0,
                    "image": "http://example.com/media/default.jpg",
                    "title": "Package Title",
                    "unlocks": 0,
                    "price": 0,
                    "stripe_product_id": "string",
                    "stripe_price_id": "string",
                    "expires_in": 0,
                    "job_cards": 0,
                    "description": "Short descripton",
                    "tag": "unlock_code_package"
                }
            ],
            "status": "ok",
            "status_code": 200,
            "message": "String."
        },
        request_only=False,
        response_only=True,
        ),
    ]
)
class AccessPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessPackage
        fields = ('__all__')


class StripeCheckoutSerializer(serializers.Serializer):
    product_tag = serializers.CharField(required=True)
    stripe_product_id = serializers.CharField(required=True)
