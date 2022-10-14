from drf_spectacular.utils import OpenApiExample, extend_schema_serializer

jobseeker_examples = [
        OpenApiExample(
        'Update single Jobseeker profile',
        description=
            """This is the response you receive when you update a user profile successfully.""",
        value={
            'data': {
                "id": 0,
                "user": {
                    "id": 0,
                    "email": "admin@example.com",
                    "first_name": "string",
                    "last_name": "string",
                    "u_type": "string",
                    "avatar": "string",
                    "phone_number": "string",
                    "contact_is_verified": "bool",
                    "birthday": "string",
                    "logged_in_as": "string",
                    "gender": "string",
                    "publish_jobseeker_profile": "bool",
                },
                "bio": "string",
                "country": "string",
                "location": "string",
                "avg_rating": "5.42",
                "avatar": "string",
                "profession": "string",
                "education_level": "Primary School",
                "profile_completeness": 0,
                "hourly_rate": 0.0
            },
            'message': 'Sample message',
            'status': 'ok',
            'status_code': 200
        
        },
        request_only=False,
        response_only=True,
    ),
    OpenApiExample(
    'Get a single Jobseeker profile',
    description="""This is the response you receive when you make a Get request to fetch a user profile successfully.""",
    value={
        'data': {
            "id": 0,
            "user": {
                "id": 0,
                "email": "admin@example.com",
                "first_name": "string",
                "last_name": "string",
                "u_type": "string",
                "avatar": "string",
                "phone_number": "string",
                "contact_is_verified": "bool",
                "birthday": "string",
                "logged_in_as": "string",
                "gender": "string",
                "publish_jobseeker_profile": "bool"
            },
            "bio": "string",
            "country": "string",
            "location": "string",
            "avg_rating": "5.42",
            "avatar": "string",
            "profession": "string",
            "education_level": "Primary School",
            "profile_completeness": 0,
            "hourly_rate": 0.0
        },
        'message': 'Sample message',
        'status': 'ok',
        'status_code': 200
    },
    request_only=False,
    response_only=True,
    ),
]


employer_examples = [
    OpenApiExample(
    'Get a single Employer profile',
    description="""This is the response you receive when you make a Get request to fetch an employer profile successfully.""",
    value={
        'data': {
            "id": 0,
            "user": {
                "id": 0,
                "email": "email@example.com",
                "first_name": "string",
                "last_name": "string",
                "u_type": "string",
                "avatar": "string",
                "phone_number": "string",
                "contact_is_verified": "bool",
                "birthday": "string",
                "logged_in_as": "string",
                "gender": "string",
                "publish_jobseeker_profile": "bool"
            },
            "access_credits": [],
        },
        'message': 'string',
        'status': 'string',
        'status_code': 200
    },
    request_only=False,
    response_only=True,
    ),
]
