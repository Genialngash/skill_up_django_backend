import datetime
from cmath import pi
from datetime import date
from urllib import response


# TODO Mark for depracation
def validate_year(year, **kwargs):
    todays_date = date.today()
    current_year = todays_date.year

    if year and isinstance(year, int):
        year = int(year)

        if year >=1960 and year <=current_year:
            return year

    return


def is_year(year, **kwargs):
    todays_date = date.today()
    current_year = todays_date.year # returns an int

    if year and isinstance(year, int):
        year = int(year)

        if year >=1960 and year <=current_year:
            return year

    return


def validate_end_year_payload(self, **kwargs):
    client_payload = self.initial_data
    end_year = is_year(client_payload['end_year'])
    start_year = is_year(client_payload['start_year'])

    if end_year and start_year:
        if start_year > end_year:
            return

        if end_year >= start_year:
            return end_year
    return


def validate_start_month_payload(self, **kwargs):
    client_payload = self.initial_data
    start_year = is_year(client_payload['start_year'])
    todays_date = date.today()
    current_year = todays_date.year # returns an int
    current_month_num = todays_date.month # returns numbers
    # current_month_str = todays_date.strftime("%B") # returns strings

    # User payload
    payload_month_num = datetime.datetime.strptime(client_payload['start_month'], '%B').month

    if start_year:
        if start_year == current_year:
            if payload_month_num > current_month_num:
                return

            if payload_month_num <= current_month_num:
                return client_payload['start_month']

        if start_year < current_year:
            return client_payload['start_month']

    return


def validate_month(self, **kwargs):
    client_payload = self.initial_data
    month_name_payload = kwargs.get('month')

    if not month_name_payload:
        return

    todays_date = date.today()
    current_year = todays_date.year # returns an int
    current_month_num = todays_date.month # returns numbers
    # current_month_str = todays_date.strftime("%B") # returns strings

    # User data
    user_month_num = datetime.datetime.strptime(month_name_payload, '%B').month


    if 'end_year' in client_payload:
        end_year = is_year(client_payload['end_year'])

        if end_year and end_year == current_year:
            if user_month_num > current_month_num:
                return

            if user_month_num <= current_month_num:
                return month_name_payload

        if end_year and end_year < current_year:
            return month_name_payload

    return
