import random
import string
from datetime import date, datetime, timedelta

from django.utils import timezone


def generate_random_code():
    chars = string.ascii_letters
    digits = string.digits
    choice_set = chars + digits
    return ''.join(random.choice(choice_set) for x in range(16))


def check_code_expiry(access_credit):
    expired = False
    todays_date = timezone.now()
    expires_on = access_credit.expires_on + timedelta(minutes=5)
    days_diff = ((expires_on - todays_date).days)

    print(f"The diff in days is {days_diff}")

    if days_diff > 0:
        expired = False
        return expired

    if days_diff < 0:
        expired = True
        return expired

    if days_diff == 0:
        current_time = todays_date.strftime("%H:%M:%S")
        expire_time = expires_on.strftime("%H:%M:%S")

        # print(current_time)
        # print(expire_time)
        # print(f"Current time is NOT past the expire time: " + str(current_time <= expire_time))

        if (current_time <= expire_time):
            expired = False
            return expired
        else:
            expired = True
            return expired

    return expired
