from utils.exceptions.handler import string_input_handler


def handler(response):
    if 'verification_code' in response.data:
        return string_input_handler(
            response, field_name='Verification code', data=response.data['verification_code'][0])

    return response
