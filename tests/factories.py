import factory
from django.contrib.auth import get_user_model
from establishments.factories import JOBS_LIST
from faker import Faker
from users.model_choices import USER_TYPES
from users.models import JobseekerProfile

User = get_user_model()

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = fake.ascii_free_email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f'{first_name.lower()}.{last_name.lower()}@example.com'
    u_type =  "Jobseeker"
    password = factory.PostGenerationMethodCall('set_password', 'testing321')



class JobseekerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobseekerProfile

    user = factory.SubFactory(UserFactory)
    bio = fake.paragraphs(nb=5)
    city = fake.city()
    country = 'United Kingdom'
    country_code = fake.country_calling_code()
    contact = fake.phone_number()
    residence = fake.latlng()
    birth_month = factory.Iterator(
        [
            'January', 
            'March',
            'December',
            'September',
            'October',
        ]
    )
    birth_year = factory.Iterator(['1995', '1992', '1993'])
    birth_day = factory.Iterator(['21', '12', '16'])
    gender = factory.Iterator(['Male', 'Female'])
    work_expertise = factory.Iterator(
        JOBS_LIST
    )
    education_level = factory.Iterator(
        USER_TYPES
    )
    hourly_rate = 25
