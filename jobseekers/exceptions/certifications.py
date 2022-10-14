from utils.exceptions.handler import string_input_handler, year_field_error_handler


def handler(response):
    print(response.data)
    if 'title' in response.data:
        data = response.data['title'][0]
        return string_input_handler(
            response,
            field_name='Certification title',
            data=data
        )

    if 'certification_year' in response.data:
        print(response.data['certification_year'][0].code)

        data = response.data['certification_year'][0]
        return year_field_error_handler(
            response,
            field_name='Certification year',
            data=data
        )

    return response
