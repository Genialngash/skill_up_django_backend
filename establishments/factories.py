import random

import factory
import phonenumbers
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from faker import Faker
from jobseekers.models import WorkExperience
from users.model_choices import EDUCATION_LEVEL, GENDER_TYPES
from users.models import EmployerProfile, JobseekerProfile

from establishments.model_choices import CONTRACT_TYPES

from .models import Company, JobCard, JobResponsibility

User = get_user_model()

fake = Faker('en_GB')

BRANCH_COORDS = [
    {'lat': 51.51473816658067, 'lng': -0.13100397360813754},
    {'lat': 51.51302890000114, 'lng': -0.1306606508593433},
    {'lat': 51.51751558798179, 'lng': -0.07023584707156189},
    {'lat': 51.58350994020408, 'lng': -0.3346967694587454},
    {'lat': 51.496351814242566, 'lng': -0.19291271292203674},
    {'lat': 51.47718143028292, 'lng': -0.06811716215192123},
    {'lat': 51.360448367565006, 'lng': 0.27031636197975817},
    {'lat': 51.6131775910205, 'lng': -0.3605511646178433 },
    {'lat': 51.234355971164575, 'lng': -0.45853880704580224},
    {'lat': 51.603035265329844, 'lng': -0.020860659049482977},

    {'lat': 51.49842052744211, 'lng': -0.2562844684175228},    
    {'lat': 51.51832772907003, 'lng': -0.03439152950684869},
    {'lat': 51.515839805846895, 'lng': -0.15383389852489224},
    {'lat': 51.51272970837745, 'lng': -0.12734667893565824},
    {'lat': 51.50806416497765, 'lng': -0.1903162965122307},
    {'lat': 51.50090940400005, 'lng': -0.17632304867463547},
    {'lat': 51.50477006892204, 'lng': -0.12032440742117904},
    {'lat': 51.527394748601, 'lng': -0.15434640862965454},
    {'lat': 51.512588576073696, 'lng': -0.11913300126520852},
    {'lat': 51.54590802883456, 'lng': -0.14934540302162783},
]


JOBS_LIST = [
    'Cleaner',
    'Driver',
    'Waitress',
    'Sales Person',
    'Accountant',
    'Receptionist',
    'Gardener',
    'Plumber',
    'Messenger',
    'Cook'
]


JOB_CATEGORIES = [
    'Home Improvement',
    'Bulding',
    'IT',
    'Sales',
    'Accounting',
    'Office Personnel',
    'Farming and Gardening',
    'Plumbing',
    'Hotel and Tourism',
    'Transport',
]

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    # defaults
    name = fake.company()
    email = f'{name[0].lower()}@company.com'
    website_url = f'www.company.com'
    bio = fake.paragraph(nb_sentences=4)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # defaults
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f'{first_name.lower()}.{last_name.lower()}@example.com'
    u_type =  "General"
    logged_in_as = "Employer"
    phone_number = '+16135550151'
    contact_is_verified = True
    password = factory.PostGenerationMethodCall('set_password', 'testing321')


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailAddress

    # defaults
    email = 'email@example.com'
    verified = True
    primary = True


class EmployerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployerProfile

    # defaults
    user =  factory.SubFactory(UserFactory)
    phone_number = fake.phone_number()
    contact_is_verified = True
    stripe_subscription_id = 'test-sub-id'
    stripe_customer_id = 'test-customer-id'


class JobResponsibilityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobResponsibility

class JobCardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobCard

    company = factory.Iterator(Company.objects.all())
    contract_type = CONTRACT_TYPES.HOURLY_GIG
    is_published = True
    taken = False
    category = 'General'
    description = fake.paragraph(nb_sentences=4)
    location = 'Nairobi, Kenya'
    application_deadline = fake.future_date()



class WorkExperienceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WorkExperience

    # defaults
    company_name = fake.company()
