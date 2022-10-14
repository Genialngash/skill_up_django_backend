import json
from email.mime import application

import pytest
from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from establishments.factories import UserFactory, WorkExperienceFactory
from mixer.backend.django import mixer
from payments.models import AccessPackage
from rest_framework.test import APIClient

User = get_user_model()


class TesTJobOfferViews(TestCase):
    def setUp(self):
        # Create Access Trial Package
        mixer.blend("payments.AccessPackage", tag='trial_package')

        # Create users with activated emails
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

        # create a company and a job card
        self.company = mixer.blend("establishments.Company", location='Nairobi, Kenya', hiring_manager=self.user2)
        self.job_card = mixer.blend("establishments.JobCard", location='Nairobi, Kenya', company=self.company)
        self.job_application = mixer.blend(
            "establishments.JobApplication",
            job_card=self.job_card,
            user=self.user1
        )

        # authenticate user1
        self.login_path = reverse('custom_login')
        login_res = self.client.post(
            self.login_path, 
            data={
                'email': self.user1.email,
                'password': 'testing321',
                'log_in_as': 'Jobseeker'
            }
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ login_res.data['data']['access_token'])


    @pytest.mark.django_db
    def test_employer_can_make_an_offer(self):
        path = '/job-offer/create/'
        data = {
            'job_card': self.job_card.id,
            'job_application': self.job_application.id,
            'applicant': self.job_application.user.id
        }

        response = self.client.post(path, json.dumps(data), content_type='application/json')
        assert response.data['message'] == 'Job offer created.'
        assert response.status_code == 201


    @pytest.mark.django_db
    def test_jobseeker_can_list_offers_made_to_them(self):
        path = '/jobseeker/offers/list/'
        response = self.client.get(path, content_type='application/json')
        assert len(response.data['data']['results']) >= 0
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_jobseeker_can_accept_a_job_offer(self):
        # scaffold a job offer
        job_offer = mixer.blend(
            "employers.JobOffer",
            job_card=self.job_card,
            job_application=self.job_application,
            applicant=self.user1
        )

        path = f'/jobseeker/offer/accept/{job_offer.id}/'
        data = {'is_accepted': False}

        response = self.client.put(path, json.dumps(data), content_type='application/json')
        assert response.status_code == 200
