from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from establishments.models import Company
from users.models import JobseekerProfile


class RATINGS (models.IntegerChoices):
    ONE_STAR = 1
    TWO_STARS = 2
    THREE_STARS = 3
    FOUR_STARS = 4
    FIVE_STARS = 5

class JobseekerRating(models.Model):
    jobseeker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='jobseeker_rating', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATINGS.choices, null=False, blank=False)
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.jobseeker.email

    class Meta:
        ordering = ['-id']
        verbose_name = 'Jobseeker Rating'
        verbose_name_plural = 'Jobseeker Ratings'


class CompanyRating(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATINGS.choices, null=False, blank=False)
    jobseeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.company.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Company Rating'
        verbose_name_plural = 'Company Ratings'


# Signals
def update_jobseeker_rating(sender, instance, **kwargs):
    """
    A signal that creates a user average rating record for a 
    jobseeker once the profile is made.
    """

    # grab the profile
    jobseeker_profile = JobseekerProfile.objects.get(user=instance.jobseeker.id)
    current_rating = jobseeker_profile.avg_rating
    current_total_raters = jobseeker_profile.total_ratings

    # increment total raters
    new_raters = current_total_raters + 1

    # new rating
    new_rating = instance.rating

    # total sum of ratings
    old_sum_of_ratings = current_total_raters * current_rating
    new_sum_of_ratings = old_sum_of_ratings + new_rating

    new_average = new_sum_of_ratings / new_raters

    # update model
    jobseeker_profile.total_ratings = new_raters
    jobseeker_profile.avg_rating = new_average
    jobseeker_profile.save()

post_save.connect(update_jobseeker_rating, sender=JobseekerRating)
