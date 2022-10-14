from utils.exceptions.handler import detail_error_handler, string_input_handler


def handler(response):
    if 'key' in response.data:
        data = response.data['key'][0]
        return string_input_handler(
            response, data=data, field_name='Key'
        )

    if 'detail' in response.data:
        data = response.data['detail'][0]
        return detail_error_handler(
            response, data=data, field_name='Key'
        )

    return response
