import datetime
import random
import string
from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework.exceptions import APIException, ValidationError


class SimilarObject(ValidationError):
    status_code = 400
    default_detail = 'Similar record found.'
    default_code = 'duplicate'


# raise SimilarObject(
#         detail={'certifications': [
#             {
#                 'title': [f'Looks like this certification has already been saved in your profile.']
#             }
#         ]},
# )
