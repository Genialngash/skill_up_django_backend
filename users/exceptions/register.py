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

    if 'password1' in response.data:
        return passwords_handler(
            response, field_name='Password', data=response.data['password1'][0])


    if 'password2' in response.data:
        return passwords_handler(
            response, field_name='Repeat password', data=response.data['password2'][0])


    if 'first_name' in response.data:
        return string_input_handler(
            response, field_name='First name', data=response.data['first_name'][0])

    if 'last_name' in response.data:
        return string_input_handler(
            response, field_name='Last name', data=response.data['last_name'][0])


    if 'u_type' in response.data:
        return choice_handler(
            response, field_name='User type', data=response.data['u_type'][0])

    if 'non_field_errors' in response.data:
        return non_field_error_handler(
            response, data=response.data['non_field_errors'][0])

    return response
