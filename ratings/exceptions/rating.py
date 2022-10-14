from utils.exceptions.handler import choice_handler, related_field_input_error_handler


def handler(response):
    if 'rating' in response.data:
        return choice_handler(
            response, field_name='Rating', data=response.data['rating'][0])

    if 'jobseeker' in response.data:
        return related_field_input_error_handler(
            response, field_name='Jobseeker', data=response.data['jobseeker'][0])

    if 'employer' in response.data:
        return related_field_input_error_handler(
            response, field_name='Employer', data=response.data['employer'][0])

    return response
