from utils.exceptions.handler import (
    boolean_field_error_handler,
    choice_handler,
    date_field_error_handler,
    number_input_handler,
    related_field_input_error_handler,
    set_error_response,
    string_input_handler,
)


def handler(response):
    if 'responsibilities' in response.data:
        if 'required' in response.data['responsibilities'][0]:
            message='Job responsibilities is a required field.'
            data=response.data['responsibilities'][0]
            err = set_error_response(
                response, data=data, message=message,
            )

            response.data = err
            return response

        for res in response.data['responsibilities']:
            if 'text' in res:
                data = res['text'][0]

                return string_input_handler(
                    response, data=data, field_name='Resposibility text'
                )

    if 'company' in response.data:
        data = response.data['company'][0]

        return related_field_input_error_handler(
            response, data=data, field_name='Company'
        )

    if 'role' in response.data:
        data = response.data['role'][0]

        return string_input_handler(
            response, data=data, field_name='Job role'
        )

    if 'category' in response.data:
        data = response.data['category'][0]
        return string_input_handler(
            response, data=data, field_name='Job category'
        )

    if 'contract_type' in response.data:
        data = response.data['contract_type'][0]
        return choice_handler(
            response, data=data, field_name='Contract type'
        )

    if 'description' in response.data:
        data = response.data['description'][0]

        return string_input_handler(
            response, data=data, field_name='Job description'
        )

    if 'location' in response.data:
        data = response.data['location'][0]

        return string_input_handler(
            response, data=data, field_name='Job location'
        )

    if 'application_deadline' in response.data:
        data = response.data['application_deadline'][0]

        return date_field_error_handler(
            response, data=data, field_name='Application deadline'
        )

    if 'is_published' in response.data:
        data = response.data['is_published'][0]
        return boolean_field_error_handler(
            response, data=data, field_name='Is published'
        )

    if 'taken' in response.data:
        data = response.data['taken'][0]
        return boolean_field_error_handler(
            response, data=data, field_name='Taken'
        )

    if 'pay' in response.data:
        data = response.data['pay'][0]
        return number_input_handler(
            response, data=data, field_name='Pay'
        )

    return response
