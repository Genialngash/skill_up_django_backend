def set_error_response(response, **kwargs):
    data = kwargs.get('data')
    message = kwargs.get('message')
    errors = {}
    errors['message'] = message
    errors['status'] = "error"
    errors['status_code'] = response.status_code
    errors['error_code'] = data.code
    return errors


def number_input_handler(response, **kwargs):
    """
    Handle errors in all fields that take numbers as inputs
    """
    possible_errors = ['required', 'invalid']
    field_name = kwargs.get('field_name')
    data = kwargs.get('data')
    error_messages = {
        'blank': f'{field_name} cannot be blank.',
        'required': f'{field_name} is a required field.',
        'invalid': f'Invalid {field_name.lower()} value.',
    }

    for err in possible_errors:
        if 'invalid value' in data.title().lower() and \
            field_name== 'Token':
            err = set_error_response(
                response, data=data,
                message='Token is invalid.'
            )
            response.data = err
            return response

        if err in data.code:
            err = set_error_response(
                response, data=data,
                message=error_messages[err]
            )
            response.data = err
            return response

    return response


def string_input_handler(response, **kwargs):
    """
    Handle errors in all fields that take strings as inputs
    """
    possible_errors = ['blank', 'required', 'invalid']
    field_name = kwargs.get('field_name')
    data = kwargs.get('data')
    error_messages = {
        'blank': f'{field_name} cannot be blank.',
        'required': f'{field_name} is a required field.',
        'invalid': f'Invalid {field_name.lower()} value.',
    }

    for err in possible_errors:
        if 'invalid value' in data.title().lower() and \
            field_name== 'Token':
            err = set_error_response(
                response, data=data,
                message='Token is invalid.'
            )
            response.data = err
            return response

        if err in data.code:
            err = set_error_response(
                response, data=data,
                message=error_messages[err]
            )
            response.data = err
            return response

    return response



def choice_handler(response, **kwargs):
    """
    Handle errors in all fields that take choices as inputs
    """
    possible_errors = ['invalid', 'blank', 'required', 'null']
    field_name = kwargs.get('field_name')
    data = kwargs.get('data')
    error_messages = {
        'blank': f'{field_name} cannot be blank.',
        'required': f'{field_name} is a required field.',
        'invalid': f'{field_name} not a valid choice.',
        'null': f'{field_name} cannot be null.',
    }

    print(response)
    print(data.code)

    for err in possible_errors:
        if err in data.code:
            err = set_error_response(
                response, data=data,
                message=error_messages[err]
            )
            response.data = err
            return response

    return response


def email_handler(response, **kwargs):
    """
    Handle errors in all fields that take an email as an input
    """
    possible_errors = ['invalid', 'blank', 'required']
    field_name = kwargs.get('field_name')
    data = kwargs.get('data')
    error_messages = {
        'blank': f'{field_name} cannot be blank.',
        'required': f'{field_name} is a required field.',
        'invalid': f'{field_name} is invalid.',
    }


    for err in possible_errors:
        if 'already registered' in data.title().lower():
            err = set_error_response(
                response, data=data,
                message='A user is already registered with this e-mail address.'
            )
            response.data = err
            return response


        if err in data.code:
            err = set_error_response(
                response, data=data,
                message=error_messages[err]
            )
            response.data = err
            return response

    return response



def passwords_handler(response, **kwargs):
    """
    Handle errors in all password fields
    """
    possible_errors = [
        'required',
        'blank',
        'too short',
        'password is too common',
        "two password fields didn't match", 
        'old password was entered incorrectly',
        'entirely numeric',
    ]

    field_name = kwargs.get('field_name')
    data = kwargs.get('data')

    error_messages = [
        f'{field_name} is a required field.',
        f'{field_name} cannot be blank.',
        "This password is too short. It must contain at least 8 characters.",
        'This password is too common.',
        'The password is too similar to your last name.',
        'Incorrect old password.',
        'This password is entirely numeric.',
        'The password is too similar to your email.'
    ]

    print(data.title().lower())

    for index, err in enumerate(possible_errors, 0):
        if err in data.title().lower():
            print('This is the error')
            print(index)
            possible_errors[index]
            error_messages[index]

            print(error_messages[index])

            err = set_error_response(
                response, data=data,
                message=error_messages[index]
            )
            response.data = err
            return response

    return response



def non_field_error_handler(response, **kwargs):
    """
    Handle all errors that are not related to a specific field
    """

    data = kwargs.get('data')
    possible_errors = [
        'provided credentials', # wrong credentials
        'is not verified', # unverified email
        "fields didn't match", # 2 password fields did not match
        'password is too similar to the first name', # weak password
        'password is too similar to the last name', # weak password
        'password is too similar to the email' # weak password
    ]

    error_messages = [
        'Unable to log in with the provided credentials.',
        'E-mail is not verified yet.',
        "The two password fields didn't match.",
        'The password is too similar to your first name.',
        'The password is too similar to your last name.',
        'The password is too similar to your email.' 
    ]

    for index, err in enumerate(possible_errors, 0):
        if err in data.title().lower():
            err = set_error_response(
                response, data=data,
                message=error_messages[index]
            )
            response.data = err
            return response

    return response


