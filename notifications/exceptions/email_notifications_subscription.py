from utils.exceptions.handler import boolean_field_error_handler


def handler(response):
    if 'new_job_application' in response.data:
        return boolean_field_error_handler(
            response, field_name='new_job_application', data=response.data['new_job_application'][0])

    return response
