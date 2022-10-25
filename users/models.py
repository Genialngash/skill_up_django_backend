import datetime
from datetime import datetime, timedelta
from pprint import pprint
from random import choices

import googlemaps
import h3
import stripe
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from establishments.models import Company
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from notifications.models import EmailNotificationSubscription
from payments.models import AccessPackage
from phonenumber_field.modelfields import PhoneNumberField
from profile_unlock.models import UserAccessCredit
from profile_unlock.profile_unlock_utilities import generate_random_code


from utils.common import get_date_suffix
from utils.models import JobCardZoneMetadata, JobseekerZoneMetadata, h3_resolutions
from establishments.models import CourseCard

from .model_choices import (
    EDUCATION_LEVEL,
    GENDER_TYPES,
    LANGUAGE_PROFICIENCY,
    LOGGED_IN_AS,
    MONTHS_OF_THE_YEAR,
    USER_TYPES,
)
from .model_managers import EmployerManager, JobseekerManager, UserManager

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


# Core Models
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    avatar = ProcessedImageField(
        upload_to="users/photos/%Y/%m/",
        processors=[Thumbnail(250, 250)],
        format="JPEG",
        options={"quality": 100},
        default="default.jpg",
    )
    phone_number = PhoneNumberField(null=True, blank=False)
    contact_is_verified = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=False)
    logged_in_as = models.CharField(
        _("Logged in as"),
        max_length=15,
        choices=LOGGED_IN_AS.choices,
        default=LOGGED_IN_AS.EMPLOYER,
        null=False,
        blank=False
    )

    u_type = models.CharField(
        _("User type"),
        max_length=15,
        choices=USER_TYPES.choices,
        default=USER_TYPES.GENERAL,
        null=False,
        blank=False
    )

    gender = models.CharField(
        _("Gender"), 
        max_length=16, 
        choices=GENDER_TYPES.choices,
        default=GENDER_TYPES.UNSPECIFIED,
        null=True,
        blank=False
    )

    # Profile publish status
    publish_jobseeker_profile = models.BooleanField(default=True)

    # Notifications
    unread_notifications = models.PositiveBigIntegerField(default=0)
    last_email_notification = models.DateTimeField(null=True, blank=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Assign user manager to the object's attributes
    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def access_credits(self):
        access_credits = UserAccessCredit.objects.filter(email=self.email)
        return access_credits

    @property
    def profile(self):
        if self.logged_in_as == 'Jobseeker':
            return self.jobseeker_profile
        if self.logged_in_as == 'Employer':
            return self.employer_profile
        return

    @property
    def companies(self):
        if self.u_type == 'General':
            companies = Company.objects.filter(hiring_manager=self)
            return companies
        return


# Create Proxy Models for each user type
class Jobseeker(User):
    objects = JobseekerManager()
    class Meta:
        proxy = True

    @property
    def more(self):
        return self.jobseekerprofile

    def save(self, *args, **kwargs):
        if not self.pk:
            self.u_type = USER_TYPES.GENERAL
        return super().save(*args, **kwargs)


class Employer(User):
    objects = EmployerManager()

    class Meta:
        proxy = True

    @property
    def more(self):
        return self.employerprofile


    def save(self, *args, **kwargs):
        if not self.pk:
            self.u_type = USER_TYPES.GENERAL
        return super().save(*args, **kwargs)

# User Profile Models
class JobseekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
        related_name='jobseeker_profile', db_constraint=False)
    bio = models.TextField(null=True, blank=False)
    country = models.CharField(max_length=64, null=True, blank=False)
    avg_rating = models.DecimalField(
        default=0.00, decimal_places=2, 
        max_digits=3, null=False, blank=False
    )
    total_ratings = models.IntegerField(default=0, null=False, blank=False)
    hourly_rate = models.IntegerField(null=True, blank=False)
    profile_completeness = models.IntegerField(
        default=0, null=False, blank=False
    )
    # Location
    location = models.CharField(blank=False, null=True, max_length=128)
    profession = models.CharField(max_length=128, null=True, blank=False)
    education_level = models.CharField(max_length=48, 
        choices=EDUCATION_LEVEL.choices, null=True, blank=False
    )

    def __str__(self):
        return self.user.email
    
    @property
    def zone_metadata(self):
        return JobseekerZoneMetadata.objects.get(profile=self)

    class Meta:
        ordering = ['-avg_rating']
        verbose_name = "Jobseeker Profile"
        verbose_name_plural = "Jobseeker Profiles"


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, 
        related_name='employer_profile', on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=96, null=True, blank=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Employer Profile"
        verbose_name_plural = "Employer Profiles"


from allauth.account.models import EmailAddress


# Signals
def create_profile(sender, instance, **kwargs):
    """
    A signal that creates a user profile here when a user completes signing up
    and they have verified their email.
    NOTE: This runs everytime the user model is saved
    """

    if instance.u_type == 'Veeta Superuser':
        try:
            EmailAddress.objects.get(email=instance.email)
        except EmailAddress.DoesNotExist:
            EmailAddress.objects.create(
                user=instance,
                email=instance.email,
                verified=True,
                primary=True
            )


    if instance.u_type == 'General':
        # Create email notifications record if it does not exist
        try:
            EmailNotificationSubscription.objects.get(user=instance)
        except EmailNotificationSubscription.DoesNotExist:
            EmailNotificationSubscription.objects.create(user=instance)

        # Create an employer profile if it does not exist
        try:
            EmployerProfile.objects.get(user=instance)
        except EmployerProfile.DoesNotExist:
            EmployerProfile.objects.create(user=instance)

        # Give Employer Access Credits on Sign Up
            access_pkg = AccessPackage.objects.get(tag='trial_package')
            total_unlocks = access_pkg.unlocks
            random_code = generate_random_code()
            naive_created_on = datetime.now()
            created_on = make_aware(naive_created_on)
            naive_expires_on = naive_created_on + timedelta(access_pkg.expires_in)
            expires_on = make_aware(naive_expires_on)

            employer_trial_access_pass = UserAccessCredit.objects.create(
                email=instance.email,
                total_unlocks=total_unlocks,
                job_cards=access_pkg.job_cards,
                is_valid=False,
                tag='sign_up_trial_credits',
                created_on=created_on,
                expires_on=expires_on,
            )

            employer_trial_access_pass.unlock_code = f"{employer_trial_access_pass.id}-{random_code}"
            employer_trial_access_pass.save()


        # Create a jobseeker profile if it does not exist
        try:
            print("Created")
            JobseekerProfile.objects.get(user=instance)
        except JobseekerProfile.DoesNotExist:
            JobseekerProfile.objects.create(user=instance)
        
        print(f'Successfully created profiles for {instance.email}...')

post_save.connect(create_profile, sender=User)
