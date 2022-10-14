from utils.exceptions.handler import string_input_handler


def handle_jwt_errors(response):
    print('JWT HANDLER')
    # if 'detail' in response.data:
    #     if 'invalid or expired' in response.data['detail'].title().lower():
    #         err = set_error_response(
    #             response, data=response.data['detail'],
    #             message='Token is invalid or expired.'
    #         )
    #         response.data = err
    #         return response

    #     if response.data['detail'].code == 'token_not_valid':
    #         err = set_error_response(
    #             response, data=response.data['detail'],
    #             message='No valid refresh token found.'
    #         )
    #         response.data = err
    #         return response

    if 'refresh' in response.data:
        return string_input_handler(
            response, data=response.data['refresh'][0], field_name='Refresh')

    if 'token' in response.data:
        return string_input_handler(
            response, data=response.data['token'][0], field_name='Token')

    return response
