import datetime
from datetime import datetime, timedelta
from random import choices

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from establishments.models import Company
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from payments.models import AccessPackage
from phonenumber_field.modelfields import PhoneNumberField
from profile_unlock.models import UserAccessCredit
from profile_unlock.profile_unlock_utilities import generate_random_code
from users.model_choices import (
    EDUCATION_LEVEL,
    GENDER_TYPES,
    LANGUAGE_PROFICIENCY,
    LOGGED_IN_AS,
    MONTHS_OF_THE_YEAR,
    USER_TYPES,
)
from utils.common import get_date_suffix
from utils.models import JobCardZoneMetadata, JobseekerZoneMetadata, h3_resolutions


# Jobseeker Profile Models
class WorkExperience(models.Model):
    profile = models.ForeignKey('users.JobseekerProfile', 
        related_name='jobseeker_experience', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=128, null=False, blank=False)
    start_year = models.PositiveIntegerField(_("Start year"), null=False, blank=False)
    start_month = models.CharField(_("Start month"), 
        choices=MONTHS_OF_THE_YEAR.choices, max_length=16, null=False, blank=False)
    end_month = models.CharField(_("End month"), 
        choices=MONTHS_OF_THE_YEAR.choices, max_length=16, null=True, blank=False)
    end_year = models.PositiveIntegerField(_("End year"), null=True, blank=False)
    currently_working_here = models.BooleanField(default=False)


    def __str__(self):
        return self.company_name



class JobseekerCertification(models.Model):
    profile = models.ForeignKey(
        'users.JobseekerProfile', 
        related_name='jobseeker_certifications',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=128, null=False, blank=False)
    certification_year = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return self.title



class JobseekerLanguage(models.Model):
    profile = models.ForeignKey(
        "users.JobseekerProfile", 
        on_delete=models.CASCADE,
        related_name='languages'
    )
    name = models.CharField(
        _("Language"),
        max_length=64,
        null=False,
        blank=False
    )
    proficiency_level = models.CharField(
        _("Proficiency Level"),
        max_length=48,
        choices=LANGUAGE_PROFICIENCY.choices,
        null=False, blank=False
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.first_name}'s Languages"
