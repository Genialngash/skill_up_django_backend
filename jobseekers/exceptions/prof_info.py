from .certifications import handler as certifications_handler
from .languages import handler as language_handler
from .work_experience import handler as work_experience_handler


def handler(response):
    if 'name' in response.data or \
        'proficiency_level' in response.data:
        return language_handler(response) 

    if 'company_name' in response.data or \
        'start_month' in response.data or \
        'start_year' in response.data or \
        'end_month' in response.data or \
        'end_year' in response.data or \
        'currently_working_here' in response.data:
        return work_experience_handler(response) 

    if 'title' in response.data or \
        'certification_year' in response.data:
        return certifications_handler(response) 

    return response
