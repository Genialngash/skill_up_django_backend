from django.db import models


class CONTRACT_TYPES(models.TextChoices):
    HOURLY_GIG = "Hourly Gig", "Hourly Gig"
    FULL_TIME = "Full Time", "Full Time"
    PART_TIME = "Part Time", "Part Time"
