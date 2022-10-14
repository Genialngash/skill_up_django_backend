
import pytest
from django.db import IntegrityError, transaction
from faker import Faker
from users.model_choices import EDUCATION_LEVEL
from users.models import JobseekerProfile

fake = Faker()

@pytest.mark.django_db(transaction=True)
def test_integrity_creating_jobseeker():
    with pytest.raises(IntegrityError):
        # creating a Jobseeker without a user with id of 1 
        JobseekerProfile.objects.create(user_id=1)
