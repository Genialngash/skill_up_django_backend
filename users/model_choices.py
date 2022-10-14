from multiprocessing.sharedctypes import Value
from random import choices

from django.db import models


class MONTHS_OF_THE_YEAR(models.TextChoices):
    JANUARY = "January", "January"
    FEBRUARY = "February", "February"
    MARCH = "March", "March"
    APRIL = "April", "April"
    MAY = "May", "May"
    JUNE = "June", "June"
    JULY = "July", "July"
    AUGUST = "August", "August"
    SEPTEMBER = "September", "Jobseeker"
    OCTOBER = "October", "October"
    NOVEMBER = "November", "November"
    DECEMBER = "December", "December"


class LANGUAGE_PROFICIENCY(models.TextChoices):
    ELEMENTARY_PROFICIENCY = "Elementary Proficiency", "Elementary Proficiency"
    LIMITED_WORKING_PROFICIENCY = "Limited Working Proficiency", "Limited Working Proficiency"
    PROFESSIONAL_WORKING_PROFICIENCY = "Professional Working Proficiency", "Professional Working Proficiency"
    FULL_PROFESSIONAL_PROFICIENCY = "Full Professional Proficiency", "Full Professional Proficiency"
    NATIVE_OR_BILINGUAL_FLUENCY = "Native or Bilingual Fluency", "Native or Bilingual Fluency"


class LOGGED_IN_AS(models.TextChoices):
    EMPLOYER = "Employer", "Employer"
    JOBSEEKER = "Jobseeker", "Jobseeker"
    VEETA_STAFF = "Veeta Staff", "Veeta Staff"
    VEETA_SUPER_USER = "Veeta Superuser"

class USER_TYPES(models.TextChoices):
    GENERAL = "General", "General"
    VEETA_STAFF = "Veeta Staff", "Veeta Staff"
    VEETA_SUPER_USER = "Veeta Superuser"

class GENDER_TYPES(models.TextChoices):
    MALE = "Male", "Male"
    FEMALE = "Female", "Female"
    NON_BINARY = "Non Binary", "Non Binary"
    UNSPECIFIED = "Unspecified", "Unspecified"


class CURRENCY_TYPES(models.TextChoices):
    USD = "U.S. Dollar", "U.S. Dollar"
    BRITISH_POUND = "British Pound", "British Pound"


# Jobseekers
class EDUCATION_LEVEL(models.TextChoices):
    UNSPECIFIED_ED_LEVEL = "Unspecified", "Unspecified"
    PRIMARY_SCHOOL = "Primary School", "Primary School"
    SECONDARY_SCHOOL = "Secondary School", "Secondary School"
    UNDERGRADUATE_DEGREE = "Undergraduate Degree", "Undergraduate Degree"
    MASTERS_DEGREE = "Masters Degree", "Masters Degree"
