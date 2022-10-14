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
from jobseekers.models import JobseekerCertification, JobseekerLanguage, WorkExperience
from mixer.backend.django import mixer
from payments.models import AccessPackage
from PIL import Image
from rest_framework.test import APIClient
from users.models import JobseekerProfile


class TestProfessionInfo(TestCase):
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
    def test_that_user_can_patch_their_certifications(self):
        path = f'/jobseekers/professional-info/'
        data = json.dumps({
            "certifications": [
                    {
                        "title": "Walangolo Cert",
                        "certification_year": 2020
                    }
            ]
        })

        response = self.client.patch(
            path, 
            content_type="application/json",
            data=data
        )
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_that_user_can_patch_their_work_experience(self):
        path = f'/jobseekers/professional-info/'
        data = json.dumps({
            "work_experience": [
                {
                    "company_name": "Test Company",
                    "start_month": "January",
                    "start_year": 2006,
                    "end_month": "January",
                    "end_year": 2020,
                    "currently_working_here": True
                }
            ]
        })

        response = self.client.patch(
            path, 
            content_type="application/json",
            data=data
        )
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_that_user_can_patch_their_languages(self):
        path = f'/jobseekers/professional-info/'
        data = json.dumps({
            "languages": [
                {
                    "name": "Test lang",
                    "proficiency_level": "Elementary Proficiency"
                }
            ]
        })

        response = self.client.patch(
            path, 
            content_type="application/json",
            data=data
        )
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_that_user_cannot_patch_certifications_with_invalid_data(self):
        path = f'/jobseekers/professional-info/'
        data = json.dumps({
            "certifications": [
                    {
                        "title": "Walangolo Cert",
                        "certification_year": 2025 # Invalid year
                    }
            ]
        })

        response = self.client.patch(
            path, 
            content_type="application/json",
            data=data
        )

        assert response.data['message'] == 'Invalid certification year.'
        assert response.status_code == 400


    @pytest.mark.django_db
    def test_that_user_cannot_patch_languages_with_invalid_data(self):
        path = f'/jobseekers/professional-info/'
        data = json.dumps({
            "languages": [
                {
                    "name": "",
                    "proficiency_level": "Elementary Proficiency"
                }
            ]
        })

        response = self.client.patch(
            path, 
            content_type="application/json",
            data=data
        )

        assert response.data['message'] == 'Language name cannot be blank.'
        assert response.status_code == 400


    @pytest.mark.django_db
    def test_that_user_cannot_patch_work_experience_with_invalid_end_month(self):
        path = f'/jobseekers/professional-info/'
        data = json.dumps({
            "work_experience": [
                {
                    "company_name": "Company Y",
                    "start_month": "January",
                    "start_year": 2005,
                    "end_month": "December",
                    "end_year": 2022,
                    "currently_working_here": False
                }
            ]
        })

        response = self.client.patch(
            path, 
            content_type="application/json",
            data=data
        )

        assert 'End month not a valid choice.' in response.data['message']
        assert response.status_code == 400


    @pytest.mark.django_db
    def test_that_user_cannot_patch_work_experience_with_invalid_end_year(self):
        path = f'/jobseekers/professional-info/'
        data = json.dumps({
            "work_experience": [
                {
                    "company_name": "Company Y",
                    "start_month": "January",
                    "start_year": 2005,
                    "end_year": 2025,
                    "end_month": "May",
                    "currently_working_here": False
                }
            ]
        })

        response = self.client.patch(
            path, 
            content_type="application/json",
            data=data
        )

        assert "invalid end year." in response.data['message'].lower()
        assert response.status_code == 400


    @pytest.mark.django_db
    def test_that_passing_an_empty_list_deletes_all_entries(self):
        path = f'/jobseekers/professional-info/'
        data = json.dumps({
            "work_experience": [],
            "languages": [],
            "certifications": []
        })

        response = self.client.patch(
            path,
            content_type="application/json",
            data=data
        )

        jobskeeker_profile = self.user1.jobseeker_profile
        
        certs_len = len(
            JobseekerCertification.objects.filter(
                profile=jobskeeker_profile
            )
        )
        langs_len = len(
            JobseekerLanguage.objects.filter(
                profile=self.user1.jobseeker_profile
            )
        )

        assert certs_len == 0
        assert langs_len == 0
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_that_user_can_update_their_professional_info(self):
        path = f'/jobseekers/professional-info/'
        data = json.dumps({
            "languages": [
                {
                    "name": "English",
                    "proficiency_level": "Elementary Proficiency"
                }
            ],
            "certifications": [
                {
                    "title": "CCP",
                    "certification_year": 2020
                }
            ],
            "work_experience": [
                {
                    "company_name": "Forward Inc",
                    "start_month": "January",
                    "start_year": 2005,
                    "end_month": "January",
                    "end_year": 2020,
                    "currently_working_here": True
                }
            ]
        })

        response = self.client.patch(
            path, 
            content_type="application/json",
            data=data
        )

        jobskeeker_profile = self.user1.jobseeker_profile
        
        certs_len = len(
            JobseekerCertification.objects.filter(
                profile=jobskeeker_profile
            )
        )
        langs_len = len(
            JobseekerLanguage.objects.filter(
                profile=self.user1.jobseeker_profile
            )
        )

        work_exp_len = len(
            WorkExperience.objects.filter(
                profile=self.user1.jobseeker_profile
            )
        )

        assert certs_len == 1
        assert langs_len == 1
        assert work_exp_len == 1
        assert response.status_code == 200


