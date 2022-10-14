import io
import json

import pytest
from allauth.account.models import EmailAddress
from django.conf import settings
from django.core import mail
from django.test import Client, RequestFactory, TestCase
from django.urls import resolve, reverse
from establishments.factories import UserFactory
from mixer.backend.django import mixer
from payments.models import AccessPackage
from PIL import Image
from profile_unlock.models import UserAccessCredit
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def email_backend_setup(settings):
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

@pytest.mark.parametrize(
    "email, first_name, last_name, u_type, password1, password2, validity",
    [
        ('smookie@gmail.com', 'Smookie', 'Epps', 'General', 'testing321', 'testing321', 201),
        ('smookie@gmail.com', 'Smookie', 'Epps', 'General', 'testing32', 'testing321', 400),
        ('smookie@gmail.com', 'Smookie', 'Epps', 'General', '', 'testing321', 400),
        ('smookie@gmail.com', '', 'Epps', None, 'testing321', 'testing321', 400),
        ('smookie@gmail.com', 'Smookie', '', 'General', 'testing321', 'testing321', 400),
        ('smookie@gmail.com', None, '', 'General', 'testing321', 'testing321', 400)
    ]
)
@pytest.mark.django_db
def test_creating_new_user(
    client, email, first_name, last_name, u_type, password1, password2, validity
):
    AccessPackage.objects.create(
        title = 'Signup Trial Credits',
        unlocks = 30,
        price = 0,
        expires_in = 30,
        job_cards =10,
        description = 'Demo text',
        tag = 'trial_package'
    )

    response = client.post(
    '/accounts/registration/',
    content_type="application/json",
    data={
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'u_type': u_type,
        'password1': password1,
        'password2': password2,
    })

    # mail.send_mail('Activate your account', 'Email body.', settings.DEFAULT_FROM_EMAIL, [email])
    # assert mail.outbox[0].subject,'Activate your account'
    assert response.status_code == validity


class TestUser(TestCase):
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
                'log_in_as': 'Jobseeker'
            }
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ login_res.data['data']['access_token'])

    # # Generate a photo
    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file


    @pytest.mark.django_db
    def test_user_can_patch_their_user_data(self):
        path = f'/accounts/auth/user/me/{self.user1.id}/'
        data = {
            'gender': 'Female'
        }
        response = self.client.patch(
            path, json.dumps(data),
            content_type='application/json'
        )
        assert response.data['data']['gender'] == data['gender']
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_user_can_only_patch_their_user_data(self):
        path = f'/accounts/auth/user/me/{self.user3.id}/'
        data = {
            "birthday": '1995-12-25',
            "gender": 'Female'
        }
        response = self.client.patch(path, data)
        assert response.data['message'] == 'You are not authorized to make this request.'
        assert response.status_code == 403


    @pytest.mark.django_db
    def test_user_can_update_avatar(self):
        path = f'/accounts/auth/user/me/{self.user1.id}/'
        avatar = self.generate_photo_file()
        data = {
            "avatar": avatar
        }
        response = self.client.patch(path, data, format='multipart')
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_user_can_change_login_state(self):
        path = f'/accounts/auth/login-state/switch/'
        raw_data = {
            "log_in_as": "Jobseeker"
        }
        clean_data = json.dumps(raw_data)
        response = self.client.patch(
            path, 
            data=clean_data, 
            content_type="application/json"
        )

        assert "Successfully logged in as" in response.data['message']
        assert response.data['data']['user']['logged_in_as'] == raw_data['log_in_as']
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_authenticated_user_can_delete_their_account(self):
        path = f'/user/account/delete/'
        response = self.client.delete(path)
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_access_credits_are_deleted_on_account_deletion(self):
        path = f'/user/account/delete/'
        response = self.client.delete(path)
        user_credits = UserAccessCredit.objects.filter(email=self.user1.email)

        assert len(user_credits) == 0
        assert response.status_code == 204
