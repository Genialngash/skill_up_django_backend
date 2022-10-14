from tabnanny import verbose

from django.conf import settings
from django.db import models

"""
resolution_1 represents the biggest area in sq km
This transaltes zone_seven to be the biggest area in sq km
"""

h3_resolutions = {
    'one': 7, # smallest area is sq km
    'two': 6,
    'three': 5,
    'four': 4,
    'five': 3,
    'six': 2,
    'seven': 1, # biggest area is sq km
}

class JobseekerZoneMetadata(models.Model):
    profile = models.OneToOneField(settings.JOBSEEKER_PROFILE_MODEL, related_name='zone_metadata', on_delete=models.CASCADE)
    zone_one = models.CharField(max_length=256, blank=False, null=False)
    zone_two = models.CharField(max_length=256, blank=False, null=False)
    zone_three = models.CharField(max_length=256, blank=False, null=False)
    zone_four = models.CharField(max_length=256, blank=False, null=False)
    zone_five = models.CharField(max_length=256, blank=False, null=False)
    zone_six = models.CharField(max_length=256, blank=False, null=False)
    zone_seven = models.CharField(max_length=256, blank=False, null=False)
    
    def __str__(self):
        return f"{self.profile.user.first_name}' H3 Data"

    class Meta:
        verbose_name = 'Jobseeker Zone Metadata'
        verbose_name_plural = 'Jobseeker Zone Metadata'


class JobCardZoneMetadata(models.Model):
    job_card = models.OneToOneField(settings.JOB_CARD_MODEL, related_name='zone_metadata', on_delete=models.CASCADE)
    zone_one = models.CharField(max_length=256, blank=False, null=False)
    zone_two = models.CharField(max_length=256, blank=False, null=False)
    zone_three = models.CharField(max_length=256, blank=False, null=False)
    zone_four = models.CharField(max_length=256, blank=False, null=False)
    zone_five = models.CharField(max_length=256, blank=False, null=False)
    zone_six = models.CharField(max_length=256, blank=False, null=False)
    zone_seven = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self):
        return f"{self.job_card.role} H3 Data"

    class Meta:
        verbose_name = 'Job Card Zone Metadata'
        verbose_name_plural = 'Job Card Zone Metadata'

