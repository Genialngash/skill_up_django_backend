import io
import json
from http import client
from pprint import pprint

import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory, TestCase
from django.urls import resolve, reverse
from establishments.factories import UserFactory
from mixer.backend.django import mixer
from payments.models import AccessPackage
from PIL import Image
from profile_unlock.models import UserAccessCredit
from rest_framework.test import APIClient


class TestEmployer(TestCase):
    def setUp(self):
        self.pkg = AccessPackage.objects.create(
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
        self.user3 = UserFactory(email='testuserthree@example.com', u_type='General')      

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

        EmailAddress.objects.create(
            user=self.user3, 
            email=self.user3.email,
            verified=True, primary=True
        )

        self.client = APIClient()

        # authenticate user1
        self.login_path = reverse('custom_login')
        login_res = self.client.post(
            self.login_path, 
            data={
                'email': self.user1.email,
                'password': 'testing321',
                'log_in_as': 'Employer'
            }
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ login_res.data['data']['access_token'])


    @pytest.mark.django_db
    def test_that_every_employer_gets_signup_credits(self):
        user_credits = UserAccessCredit.objects.filter(email=self.user1.email)
        assert len(user_credits) == 1


    @pytest.mark.django_db
    def test_user_can_fetch_their_employer_profile(self):
        path = f'/accounts/employer/profile/{self.user1.id}/'
        response = self.client.get(path)
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_user_can_only_fetch_their_employer_profile(self):
        """
        Test that a user can only fetch their employer profile
        anad not any other user's employer profile.
        """
        path = f'/accounts/employer/profile/{self.user2.id}/'
        response = self.client.get(path)
        assert response.status_code == 403


    @pytest.mark.django_db
    def test_user_can_only_fetch_their_employer_profile(self):
        """
        Test that a user can only fetch their profile if they are authenticated.
        """

        client = APIClient()
        path = f'/accounts/employer/profile/{self.user2.id}/'
        response = client.get(path)
        assert response.status_code == 401
