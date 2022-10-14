from django.conf import settings
from django.db import models


class JobBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_card = models.ForeignKey(settings.JOB_CARD_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Job Bookmark'
        verbose_name_plural = 'Job Bookmarks'
