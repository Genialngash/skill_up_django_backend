
from utils.exceptions.handler import email_handler


def handler(response):
    if 'email' in response.data:
        return email_handler(
            response, field_name='Email', data=response.data['email'][0])

    return response
