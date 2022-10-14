import random
from operator import index

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from establishments.factories import (
    JOBS_LIST,
    CompanyFactory,
    EmailFactory,
    JobCardFactory,
    UserFactory,
)
from establishments.models import Company
from faker import Faker
from faker_e164.providers import E164Provider
from payments.models import AccessPackage
from users.model_choices import EDUCATION_LEVEL, GENDER_TYPES
from users.models import EmployerProfile, JobseekerProfile

from .locations import locations

User = get_user_model()
fake = Faker('en_GB')
fake.add_provider(E164Provider)

class Command(BaseCommand):
    help = 'This command populates the database with data needed for testing purposes'

    def handle(self, *args, **kwargs):
        for _j in range(10):
            # Create x amount of users
            first_name=fake.unique.first_name(),
            last_name=fake.unique.last_name(),

            # Contact
            region_choices = ['AU', 'US', 'GB', 'CA']
            phone_number = fake.safe_e164(region_code=random.choice(region_choices))
            contact_is_verified = True

            # Birthday
            random_day_of_the_month = random.randint(1, 28)
            random_month = random.randint(1, 12)
            year_choices = [1996, 1995, 1990, 2000, 1989, 1992]
            year = random.choice(year_choices)

            birthday = f"{year}-{random_month}-{random_day_of_the_month}"

            # Gender
            gender_choices = ['Female', 'Male',]
            gender = random.choice(gender_choices)

            # Email
            email = first_name[0].lower() + '.' + last_name[0].lower() + '@yopmail.com',
            u_type='General'

            new_user = UserFactory(
                first_name=first_name[0],
                last_name=last_name[0],
                email=email[0],
                u_type=u_type,
                gender=gender,
                birthday=birthday,
                phone_number=phone_number,
                contact_is_verified=contact_is_verified
            )
            EmailFactory(user=new_user, email=email[0], primary=True, verified=True)

            # Update_profile
            jobseeker_profile = JobseekerProfile.objects.get(user=new_user)
            jobseeker_profile.bio = fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
            jobseeker_profile.location =  random.choice(locations)
            jobseeker_profile.country = 'Kenya'

            rating_choices = [1.00, 2.00, 3.00, 4.00, 5.00]
            jobseeker_profile.avg_rating = random.choice(rating_choices)

            total_raters_choices = [12, 56, 30, 43, 28, 32]
            jobseeker_profile.total_ratings = random.choice(total_raters_choices)

            hourly_rate_choices = [15, 30, 45, 35,]
            jobseeker_profile.hourly_rate = random.choice(hourly_rate_choices)


            ed_level_choices = ['Unspecified', "Primary School" , "Secondary School", "Undergraduate Degree", "Masters Degree"]
            jobseeker_profile.education_level = random.choice(ed_level_choices)
            jobseeker_profile.profession = fake.job()
            jobseeker_profile.save()


        reqular_users = User.objects.filter(is_superuser=False, is_staff=False)
        for index, employer in enumerate(reqular_users, start=0):
            # Create companies for every user
            company_name = fake.company()
            email = 'example-email@company.com'
            website_url = 'www.company.com'
            bio = fake.paragraph(nb_sentences=4)
            new_company = CompanyFactory(
                hiring_manager=employer, 
                name=company_name, 
                email=email, 
                website_url=website_url,
                bio=bio
            )
