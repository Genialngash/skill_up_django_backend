from utils.exceptions.handler import (
    choice_handler,
    email_handler,
    non_field_error_handler,
    passwords_handler,
    string_input_handler,
)


def handler(response):
    if 'email' in response.data:
        return email_handler(
            response, field_name='Email', data=response.data['email'][0])
    
    if 'password' in response.data:
        return passwords_handler(
            response, field_name='Password', data=response.data['password'][0])

    if 'log_in_as' in response.data:
        return choice_handler(
            response, field_name='log_in_as', data=response.data['log_in_as'][0])


    if 'non_field_errors' in response.data:
        return non_field_error_handler(
            response, data=response.data['non_field_errors'][0])

    return response