# ("Forward Inc", "January", 2005, "January", 2020, True)
@pytest.mark.parametrize(
    "company, start_month, start_year, end_month, end_year, currently_working_here, validity",
    [
        # All Fields Okay
        ("Forward Inc", "January", 2005, None, None, True, 200),
        ("Forward Inc", "January", 2005, "March", 2020, False, 200),
        # ("Forward Inc", "", 2005, "March", None, False, 400),
        # ("Forward Inc", "January", None, "March", None, False, 400),
    ]
)
@pytest.mark.django_db
def test_user_creating_professional_experience(
    client, company, 
    start_month, start_year, 
    end_month, end_year, 
    currently_working_here,
    validity
):
    """
    Test creating a company with invalid payload fails
    """

    alt_client = APIClient()

    # Create the access pkg
    AccessPackage.objects.create(
        title = 'Signup Trial Credits',
        unlocks = 30,
        price = 0,
        expires_in = 30,
        job_cards =10,
        description = 'Demo text',
        tag = 'trial_package'
    )

    # Create user
    user = UserFactory(email='testuserone@example.com', u_type='General')
    # user2 = UserFactory(email='testusertwo@example.com', u_type='General')

    EmailAddress.objects.create(
        user=user, 
        email=user.email,
        verified=True, primary=True
    )

    # Create a company
    # company = mixer.blend('establishments.Company', hiring_manager=user2)


    # Authenticate user
    login_path = reverse('custom_login')
    login_res = alt_client.post(
        login_path, 
        data={
            'email': user.email,
            'password': 'testing321',
            'log_in_as': 'Employer'
        }
    )

    alt_client.credentials(HTTP_AUTHORIZATION='Bearer '+ login_res.data['data']['access_token'])

    em = None
    sy = None

    if end_month:
        em = end_month

    if end_year:
        sy = end_year

    print(em)
    print(sy)

    data = json.dumps({
        "company": company,
        "start_month": start_month,
        "start_year": start_year,
        "end_month": em,
        "end_year": sy,
        "currently_working_here": currently_working_here
    })

    response = alt_client.patch(
        '/jobseekers/professional-info/',
        data=data,
        content_type="application/json"
    )

    print(response.data)
    assert response.status_code == validity
