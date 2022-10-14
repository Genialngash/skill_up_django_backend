from utils.exceptions.handler import (
    choice_handler,
    detail_error_handler,
    number_input_handler,
    string_input_handler,
)


def handler(response):
    if 'bio' in response.data:
        data = data=response.data['bio'][0]
        return string_input_handler(
            response, data=data, field_name='Bio'
        )

    if 'country' in response.data:
        data=response.data['country'][0]
        return string_input_handler(
            response, data=data, field_name='Country'
        )

    if 'education_level' in response.data:
        data=response.data['education_level'][0]
        return choice_handler(
            response, data=data, field_name='Education level'
        )

    if 'location' in response.data:
        data=response.data['location'][0]
        return string_input_handler(
            response, data=data, field_name='Location'
        )

    if 'profession' in response.data:
        data=response.data['profession'][0]
        return string_input_handler(
            response, data=data, field_name='Profession'
        )

    if 'hourly_rate' in response.data:
        data=response.data['hourly_rate'][0]
        return number_input_handler(
            response, data=data, field_name='Hourly rate'
        )

    if 'detail' in response.data:
        data=response.data['profession'][0]
        return detail_error_handler(
            response, data=data
        )
