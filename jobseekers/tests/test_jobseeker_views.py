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

class TestJobseekerListView(TestCase):
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
        self.user2 = UserFactory(email='testusertwo@example.com', u_type='General')

        EmailAddress.objects.create(
            user=self.user1, 
            email=self.user1.email,
            verified=True, primary=True
        )

        EmailAddress.objects.create(
            user=self.user2, 
            email=self.user2.email,
            verified=True, primary=True
        )

        self.client = APIClient()


    @pytest.mark.django_db
    def test_users_can_list_jobseekers(self):
        path = '/jobseekers/'
        response = self.client.get(path)
        assert len(response.data['data']['results']) == 2
        assert response.status_code == 200
