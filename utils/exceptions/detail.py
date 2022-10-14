from utils.exceptions.handler import detail_error_handler


def handler(response):
    data = response.data['detail']
    return detail_error_handler(response, data=data,)
