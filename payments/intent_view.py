import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import views
from rest_framework.response import Response
from users.models import EmployerProfile

from .models import AccessPackage

User = get_user_model()


from rest_framework import serializers


class IntentSerializer(serializers.Serializer):
    stripe_product_id = serializers.CharField(required=True)
    service_type = serializers.CharField(required=True)
    user_email = serializers.EmailField(required=True)


class StripeIntentView(views.APIView):

    serializer_class = IntentSerializer

    def post(self, request, format=None):
        serializer = IntentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            # if request.data['package_type'] == 'all_access_sub':
            #     sub_package = ProSubscriptionPackage.objects.get(stripe_product_id=request.data['stripe_package_id'])
            #     user = User.objects.get(email=request.data['user_email'])
            #     employer_profile = EmployerProfile.objects.get(user=user)

            #     if employer_profile.stripe_customer_id is None:
            #         user_full_name = f'{user.first_name} {user.last_name}'
            #         customer = stripe.Customer.create(
            #             email=request.data['user_email'],
            #             name=user_full_name
            #         )
                
            #     if employer_profile.stripe_customer_id:
            #         customer = stripe.Customer.retrieve(employer_profile.stripe_customer_id)

            #     # TODO: add receipt_email=user.email, on PROD

            #     subscription = stripe.Subscription.create(
            #             customer=customer['id'],
            #             items=[{
            #                 'price': sub_package.stripe_price_id,
            #             }],
            #             payment_behavior='default_incomplete',
            #             expand=['latest_invoice.payment_intent'],
            #         )

            #     return Response({
            #         'clientSecret': subscription['latest_invoice']['payment_intent']['client_secret']
            #     })


            if request.data['service_type'] == 'unlock_code':
                print('HANDLE UNLOCK')
                unlock_package = AccessPackage.objects.get(stripe_product_id=request.data['stripe_product_id'])
                stripe_price = stripe.Price.retrieve(unlock_package.stripe_price_id)
                intent = stripe.PaymentIntent.create(
                    amount=stripe_price['unit_amount'],
                    currency='usd',
                    payment_method_types=['card'],
                    metadata={
                        'service_type': request.data['service_type'],
                        'unlock_package_id': unlock_package.id,
                        'user_email': request.data['user_email'],
                        'user_type': 'anonymous'
                    }
                )

                print(intent)

                return Response({
                    'data': {
                        'client_secret': intent['client_secret'],
                    },
                    'message': 'Success.',
                    'status_code': 200,
                    'status': 'ok'
                })

        except Exception as e:
            print(e)
            return Response({ 'detail': str(e) })
