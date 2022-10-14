from utils.exceptions.handler import related_field_input_error_handler


def handler(response):
    if 'card' in response.data:
        data = response.data['card'][0]
        return related_field_input_error_handler(
            response, data=data, field_name='Card'
        )


    if 'user' in response.data:
        data = response.data['user'][0]
        return related_field_input_error_handler(
            response, data=data, field_name='User'
        )

    return response
