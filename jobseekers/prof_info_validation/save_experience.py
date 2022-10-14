from jobseekers.models import WorkExperience


def create_experience(serializer, profile):
    print('Creating Out')

    if 'end_year' in serializer.validated_data and \
        'end_month' in serializer.validated_data and \
        serializer.validated_data['currently_working_here']:
        print('Creating One')

        WorkExperience.objects.create(
            profile=profile,
            start_year=serializer.validated_data['start_year'],
            start_month=serializer.validated_data['start_month'],
            end_month=serializer.validated_data['end_month'],
            end_year=serializer.validated_data['end_year'],
            company_name=serializer.validated_data['company_name'],
            currently_working_here = serializer.validated_data['currently_working_here']
        )


    if 'end_year' in serializer.validated_data and \
        'end_month' in serializer.validated_data and \
        not serializer.validated_data['currently_working_here']:
        print('Creating One')

        WorkExperience.objects.create(
            profile=profile,
            start_year=serializer.validated_data['start_year'],
            start_month=serializer.validated_data['start_month'],
            end_month=serializer.validated_data['end_month'],
            end_year=serializer.validated_data['end_year'],
            company_name=serializer.validated_data['company_name'],
            currently_working_here = serializer.validated_data['currently_working_here']
        )


    if 'end_year' not in serializer.validated_data and \
        'end_month' not in serializer.validated_data and \
        not serializer.validated_data['currently_working_here']:
        print('Creating Two')

        return {
            'error_code': 'invalid',
            'status': 'error',
            'status_code': 400,
            'message': 'Missing end month or end_year.'
        }


    if 'end_year' not in serializer.validated_data and \
        'end_month' not in serializer.validated_data and \
        serializer.validated_data['currently_working_here']:
        print('Creating Three')

        WorkExperience.objects.create(
            profile=profile,
            start_year=serializer.validated_data['start_year'],
            start_month=serializer.validated_data['start_month'],
            company_name=serializer.validated_data['company_name'],
            currently_working_here=serializer.validated_data['currently_working_here'],
        )


def update_experience(data, saved_exp):
    print('Updating')
    # print(data)


    if not 'end_year' in data and \
        data['currently_working_here'] == False:
        print('One')
        return {
            'error_code': 'invalid',
            'status': 'error',
            'status_code': 400,
            'message': 'End year is a required field.'
        }
    

    if 'end_month' not in data and \
        not data['currently_working_here']:
        print('Two')

        return {
            'error_code': 'invalid',
            'status': 'error',
            'status_code': 400,
            'message': 'End month is a required field.'
        }

    if 'end_year' in data and \
        'start_year' in data  and \
        data['start_year'] > \
        data['end_year']:
        return {
            'error_code': 'invalid',
            'status': 'error',
            'status_code': 400,
            'message': 'Start year cannot be greater than end year.'
        }

    if 'end_year' in data and \
        'end_month' in data and \
        data['currently_working_here']:

        print('Saving...end data')

        saved_exp.start_year=data['start_year']
        saved_exp.start_month=data['start_month']
        saved_exp.end_month=None
        saved_exp.end_year=None
        saved_exp.company_name=data['company_name']
        saved_exp.currently_working_here = data['currently_working_here']
        saved_exp.save()

    if 'end_year' not in data and \
        'end_month' not in data and \
        data['currently_working_here']:
        print('No Jon')
        # print(saved_exp)

        print(data['start_year'])
        print(type(data['start_year']))

        saved_exp.start_year = data['start_year']
        saved_exp.start_year = data['start_year']
        saved_exp.start_month=data['start_month']
        saved_exp.end_month=None
        saved_exp.end_year=None
        saved_exp.company_name=data['company_name']
        saved_exp.currently_working_here = data['currently_working_here']
        saved_exp.save()


    if 'end_year' in data and \
        'end_month' in data and \
        not data['currently_working_here']:

        print('Saving...end data here')

        saved_exp.start_year=data['start_year']
        saved_exp.start_month=data['start_month']
        saved_exp.end_month=data['end_month']
        saved_exp.end_year=data['end_year']
        saved_exp.company_name=data['company_name']
        saved_exp.currently_working_here = data['currently_working_here']
        saved_exp.save()
