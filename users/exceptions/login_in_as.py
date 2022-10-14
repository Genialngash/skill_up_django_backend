from utils.exceptions.handler import choice_handler


def handler(response):
    if 'log_in_as' in response.data:
        return choice_handler(
            response, field_name='log_in_as', data=response.data['log_in_as'][0])
    
    return response
