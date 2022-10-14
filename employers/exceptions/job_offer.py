from utils.exceptions.handler import related_field_input_error_handler


def handler (response):
    if 'job_card' in response.data:
        data = response.data['job_card'][0]
        return related_field_input_error_handler(
            response,
            field_name='Job card',
            data=data
        )

    if 'job_application' in response.data:
        data = response.data['job_application'][0]
        return related_field_input_error_handler(
            response,
            field_name='Job application',
            data=data
        )

    if 'applicant' in response.data:
        data = response.data['applicant'][0]
        return related_field_input_error_handler(
            response,
            field_name='Applicant',
            data=data
        )

    return response
