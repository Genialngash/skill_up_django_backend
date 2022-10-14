from utils.exceptions.handler import boolean_field_error_handler


def handler(response):
    if 'mark_as_read' in response.data:
        return boolean_field_error_handler(
            response, field_name='mark_as_read', data=response.data['mark_as_read'][0])

    if 'mark_all_as_read' in response.data:
        return boolean_field_error_handler(
            response, field_name='mark_all_as_read', data=response.data['mark_all_as_read'][0])

    return response
