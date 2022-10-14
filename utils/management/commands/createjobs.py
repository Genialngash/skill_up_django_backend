import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from establishments.factories import (
    JOB_CATEGORIES,
    JOBS_LIST,
    JobCardFactory,
    JobResponsibilityFactory,
)
from establishments.models import Company
from faker import Faker

from .locations import locations

User = get_user_model()
fake = Faker() 


categories = [
    'Health & Medicine',
    'Engineering',
    'Hotel & Hospitality',
    'Education',
    'Business Management',
    'General',
    'Construction',
    'Art',
]

class Command(BaseCommand):
    help = 'This command populates the database with fake jobs'

    def handle(self, *args, **kwargs):
        companies = Company.objects.all()
        total_companies = len(companies)

        for i in range(total_companies): 
            co_index = random.randrange(0, total_companies)

            location_index = random.randrange(0, (len(locations) - 1))
            card = JobCardFactory(
                location=locations[location_index],
                company=companies[co_index],
                role=fake.job(), 
                category=random.choice(categories),
                description = fake.paragraph(nb_sentences=5),
                pay=random.randrange(15, 65, 5)
            )

            total_responsibilities = random.randrange(1, 5)

            for _ in range(total_responsibilities):
                JobResponsibilityFactory(
                    card=card,
                    text=fake.sentence(nb_words=7, variable_nb_words=False)
                )

            card.save()
            print(f"Created a job card for {card.role}")
