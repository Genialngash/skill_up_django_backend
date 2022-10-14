from utils.exceptions.handler import choice_handler, string_input_handler


def handler(response):
    print(response.data)
    if 'phone_number' in response.data:
        return string_input_handler(
            response, field_name='Phone number', data=response.data['phone_number'][0])
    
    if 'channel' in response.data:
        return choice_handler(
            response, field_name='Channel', data=response.data['channel'][0])

    return response
