from utils.exceptions.handler import (
    email_handler,
    invalid_file_field_error_handler,
    related_field_input_error_handler,
    string_input_handler,
    url_error_handler,
)


def handler(response):
    if 'name' in response.data:
        return string_input_handler(
            response, data=response.data['name'][0], field_name='Company name')

    if 'logo' in response.data:
        return invalid_file_field_error_handler(
            response, data=response.data['logo'][0], field_name='Company logo')

    if 'email' in response.data:
        return email_handler(
            response, field_name='Email', data=response.data['email'][0])

    if 'website_url' in response.data:
        return url_error_handler(
            response,
            field_name='Company website',
            data=response.data['website_url'][0]
        )

    if 'bio' in response.data:
        return string_input_handler(
            response, data=response.data['bio'][0], field_name='Company bio')

    if 'hiring_manager' in response.data:
        return related_field_input_error_handler(
            response,
            data=response.data['hiring_manager'][0],
            field_name='Company hiring manager'
        )

    return response
