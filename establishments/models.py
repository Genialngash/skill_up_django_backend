from datetime import datetime

import googlemaps
import h3
import timeago
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, Thumbnail, resize
from utils.models import JobCardZoneMetadata, h3_resolutions

from .model_choices import CONTRACT_TYPES

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

class Company(models.Model):
    hiring_manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='companies', on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=False, blank=False)
    email = models.EmailField(max_length=128, null=False, blank=False)
    location = models.CharField(max_length=128)
    logo = ProcessedImageField(
        upload_to="media/establishments/companies/logo/%Y/%m/",
        processors=[Thumbnail(250, 250)],
        format="JPEG",
        options={"quality": 100},
        default="default_logo.jpg",
    )

    website_url = models.URLField(blank=True, null=True)
    bio = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = "Company"
        verbose_name_plural = "Companies"

from ckeditor.fields import RichTextField
from django.utils.timezone import make_naive


class JobCard(models.Model):
    company = models.ForeignKey(Company, related_name='company', on_delete=models.CASCADE)
    role = models.CharField(max_length=128, null=False, blank=False)
    category = models.CharField(max_length=255, null=False, blank=False)
    contract_type = models.CharField(_("Contract Type"),
        max_length=32, choices=CONTRACT_TYPES.choices,
        null=False, blank=False
    )
    description = models.TextField(null=False, blank=False)
    positions_available = models.PositiveIntegerField(default=1, null=False, blank=False)

    # Location
    location = models.CharField(blank=False, null=False, max_length=128)
    
    # TODO desc html
    # desc = RichTextField(config_name='awesome_ckeditor', null=True, blank=True)

    is_published = models.BooleanField(default=True)
    taken = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    application_deadline = models.DateField()
    pay = models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Job Card'
        verbose_name_plural = 'Job Cards'

    def __str__(self):
        return f'{self.role} at {self.company.name}'
    
    @property
    def time_since(self):
        now = datetime.now()
        time_ago = timeago.format(self.created_on.replace(tzinfo=None), now)
        return str(time_ago)

    @property
    def zone_metadata(self):
        return JobCardZoneMetadata.objects.get(job_card=self)


def populate_job_card_h3_zone(sender, instance, **kwargs):
    """Create and populate the h3 zones for a job card"""
    location_name = instance.location

    geocode_result = gmaps.geocode(location_name)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']


    print(lat, lng)
    if instance:
        try:
            zone_meta = JobCardZoneMetadata.objects.get(job_card=instance)
            print(zone_meta)
        except JobCardZoneMetadata.DoesNotExist:
            JobCardZoneMetadata.objects.create(
                job_card=instance,
                zone_one=h3.geo_to_h3(lat, lng, h3_resolutions['one']),
                zone_two=h3.geo_to_h3(lat, lng, h3_resolutions['two']),
                zone_three=h3.geo_to_h3(lat, lng, h3_resolutions['three']),
                zone_four=h3.geo_to_h3(lat, lng, h3_resolutions['four']),
                zone_five=h3.geo_to_h3(lat, lng, h3_resolutions['five']),
                zone_six=h3.geo_to_h3(lat, lng, h3_resolutions['six']),
                zone_seven=h3.geo_to_h3(lat, lng, h3_resolutions['seven']),
            )

post_save.connect(populate_job_card_h3_zone, sender=JobCard)

class CourseCard(models.Model):
    proffesional = models.ForeignKey(settings.EMPLOYER_PROFILE_MODEL, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=32, null=False, blank=False)
    course_description = models.TextField(null=False, blank=False)

    def __str__(self):
        return f'{self.course_name}'

class Enrolments(models.Model):
    course = models.ForeignKey(CourseCard, on_delete=models.CASCADE,db_constraint=False)
    by = models.ForeignKey(settings.JOBSEEKER_PROFILE_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.course.course_name} - {self.by.user.first_name}'

class LessonsModule(models.Model):
    course = models.ForeignKey(CourseCard, on_delete=models.CASCADE)
    lesson_name = models.CharField(max_length=32, null=False, blank=False)
    lesson_description = models.TextField(null=False, blank=False)

    def __str__(self):
        return f'{self.lesson_name}'


class Checker(models.Model):
    lesson = models.ForeignKey(LessonsModule, on_delete=models.CASCADE)
    enrolment = models.ForeignKey(Enrolments, on_delete=models.CASCADE,null=True, blank=True)

class JobResponsibility(models.Model):
    text = models.TextField(null=False, blank=False)
    card = models.ForeignKey(
        JobCard, 
        related_name='responsibilities', 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.text}' 


class JobApplication(models.Model):
    job_card = models.ForeignKey(JobCard, related_name='applications', on_delete=models.CASCADE)
    # the applicant of the job card
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{ self.user.first_name }'s Application at { self.job_card.company.name }"

    @property
    def user_profile(self):
        if self.user.u_type == 'General':
            return self.user.jobseeker_profile

        return None

    class Meta:
        ordering = ['-id']
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'



# def create_employee_on_application_approval(sender, instance, **kwargs):
#     """Create an Employee Record when their application is approved"""
#     # Check if it exists
#     if (instance.approved):
#         try:
#             Employee.objects.get(user=instance.user)
#         except Employee.DoesNotExist:
#             # TODO Notify the jobseeker
#             # Create an Employee
#             new_employee = Employee.objects.create(
#                 role=instance.card.role,
#                 company=instance.card.company,
#                 user=instance.user,
#             )

#             new_employee.save()

# post_save.connect(create_employee_on_application_approval, sender=JobApplication)


class Employee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=64, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    joined_on =  models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{ self.user.first_name } { self.user.last_name }"
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

class Completed(models.Model):
    lesson = models.ForeignKey(LessonsModule, on_delete=models.CASCADE)
    enrolment = models.ForeignKey(Enrolments, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"{self.lesson} - {self.enrolment}"
