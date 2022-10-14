from utils.exceptions.handler import (
    boolean_field_error_handler,
    choice_handler,
    date_field_error_handler,
    invalid_file_field_error_handler,
    non_field_error_handler,
    string_input_handler,
)


def handler(response):
    if 'first_name' in response.data:
        return string_input_handler(
            response, field_name='First name', data=response.data['first_name'][0])

    if 'last_name' in response.data:
        return string_input_handler(
            response, field_name='Last name', data=response.data['last_name'][0])

    if 'avatar' in response.data:
        return invalid_file_field_error_handler(
            response, field_name='Avatar', data=response.data['avatar'][0])

    if 'birthday' in response.data:
        return date_field_error_handler(
            response, field_name='Birthday', data=response.data['birthday'][0])

    if 'gender' in response.data:
        return choice_handler(
            response, field_name='Gender', data=response.data['gender'][0])

    if 'logged_in_as' in response.data:
        return choice_handler(
            response, field_name='logged_in_as', data=response.data['logged_in_as'][0])


    if 'publish_jobseeker_profile' in response.data:
        return boolean_field_error_handler(
            response, field_name='Publish job card', data=response.data['publish_jobseeker_profile'][0])

    if 'non_field_errors' in response.data:
        return non_field_error_handler(
            response, data=response.data['non_field_errors'][0])

    return response
