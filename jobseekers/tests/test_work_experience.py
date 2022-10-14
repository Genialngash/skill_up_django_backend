import json

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

class TestJobseekerWorkExperienceView(TestCase):
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
    def test_jobseeker_can_create_a_work_experience_entry(self):
        """
        Test creating a work experience entry for a place that the user currently
        works at. ie The end year and the end month should be skipped in this scenario
        """

        path = '/work-experience/create/'
        data = {
            "profile": self.user1.jobseeker_profile.id,
            "company_name": "Doorstep Inc",
            "start_month": "March",
            "start_year": 2005,
            "currently_working_here": True
        }
        response = self.client.post(path, json.dumps(data), content_type='application/json')

        assert response.data['data']['currently_working_here'] == True
        assert response.data['message'] == 'Work experience saved.'
        assert response.status_code == 201


    @pytest.mark.django_db
    def test_jobseeker_cannot_create_a_work_experience_entry_with_invalid_payload(self):
        """
        Test creating a work experience entry for a place that the user is not currently
        working in and skipping end_month and end_year will throw an error.
        """

        path = '/work-experience/create/'
        data = {
            "profile": self.user1.jobseeker_profile.id,
            "company_name": "Doorstep Inc",
            "start_month": "January",
            "start_year": 2005,
            "currently_working_here": False
        }
        response = self.client.post(path, json.dumps(data), content_type='application/json')
        assert response.status_code == 400


    @pytest.mark.django_db
    def test_jobseeker_can_update_a_work_experience_entry(self):
        work_experience = WorkExperienceFactory(
            profile=self.user1.jobseeker_profile,
            start_year=2020,
            start_month='January',
            currently_working_here=True
        )

        path = f'/work-experience/update/{work_experience.id}/'

        data = {
            "profile": self.user1.jobseeker_profile.id,
            "company_name": "Doorstep Inc",
            "start_month": "March",
            "start_year": 2005,
            "currently_working_here": True
        }

        response = self.client.put(path, json.dumps(data), content_type='application/json')

        assert response.data['data']['currently_working_here'] == True
        assert response.data['message'] == 'Work experience updated successfully.'
        assert response.status_code == 200