def related_field_input_error_handler(response, **kwargs):
    """
    Handle all errors from a related field input
    """

    data = kwargs.get('data')
    field_name = kwargs.get('field_name')
    possible_errors = ['required', 'null', 'does_not_exist', 'incorrect_type']
    print(response.data)

    error_messages = [
        f'{field_name} is a required field.',
        f'{field_name} cannot be null.',
        f"{field_name} provided does not exist.",
        f'Incorrect {field_name.lower()} type. Expected pk value but received str.',
    ]

    for index, err in enumerate(possible_errors, 0):
        if err in data.code:
            err = set_error_response(
                response, data=data,
                message=error_messages[index]
            )
            response.data = err
            return response

    return response




def detail_error_handler(response, **kwargs):
    """
    Handle general detail errors
    """

    print('GENERAL DETAIL HANDLER')

    data = kwargs.get('data')
    field_name = kwargs.get('field_name')
    possible_errors = [
        'method_not_allowed',
        'not_found',
        'unsupported_media_type',
        'parse_error',
        'permission_denied',
        'not_authenticated',
        'token_not_valid',
        'user_not_found'
    ]
    methods = ['post', 'put', 'get', 'patch', 'delete']

    # print(response.data)

    error_messages = {
        'method_not_allowed': 'Method not allowed.',
        'not_found': 'Resource not found.',
        'unsupported_media_type': 'Unsupported media type.',
        'parse_error': 'Error parsing the JSON payload.',
        'permission_denied': 'You are not authorized to perform this action.',
        'not_authenticated': 'Authentication credentials were not provided.',
        'token_not_valid': 'Token is invalid or expired.',
    }

    method_error_messages = {
        'get': 'Method GET not allowed.',
        'post': 'Method POST not allowed.',
        'patch': 'Method PATCH not allowed.',
        'put': 'Method PUT not allowed.',
        'delete': 'Method DELETE not allowed.',  
    }

    for index, err in enumerate(possible_errors, 0):
        if err in data.code:
            if err == 'not_found' and field_name == 'Key':
                err = set_error_response(
                    response, data=data,
                    message='Invalid key.'
                )
                response.data = err
                return response

            if err == 'method_not_allowed':
                for index, method in enumerate(methods, 0):
                    if method in data.title().lower():
                        err = set_error_response(
                            response, data=data,
                            message=method_error_messages[method]
                        )
                        response.data = err
                        return response
            
            else:
                err = set_error_response(
                    response, data=data,
                    message=error_messages[err]
                )
                response.data = err
                return response

    return response



def url_error_handler(response, **kwargs):
    data = kwargs.get('data')
    field_name = kwargs.get('field_name')
    possible_errors = ['required', 'blank', 'invalid', 'null']
    print(response.data)

    error_messages = {
        'blank': f'{field_name} cannot be blank.',
        'required': f'{field_name} is a required field.',
        'invalid': f"Enter a valid url.",
        'null': f"Enter a valid url.",
    }

    for index, err in enumerate(possible_errors, 0):
        if err in data.code:
            err = set_error_response(
                response, data=data,
                message=error_messages[err]
            )
            response.data = err
            return response

    return response


def invalid_file_field_error_handler(response, **kwargs):
    data = kwargs.get('data')
    field_name = kwargs.get('field_name')
    possible_errors = ['invalid',]
    print(response.data)

    error_messages = {
        'invalid': f'The submitted {field_name.lower()} was not a file. Check the encoding type on the form.'
    }
    
    for err in possible_errors:
        if err in data.code:
            err = set_error_response(
                response, data=data,
                message=error_messages[err]
            )
            response.data = err
            return response


def boolean_field_error_handler(response, **kwargs):
    data = kwargs.get('data')
    field_name = kwargs.get('field_name')
    possible_errors = ['invalid', 'required']

    error_messages = {
        'invalid': f'Invalid value. Use True or False',
        'required': f'{field_name} is a required field.',

    }

    for err in possible_errors:
        if err in data.code:
            err = set_error_response(
                response, data=data,
                message=error_messages[err]
            )
            response.data = err
            return response


def date_field_error_handler(response, **kwargs):
    data = kwargs.get('data')
    field_name = kwargs.get('field_name')
    possible_errors = ['invalid',]
    print(response.data)

    error_messages = {
        'invalid': f'{field_name} has wrong format. Use one of these formats instead: YYYY-MM-DD.'
    }
    
    for err in possible_errors:
        if err in data.code:
            err = set_error_response(
                response, data=data,
                message=error_messages[err]
            )
            response.data = err
            return response



def phone_number_field_error_handler(response, **kwargs):
    data = kwargs.get('data')
    field_name = kwargs.get('field_name')
    possible_errors = ['invalid',]
    print(response.data)

    error_messages = {
        'invalid': f'Invalid phone number.'
    }
    
    for err in possible_errors:
        if err in data.code:
            err = set_error_response(
                response, data=data,
                message=error_messages[err]
            )
            response.data = err
            return response




def year_field_error_handler(response, **kwargs):
    data = kwargs.get('data')
    field_name = kwargs.get('field_name')
    possible_errors = ['invalid', 'required']

    error_messages = {
        'invalid': f'Invalid {field_name.lower()}.',
        'required': f'{field_name} is a required field.'
    }
    
    for err in possible_errors:
        if err in data.code:
            err = set_error_response(
                response, data=data,
                message=error_messages[err]
            )
            response.data = err
            return response
