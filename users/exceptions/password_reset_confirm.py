from utils.exceptions.handler import passwords_handler, string_input_handler


def handler(response):
    if 'uid' in response.data:
        return string_input_handler(
            response, field_name='Uid', data=response.data['uid'][0])

    if 'token' in response.data:
        return string_input_handler(
            response, field_name='Token', data=response.data['token'][0])

    if 'new_password1' in response.data:
        return passwords_handler(
            response, field_name='New password', data=response.data['new_password1'][0])

    if 'new_password2' in response.data:
        return passwords_handler(
            response, field_name='Repeat new password', data=response.data['new_password2'][0])

    return response
