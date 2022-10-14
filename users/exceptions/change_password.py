from utils.exceptions.handler import passwords_handler


def handler(response):
    if 'new_password1' in response.data:
        return passwords_handler(
            response, field_name='New password', data=response.data['new_password1'][0])

    if 'new_password2' in response.data:
        return passwords_handler(
            response, field_name='Repeat new password', data=response.data['new_password2'][0])

    if 'old_password' in response.data:
        return passwords_handler(
            response, field_name='Old password', data=response.data['old_password'][0])

    return response
