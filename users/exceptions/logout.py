from utils.exceptions.handler import set_error_response


def handler(response):
    print('LOGOUT HANDLER')
    if response.data['code'] == 'token_not_valid':
        err =  set_error_response(
            response, data=response.data
        )
        response.data = err
        return response

    return response
