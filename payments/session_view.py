import datetime
import json
from datetime import datetime, timedelta

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from profile_unlock.models import UserAccessCredit
from profile_unlock.profile_unlock_utilities import generate_random_code
from rest_framework import generics, status, views
from rest_framework.response import Response
from utils.common import get_date_suffix

from .models import AccessPackage
from .serializers import AccessPackageSerializer, StripeCheckoutSerializer
from .tasks import send_user_activation_code

User = get_user_model()

class PackagesListView(generics.ListAPIView):
    """
    List the packages available for purchase
    """
    serializer_class = AccessPackageSerializer
    queryset = AccessPackage.objects.filter(tag='unlock_code_package')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'status': 'ok',
            'status_code': 200,
            'message': 'Success.',
        })


class StripeCheckoutView(views.APIView):
    serializer_class = StripeCheckoutSerializer
    stripe.api_key = settings.STRIPE_SECRET_KEY

    def post(self, request, format=None):
        user = request.user
        serializer = StripeCheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain_url = settings.STRIPE_FRONTEND_DOMAIN_URL

        try:
            product_tag = serializer.data['product_tag']

            if product_tag == 'unlock_code_package':
                unlock_package = AccessPackage.objects.get(
                    stripe_product_id=serializer.data['stripe_product_id'])

                if user.is_anonymous:
                    checkout_session = stripe.checkout.Session.create(
                        success_url=domain_url + '/payments/success?sid={CHECKOUT_SESSION_ID}',
                        cancel_url=domain_url + '/payments/failure/',
                        payment_method_types=['card'],
                        mode='payment',
                        metadata={
                            'user_type': 'anonymous_user',
                            'product_tag': product_tag,
                            'veeta_product_id': unlock_package.id,
                            'stripe_product_id': unlock_package.stripe_product_id,
                            'unlocks': unlock_package.unlocks,
                        },
                        line_items=[
                            {
                                'price': unlock_package.stripe_price_id,
                                'quantity': 1,
                            }
                        ],
                        customer_creation="if_required"
                    )

                if not user.is_anonymous:
                    # Create a stripe customer if they do not exist
                    if user.u_type == 'General':
                        employer_profile = user.employer_profile

                        if employer_profile.stripe_customer_id is None:
                            # create a new customer
                            full_name = f"{user.first_name} {user.last_name}"
                            stripe_customer = stripe.Customer.create(
                                email=user.email,
                                name=full_name
                            )
                            stripe_customer_id = stripe_customer['id']
                            employer_profile.stripe_customer_id = stripe_customer['id']
                            employer_profile.save()
                        
                        if employer_profile.stripe_customer_id:
                            stripe_customer_id = employer_profile.stripe_customer_id

                    checkout_session = stripe.checkout.Session.create(
                        success_url=domain_url + '/payments/success?sid={CHECKOUT_SESSION_ID}',
                        cancel_url=domain_url + '/payments/cancelled/',
                        payment_method_types=['card'],
                        mode='payment',
                        metadata={
                            'user_type': 'authenticated_user',
                            'product_tag': product_tag,
                            'veeta_product_id': unlock_package.id,
                            'stripe_product_id': unlock_package.stripe_product_id,
                            'unlocks': unlock_package.unlocks
                        },
                        line_items=[
                            {
                                'price': unlock_package.stripe_price_id,
                                'quantity': 1,
                            }
                        ],
                        customer=stripe_customer_id
                    )

                return Response({
                    'data': {
                        'session_id': checkout_session['id']
                    },
                    'message': 'Checkout session created successfully.',
                    'status': 'ok',
                    'status_code': 200,
                }, status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'status': 'error',
                'error_code': 'invalid',
                'message': str(e),
                'status_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)



class StripeWebhook(views.APIView):
    # webhook
    # ./stripe listen --api-key ${VEETA_STRIPE_SECRET_KEY} --forward-to localhost:8000/payments/webhook/
    
    @extend_schema(exclude=True)
    @csrf_exempt
    def post(self, request, format=None):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return Response({
                'error_code': 'invalid',
                'message': 'Invalid payload.',
                'status': 'error',
                'status_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response({
                'error_code': 'invalid',
                'message': 'Invalid signature.',
                'status': 'error',
                'status_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)


        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            print("Payment was Successful.")
            payment_data = json.loads(payload)
            clean_data = payment_data['data']['object']
            email = clean_data['customer_details']['email']
            payment_metadata = clean_data['metadata']

            if payment_metadata['product_tag'] == 'unlock_code_package':
                print('Creating CODE')
                access_pkg = AccessPackage.objects.get(stripe_product_id=payment_metadata['stripe_product_id'])
                total_unlocks = access_pkg.unlocks
                random_code = generate_random_code()
                naive_created_on = datetime.now()
                created_on = make_aware(naive_created_on)
                naive_expires_on = naive_created_on + timedelta(access_pkg.expires_in)
                expires_on = make_aware(naive_expires_on)

                if payment_metadata['user_type'] == 'anonymous_user':
                    valid_codes = UserAccessCredit.objects.filter(
                        is_valid=True,
                        email=email
                    )

                    if valid_codes.exists():
                        auth_unlock_code = valid_codes[0]
                        print('Found a Valid Code')

                        naive_expires_on = naive_created_on + timedelta(access_pkg.expires_in)
                        expires_on = make_aware(naive_expires_on)
                        updated_total_unlocks = auth_unlock_code.total_unlocks + total_unlocks
                        updated_total_job_cards = auth_unlock_code.job_cards + access_pkg.job_cards
                        auth_unlock_code.total_unlocks = updated_total_unlocks
                        auth_unlock_code.job_cards = updated_total_job_cards
                        auth_unlock_code.expires_on = expires_on
                        auth_unlock_code.save()

                        # Send Email to User via Celery
                        mail_context = generate_mail_context(auth_unlock_code)
                        send_user_activation_code \
                            .delay(auth_unlock_code.email, mail_context)


                    if not valid_codes.exists():
                        new_unlock_code = UserAccessCredit.objects.create(
                            email=email,
                            total_unlocks=total_unlocks,
                            job_cards=access_pkg.job_cards,
                            is_valid=True,
                            tag='customer_bought_credits',
                            created_on=created_on,
                            expires_on=expires_on,
                        )

                        new_unlock_code.unlock_code = f"{new_unlock_code.id}-{random_code}"
                        new_unlock_code.save()

                        # Send Email to User via Celery
                        mail_context = generate_mail_context(new_unlock_code)                        
                        send_user_activation_code \
                            .delay(new_unlock_code.email, mail_context)


                if payment_metadata['user_type'] == 'authenticated_user':
                    # Get user from DB
                    user = User.objects.get(email=email)
                    
                    # Check for existing access code
                    valid_codes = UserAccessCredit.objects.filter(
                        is_valid=True,
                        email=email
                    )

                    if valid_codes.exists():
                        auth_unlock_code = valid_codes[0]
                        print('Found a Valid Code')

                        naive_expires_on = naive_created_on + timedelta(access_pkg.expires_in)
                        expires_on = make_aware(naive_expires_on)
                        updated_total_unlocks = auth_unlock_code.total_unlocks + total_unlocks
                        updated_total_job_cards = auth_unlock_code.job_cards + access_pkg.job_cards
                        auth_unlock_code.total_unlocks = updated_total_unlocks
                        auth_unlock_code.job_cards = updated_total_job_cards
                        auth_unlock_code.expires_on = expires_on
                        auth_unlock_code.save()

                        # Send Email to User via Celery
                        mail_context = generate_mail_context(auth_unlock_code)
                        send_user_activation_code \
                            .delay(auth_unlock_code.user.email, mail_context)


                    if not valid_codes.exists():
                        auth_unlock_code = UserAccessCredit.objects.create(
                            user=user,
                            email=email,
                            total_unlocks=total_unlocks,
                            job_cards=access_pkg.job_cards,
                            is_valid=True,
                            tag='customer_bought_credits',
                            created_on=created_on,
                            expires_on=expires_on,
                        )

                        auth_unlock_code.unlock_code = f"{auth_unlock_code.id}-{random_code}"
                        auth_unlock_code.save()

                        # Send Email to User via Celery
                        mail_context = generate_mail_context(auth_unlock_code)                        
                        send_user_activation_code \
                            .delay(auth_unlock_code.user.email, mail_context)

        return Response(status=status.HTTP_200_OK)


def generate_mail_context(access_credit):
    expire_month = access_credit.expires_on.strftime("%B") # 'December'
    expire_day = access_credit.expires_on.day
    expire_year = access_credit.expires_on.year
    date_suffix = get_date_suffix(access_credit.expires_on)

    mail_context = {
        'unlock_code': access_credit.unlock_code,
        'expire_month': expire_month,
        'expire_day': expire_day,
        'expire_year': expire_year,
        'date_suffix': date_suffix,
        'job_cards': access_credit.job_cards,
        'total_unlocks': access_credit.total_unlocks,
        'site_name': 'Veeta UK'
    }

    return mail_context
