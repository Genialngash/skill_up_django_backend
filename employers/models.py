from django.conf import settings
from django.db import models


class JobOffer(models.Model):
    job_card = models.ForeignKey(settings.JOB_CARD_MODEL, on_delete=models.CASCADE)
    job_application = models.ForeignKey(settings.JOB_APPLICATION_MODEL, on_delete=models.CASCADE)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on_timestamp = models.DateTimeField(auto_now_add=True)

    accepted_at_timestamp = models.DateTimeField(null=True, blank=False)  # Job applicant modifies this
    is_accepted = models.BooleanField(default=False)  # Job applicant modifies this


    def __str__(self):
        return f"{self.applicant.first_name} {self.applicant.last_name}'s job offer at {self.job_card.company.name}"

    class Meta:
        ordering = ['-id']
        verbose_name = 'Job Offer'
        verbose_name_plural = 'Job Offers'
