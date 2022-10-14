from email.mime import application

import pytest
from allauth.account.models import EmailAddress
from django.conf import settings
from django.core import mail
from django.test import Client, RequestFactory, TestCase
from django.urls import resolve, reverse
from establishments.factories import CompanyFactory, JobCardFactory, UserFactory
from mixer.backend.django import mixer
from payments.models import AccessPackage
from PIL import Image
from profile_unlock.models import UserAccessCredit
from rest_framework.test import APIClient


class TestNotifications(TestCase):
    def setUp(self):
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
    def test_user_can_fetch_their_notifications(self):
        path = f'/notifications/list/'
        response = self.client.get(path)
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_job_application_creates_a_notification(self):
        # create a company and job card as user1
        company = CompanyFactory(hiring_manager=self.user1)
        job_card = JobCardFactory(company=company, pay=10)

        # make an application as user2
        local_client = APIClient()
        login_res = local_client.post(
            self.login_path, 
            data={
                'email': self.user2.email,
                'password': 'testing321',
                'log_in_as': 'Employer'
            }
        )

        local_client.credentials(HTTP_AUTHORIZATION='Bearer '+ login_res.data['data']['access_token'])

        path = f'/job-applications/'
        data = {
            'user': self.user2.id,
            'job_card': job_card.id
        }
        response = local_client.post(path, data)
        print(response.data)

        # fetch notifications as user1 => owner of the company and the job card
        path = f'/notifications/list/'
        response = self.client.get(path)

        assert len(response.data['data']['results']) > 0
        assert response.status_code == 200



    @pytest.mark.django_db
    def test_user_can_modify_their_email_notifications_subscription(self):
        path = f'/notifications/email/subscription/'
        data = {"new_job_application": True}

        response = self.client.patch(path, data)
        assert response.data['message'] == "Email notifications updated."
        assert response.status_code == 200
