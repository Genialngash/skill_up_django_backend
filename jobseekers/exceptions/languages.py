
from utils.exceptions.handler import choice_handler, string_input_handler


def handler (response):
    if 'name' in response.data:
        data = response.data['name'][0]
        return string_input_handler(
            response,
            field_name='Language name',
            data=data
        )

    if 'proficiency_level' in response.data:
        data = response.data['proficiency_level'][0]
        return choice_handler(
            response,
            field_name='language_proficiency_level',
            data=data
        )

