
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer

job_applications_examples = [
    OpenApiExample(
    'Retrieve a job application',
    description=
        """This is the response you retrieve a single job applications.""",
    value={
        "data": {
            "id": 0,
            "approved": 'bool',
            "card": {
                "id": 0,
                "role": "String",
                "category": "String",
                "contract_type": "Hourly Gig",
                "location": "String",
                "created_on": "2022-04-11",
                "updated_on": "2022-04-11",
                "application_deadline": "2022-04-11",
                "is_published": 'bool',
                "taken": 'bool',
                "company": {
                    "id": 0,
                    "name": "Palmer Group"
                },
                "responsibilities": [
                    {
                    "text": "Review products."
                    }
                ]
            },
            "user": {
                "id": 0,
                "first_name": "Douglas",
                "last_name": "Douglas",
                "u_type": "Jobseeker"
            },
        },
        "message": "Sample message",
        "status": "ok",
        "status_code": 200
    },
    request_only=False,
    response_only=True,
    ),
     OpenApiExample(
    'List job applications',
    description=
        """This is the response you list job applications.""",
    value={
        "data": {
            "count": 0,
            "next": 'null',
            "previous": 'null',
            "results": [
                {
                    "id": 8,
                    "card": {
                    "id": 115,
                    "role": "Reviewer",
                    "category": "General",
                    "contract_type": "Hourly Gig",
                    "location": "Review products.",
                    "created_on": "2022-04-11T15:10:08.630867Z",
                    "updated_on": "2022-04-11T15:10:08.630916Z",
                    "application_deadline": "2022-04-11",
                    "is_published": 'bool',
                    "taken": 'bool',
                    "company": {
                        "id": 25,
                        "name": "Company Name"
                    },
                    "responsibilities": [
                        {
                        "text": "String"
                        }
                    ]
                    },
                    "user": {
                        "id": 0,
                        "first_name": "String",
                        "last_name": "String",
                        "u_type": "Jobseeker"
                    },
                    "approved": 'false'
                },
            ]
        },
        "message": "Sample message.",
        "status": "ok.",
        "status_code": 200
    },
    request_only=False,
    response_only=True,
    ),
]


job_card_examples = [
    OpenApiExample(
    'List job cards',
    description=
        """This is the response you get when you list job cards successfully.""",
    value={
        'data': {
            "current_page": 0,
            "previous_page": None,
            "next_page": None,
            "count": 0,
            "results": [
                {
                    "id": 0,
                    "company": {
                        "name": "string",
                        "logo": "string",
                        "bio": "string"
                    },
                    "role": "string",
                    "category": 0,
                    "contract_type": "Hourly Gig",
                    "responsibilities": [
                        {
                        "text": "string"
                        }
                    ],
                    "description": "string",
                    "location": "string",
                    "created_on": "2022-04-09T13:06:05.564Z",
                    "updated_on": "2022-04-09T13:06:05.564Z",
                    "application_deadline": "2022-04-09",
                    "is_published": "bool",
                    "taken": "bool"
                }
            ]                
        },
        'message': 'Sample message',
        'status': 'ok',
        'status_code': 200
    },
    request_only=False,
    response_only=True,
    ),
    OpenApiExample(
    'Create a job card success',
    description=
        """This is the response you create a job card successfully.""",
    value={
        "data": {
            "id": 0,
            "company": {
                "name": "string",
                "logo": "string",
                "bio": "string"
            },
            "role": "string",
            "category": 0,
            "contract_type": "Hourly Gig",
            "responsibilities": [
                {
                "text": "string"
                }
            ],
            "description": "string",
            "location": "string",
            "created_on": "2022-04-09T13:06:05.564Z",
            "updated_on": "2022-04-09T13:06:05.564Z",
            "application_deadline": "2022-04-09",
            "is_published": "bool",
            "taken": "bool"
        },
        "status": "ok",
        "status_code": 201,
        "message": "Job card created successfully."
    },
    request_only=False,
    response_only=True,
    ),
    OpenApiExample(
    'Create a job card failure',
    description=
        """This is the response a failure occurs creating a job card.""",
    value={
        "message": "Error message.",
        "status": "error",
        "status_code": 400,
        "error_code": "error_code"
    },
    request_only=False,
    response_only=True,
    ),
]

