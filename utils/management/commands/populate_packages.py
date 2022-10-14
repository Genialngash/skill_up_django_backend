import os

import stripe
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from payments.models import AccessPackage


class Command(BaseCommand):
    help = 'This command populates the database with stripe products'

    def handle(self, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_products = stripe.Product.list()
        stripe_data = stripe_products['data']

        for item in stripe_data:
            if item['name'] != 'All Access Pro Subscription':
                # check if product exists
                pkg = AccessPackage.objects.filter(
                    stripe_product_id=item['id']
                )

                if not pkg.exists():
                    AccessPackage.objects.create(
                        title=item['name'],
                        unlocks=item['metadata']['unlocks'],
                        price=item['metadata']['price'],
                        stripe_product_id=item['id'],
                        stripe_price_id=item['metadata']['stripe_price_id'],
                        expires_in=item['metadata']['expires_in'],
                        job_cards=item['metadata']['job_cards'],
                        description=item['description']
                    )
                    print(f"Created Product with id {item['id']} Successfully")
                else:
                    print(f"Product with id {item['id']} Exists Already")


        try:
            AccessPackage.objects.get(tag='trial_package')
        except AccessPackage.DoesNotExist:
            AccessPackage.objects.create(
                tag='trial_package',
                title='Sign Up Trial Credits',
                unlocks=10,
                price=0,
                expires_in=30,
                job_cards=5,
                description='Sign up trial credits for new users.'
            )
