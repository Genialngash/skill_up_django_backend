from utils.exceptions import handler


def handler(response):
    if 'job_card' in response.data:
        return handler.related_field_input_error_handler(
            response,
            data=response.data['job_card'][0],
            field_name='Job card'
        )

    if 'user' in response.data:
        return handler.related_field_input_error_handler(
            response,
            data=response.data['user'][0],
            field_name='User'
        )

    return response
