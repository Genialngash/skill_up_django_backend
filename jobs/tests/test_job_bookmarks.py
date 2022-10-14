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

class TestJobJobBookmarks(TestCase):
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

        # authenticate user
        self.login_path = reverse('custom_login')
        login_res = self.client.post(
            self.login_path, 
            data={
                'email': self.user1.email,
                'password': 'testing321',
                'log_in_as': 'Employer'
            }
        )

        self.company = mixer.blend(settings.COMPANY_MODEL, location='Nairobi', hiring_manager=self.user2)
        self.job_card_one = mixer.blend(settings.JOB_CARD_MODEL, company=self.company, location='Nairobi')
        self.job_card_two = mixer.blend(settings.JOB_CARD_MODEL, company=self.company, location='Nairobi')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['data']['access_token'])


    @pytest.mark.django_db
    def test_authenticated_jobseeker_can_create_job_bookmark(self):
        data = {
            'job_card': self.job_card_one.id,
            'user': self.user1.id
        }

        path = '/jobs/bookmark/create/'
        response = self.client.post(path, data)
        assert response.data['message'] == 'Bookmark saved successfully.'


    @pytest.mark.django_db
    def test_authenticated_jobseeker_cannot_create_duplicate_bookmarks(self):
        mixer.blend(settings.JOB_BOOKMARK_MODEL, job_card=self.job_card_one, user=self.user1)
        data = {
            'job_card': self.job_card_one.id,
            'user': self.user1.id
        }

        path = '/jobs/bookmark/create/'
        response = self.client.post(path, data)
        assert response.status_code == 400


    @pytest.mark.django_db
    def test_user_cannot_create_a_bookmark_on_behalf_of_another_user(self):
        data = {
            'job_card': self.job_card_one.id,
            'user': self.user3.id
        }

        path = '/jobs/bookmark/create/'
        response = self.client.post(path, data)
        assert response.status_code == 400
        assert response.data['message'] == 'You cannot create a bookmark for another user.'


    @pytest.mark.django_db
    def test_authenticated_jobseeker_can_list_their_job_bookmarks(self):
        mixer.blend(settings.JOB_BOOKMARK_MODEL, job_card=self.job_card_one, user=self.user1)
        mixer.blend(settings.JOB_BOOKMARK_MODEL, job_card=self.job_card_two, user=self.user1)

        path = '/jobs/bookmarks/list/'
        response = self.client.get(path)
        assert len(response.data['data']['results']) == 2


    @pytest.mark.django_db
    def test_authenticated_jobseeker_can_delete_all_their_job_bookmarks(self):
        mixer.blend(settings.JOB_BOOKMARK_MODEL, job_card=self.job_card_one, user=self.user1)
        mixer.blend(settings.JOB_BOOKMARK_MODEL, job_card=self.job_card_two, user=self.user1)

        path = '/jobs/bookmarks/delete/'
        response = self.client.delete(path)

        assert response.status_code == 200
        assert response.data['message'] == 'Bookmarks deleted successfully.'


    @pytest.mark.django_db
    def test_authenticated_jobseeker_can_delete_a_single_job_bookmarks(self):
        mixer.blend(settings.JOB_BOOKMARK_MODEL, job_card=self.job_card_one, user=self.user1)
        mixer.blend(settings.JOB_BOOKMARK_MODEL, job_card=self.job_card_two, user=self.user1)

        path = '/jobs/bookmarks/delete/'
        response = self.client.delete(path)

        assert response.status_code == 200
        assert response.data['message'] == 'Bookmarks deleted successfully.'
