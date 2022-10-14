from django.conf import settings
from django.db import models


class UserAccessCredit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    email = models.EmailField(null=True, blank=True)
    unlock_code = models.CharField(max_length=32, null=True, blank=False)
    total_unlocks = models.PositiveIntegerField(default=0, null=False, blank=False)
    job_cards = models.PositiveIntegerField(default=0, null=False, blank=False)
    is_valid = models.BooleanField(default=False)
    tag = models.CharField(max_length=32, null=False, blank=False)
    created_on = models.DateTimeField(null=True, blank=True)
    expires_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.unlock_code}"
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'User Access Credit'
        verbose_name_plural = 'User Access Credits'


class UnlockedProfile(models.Model):
    access_credit = models.ForeignKey(UserAccessCredit, on_delete=models.CASCADE)
    profile = models.ForeignKey("users.JobseekerProfile", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.access_credit.unlock_code

    class Meta:
        ordering = ['-id']
        verbose_name = 'Unlocked Profile'
        verbose_name_plural = 'Unlocked Profiles'
