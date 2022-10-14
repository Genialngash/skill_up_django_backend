import json

import pytest
from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from establishments.factories import UserFactory
from mixer.backend.django import mixer
from payments.models import AccessPackage
from rest_framework.test import APIClient

User = get_user_model()

class TestJobApplication(TestCase):
    def setUp(self):
        # Create Access Trial Package
        AccessPackage.objects.create(
            title = 'Signup Trial Credits',
            unlocks = 30,
            price = 0,
            expires_in = 30,
            job_cards =10,
            description = 'Demo text',
            tag = 'trial_package'
        )

        self.user1 = UserFactory(email='testuserone@example.com', u_type='General')


        EmailAddress.objects.create(
            user=self.user1, 
            email=self.user1.email,
            verified=True, primary=True
        )

        self.client = APIClient()

        # Authenticate user
        self.login_path = reverse('custom_login')
        login_res = self.client.post(
            self.login_path, 
            data={
                'email': self.user1.email,
                'password': 'testing321',
                'log_in_as': 'Employer'
            }
        )

        self.company = mixer.blend(settings.COMPANY_MODEL, location='Nairobi', hiring_manager=self.user1)
        self.job_card_one = mixer.blend(settings.JOB_CARD_MODEL, company=self.company, location='Nairobi')
        self.job_card_two = mixer.blend(settings.JOB_CARD_MODEL, company=self.company, location='Nairobi')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['data']['access_token'])


    @pytest.mark.django_db
    def test_jobseeker_can_make_job_application(self):
        data = json.dumps(
            {
                'job_card': self.job_card_one.id,
                'user': self.user1.id
            }
        )

        path = '/job-applications/'
        response = self.client.post(path, data, content_type='application/json')
        assert response.data['message'] == 'Application submitted successfully.'
