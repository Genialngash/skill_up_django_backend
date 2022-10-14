from django.contrib.auth.models import BaseUserManager
from django.db import models

from .model_choices import USER_TYPES


# User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("users must have an email address!")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.is_staff = False
        user.is_superuser = False
        user.u_type = USER_TYPES.GENERAL
        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_superuser(self, email, password, **extra_fields):
        """Create and save a new super user"""
        if not email:
            raise ValueError("Users must have an email address!")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.u_type = USER_TYPES.VEETA_SUPER_USER
        user.set_password(password)
        user.save(using=self.db)

        return user


# Employer Managers
class EmployerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(u_type=USER_TYPES.GENERAL)
        )

# Jobseeker Managers
class JobseekerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(u_type=USER_TYPES.GENERAL)
        )
