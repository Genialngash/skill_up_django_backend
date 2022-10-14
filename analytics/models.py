from django.db import models


class UserStatistics(models.Model):
    total_jobseekers = models.IntegerField(default=0)
    total_employers = models.IntegerField(default=0)

    def __str__(self):
        return 'Statistics'
