import io
import json
from http import client

import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory, TestCase
from django.urls import resolve, reverse
from establishments.factories import UserFactory
from mixer.backend.django import mixer
from payments.models import AccessPackage
from PIL import Image
from rest_framework.test import APIClient

User = get_user_model()


def create_employer():
    user = UserFactory(u_type='Employer')
    return user


@pytest.mark.django_db
def test_fetching_user_companies_anonymously(client):
    """
    Test an anonymous user cannot view user specific companies
    """
    response = client.get('/my-companies/', content_type="application/json",)
    assert response.status_code == 401


@pytest.mark.django_db
def test_fetching_companies_detail_anonymously(client):
    """
    Test that only users of type employers can view company details
    """
    pkg = AccessPackage.objects.create(
        title = 'Signup Trial Credits',
        unlocks = 30,
        price = 0,
        expires_in = 30,
        job_cards =10,
        description = 'Demo text',
        tag = 'trial_package'
    )

    user1 = UserFactory(email='testuserone@example.com', u_type='Employer')
    company = mixer.blend('establishments.Company', hiring_manager=user1)
    path = f'/company/{company.id}/'
    response = client.get(path, content_type="application/json",)
    assert response.status_code == 401


class TestCompany(TestCase):
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
        self.user1_co = mixer.blend('establishments.Company', hiring_manager=self.user1)
        self.user2_co = mixer.blend('establishments.Company', hiring_manager=self.user2)

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

    # generate a photo
    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file


    @pytest.mark.django_db
    def test_user_can_create_a_company(self):
        path = f'/company/'
        data = {
            "name": "July Inc",
            "email": "july-inc@example.com",
            "location": "Nairobi",
            "website_url": "https://july-inc.com",
            "bio": "Some bio",
            "hiring_manager": self.user1.id
        }

        parsed_data = json.dumps(data)
        response = self.client.post(path, parsed_data, content_type='application/json')
        assert response.status_code == 201


    @pytest.mark.django_db
    def test_owner_can_delete_own_company(self):
        path = f'/company/{self.user1_co.id}/'
        response = self.client.delete(path)
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_owner_can_modify_own_company(self):
        path = f'/company/{self.user1_co.id}/'
        response = self.client.patch(path, {'name': 'New Company Name'})
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_cannot_delete_another_employer_company(self):
        path = f'/company/{self.user2_co.id}/'
        response = self.client.delete(path)
        assert response.status_code == 401


    @pytest.mark.django_db
    def test_cannot_modify_another_employer_company(self):
        path = f'/company/{self.user2_co.id}/'
        response = self.client.patch(path, {'company_website': 'http://url-change.com'})
        assert response.status_code == 401


    @pytest.mark.django_db
    def test_employer_can_create_company(self):
        path = f'/company/'
        logo_image = self.generate_photo_file()
        data={
            "name": "Test Company Name",
            "email": 'email@example.com',
            "logo": logo_image,
            "website_url": 'http://example.com',
            "bio": 'Some bio',
            "hiring_manager": int(self.user1.id),
            "location": "Nrb"
        }

        response = self.client.post(path, data, format='multipart')
        assert response.status_code == 201


    @pytest.mark.django_db
    def test_jobseeker_cannot_create_company(self):
        login_jobseeker = self.client.post(
            self.login_path, 
            data={
                'email': self.user3.email,
                'password': 'testing321',
                'log_in_as': 'Jobseeker'
            }
        )

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer '+ login_jobseeker.data['data']['access_token']
        )

        path = f'/company/'
        logo_image = self.generate_photo_file()
        data={
            "name": "Test Company Name",
            "email": 'email@example.com',
            "logo": logo_image,
            "website_url": 'http://example.com',
            "bio": 'Some bio',
            "hiring_manager": int(self.user3.id),
            "location": "Nrb"
        }

        response = self.client.post(path, data, format='multipart')
        assert response.status_code == 403



    @pytest.mark.django_db
    def test_only_the_owner_can_delete_company(self):
        """
        Test that only the owner can delete their company
        """
        company = mixer.blend('establishments.Company', hiring_manager=self.user2)
        path = f'/company/{company.id}/'
        response = self.client.delete(path, content_type="application/json",)    
        assert response.status_code == 401


    @pytest.mark.django_db
    def test_modifying_company_anonymously(self):
        """
        Test that only the owner can modify their company
        """
        company = mixer.blend('establishments.Company', hiring_manager=self.user2)
        path = f'/company/{company.id}/'
        data=json.dumps({"name": "New Company Name"})
        response = self.client.patch(
            path, 
            data, 
            content_type="application/json"
        )

        assert response.status_code == 401


@pytest.mark.parametrize(
    "name, email, website_url, bio, location, validity",
    [
        # All Fields Okay
        ('Test Company', 'test-email@company.com', 'http://company.com', 'Some bio', 'Some City', 201),
        # Missing | Blank Company Name
        ('', 'test-email@company.com', 'http://company.com', 'Some bio', 'Nrb', 400),
        (None, 'test-email@company.com', 'http://company.com', 'Some bio', 'Nrb', 400),
        # Missing | Invalid Company Email
        ('Test Company', '', 'http://company.com', 'Nrb', 'Some bio', 400),
        ('Test Company', None, 'http://company.com', 'Nrb', 'Some bio', 400),
        ('Test Company', 'test-emailcompany.com', 'http://company.com', 'Some bio', 'Nrb', 400),
        # Invalid | Missing Company Website
        ('Test Company', 'test-email@company.com', 'company.com', 'Some bio', 'Some City', 400),
        ('Test Company', 'test-email@company.com', '', 'Some bio', 'Some City', 201),
        ('Test Company', 'test-email@company.com', None, 'Nrb', 'Some bio', 201),
        # Missing Location
        ('Test Company', 'test-email@company.com', 'http://company.com', 'Some bio', '', 400),
        ('Test Company', 'test-email@company.com', 'http://company.com', 'Some bio', None, 400),
        # Mising Bio
        ('Test Company', 'test-email@company.com', 'http://company.com', 'Some bio', '', 400),
        ('Test Company', 'test-email@company.com', 'http://company.com', 'Some bio', None, 400),
    ]
)
@pytest.mark.django_db
def test_employer_can_create_company(
    client, name, email, website_url, location, bio, validity
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
    EmailAddress.objects.create(
        user=user, 
        email=user.email,
        verified=True, primary=True
    )

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
    data = json.dumps({
        "name": name,
        "email": email,
        "website_url": website_url,
        "bio": bio,
        "hiring_manager": int(user.id),
        "location": location
    })

    response = alt_client.post(
        '/company/',
        content_type="application/json",
        data=data
    )

    assert response.status_code == validity
