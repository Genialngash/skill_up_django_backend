from utils.exceptions.handler import (
    boolean_field_error_handler,
    choice_handler,
    string_input_handler,
    year_field_error_handler,
)


def handler(response):
    if 'currently_working_here' in response.data:
        data = response.data['currently_working_here'][0]
        return boolean_field_error_handler(
            response,
            field_name='Currently working here',
            data=data
        )

    if 'company_name' in response.data:
        data = response.data['company_name'][0]
        return string_input_handler(
            response,
            field_name='Company name',
            data=data
        )

    if 'start_month' in response.data:
        data = response.data['start_month'][0]
        return choice_handler(
            response,
            field_name='Start month',
            data=data
        )

    if 'start_year' in response.data:
        data = response.data['start_year'][0]
        return year_field_error_handler(
            response,
            field_name='Start year',
            data=data
        )

    if 'end_year' in response.data:
        data = response.data['end_year'][0]
        return year_field_error_handler(
            response,
            field_name='End year',
            data=data
        )

    if 'end_month' in response.data:
        data = response.data['end_month'][0]
        return choice_handler(
            response,
            field_name='End month',
            data=data
        )

    return response
