from utils.exceptions.handler import boolean_field_error_handler


def handler(response):
    if 'approved' in response.data:
        data=response.data['approved'][0]
        return boolean_field_error_handler(
            response, field_name='', data=data        
        )

    if 'card' in response.data:
        return response

    return response
