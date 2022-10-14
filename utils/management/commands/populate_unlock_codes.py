import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from faker import Faker
from payments.models import AccessPackage
from profile_unlock.models import UserAccessCredit
from profile_unlock.profile_unlock_utilities import generate_random_code

User = get_user_model()
fake = Faker('en_GB')

class Command(BaseCommand):
    help = 'This command populates the database with unlock codes'

    def handle(self, *args, **kwargs):
        product_id_choices = ['prod_LELe6q3up2mbWz', 'prod_LEiHQv8ohaXrLY', 'prod_LEiMRrZv4YT97n']
        employers = User.objects.filter(u_type='General').order_by('-id')[:15]

        # Registered users codes
        for employer in employers:
            # code
            access_pkg = AccessPackage.objects.get(stripe_product_id=product_id_choices[random.randint(0, 2)])
            total_unlocks = access_pkg.unlocks
            random_code = generate_random_code()
            naive_created_on = datetime.now()
            created_on = make_aware(naive_created_on)
            naive_expires_on = naive_created_on + timedelta(access_pkg.expires_in)
            expires_on = make_aware(naive_expires_on)

            new_unlock_code = UserAccessCredit.objects.create(
                email=employer.email,
                total_unlocks=total_unlocks,
                job_cards=access_pkg.job_cards,
                is_valid=True,
                tag='sign_up_trial_credits',
                created_on=created_on,
                expires_on=expires_on,
            )

            new_unlock_code.unlock_code = f"{new_unlock_code.id}-{random_code}"
            new_unlock_code.save()
            print(f'Created Unlock Code for {new_unlock_code.email}')

   
        # anonymous user codes
        for _ in range(12):
            # code
            access_pkg = AccessPackage.objects.get(stripe_product_id=product_id_choices[random.randint(0, 2)])
            total_unlocks = access_pkg.unlocks
            random_code = generate_random_code()
            naive_created_on = datetime.now()
            created_on = make_aware(naive_created_on)
            naive_expires_on = naive_created_on + timedelta(access_pkg.expires_in)
            expires_on = make_aware(naive_expires_on)

            new_unlock_code = AnonymousUserAccessCode.objects.create(
                email=fake.ascii_free_email(),
                total_unlocks=total_unlocks,
                job_cards=access_pkg.job_cards,
                is_valid=True,
                created_on=created_on,
                expires_on=expires_on,
            )

            new_unlock_code.unlock_code = f"{new_unlock_code.id}-{random_code}"
            new_unlock_code.save()

        print('All Unlock Codes Created Successfully')
        return
