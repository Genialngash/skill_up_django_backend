from utils.exceptions.handler import number_input_handler, string_input_handler


def handler(response):
    if 'jobseeker' in response.data:
        data = response.data['jobseeker'][0]
        return number_input_handler(response, data=data, field_name='Jobseeker')

    if 'unlock_code' in response.data:
        data = response.data['unlock_code'][0]
        return string_input_handler(response, data=data, field_name='Unlock code')
    
    return response
