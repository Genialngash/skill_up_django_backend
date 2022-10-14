from jobseekers.models import JobseekerCertification


def handler(**kwargs):
    data = kwargs.get('data')
    cert_serializer = kwargs.get('cert_serializer')
    profile = kwargs.get('profile')

    if 'certifications' in data:
        if len(data['certifications']) == 0:
            # Delete all
            saved_certs = JobseekerCertification.objects.filter(
                profile=profile
            )

            if len(saved_certs) > 0:
                for cert in saved_certs:
                    cert.delete()

                    return None

            return None

        if len(data['certifications']) > 0:
            saved_certs = JobseekerCertification.objects.filter(
                profile=profile
            )

            if len(saved_certs) == 0:
                # Create new user languages
                print('Create New....')
                for index, lang in enumerate(data['certifications'], start=0):
                    serializer = cert_serializer(data=data['certifications'][index])
                    serializer.is_valid(raise_exception=True)

                    JobseekerCertification.objects.create(
                        title=serializer.data['title'],
                        profile=profile,
                        certification_year=serializer.data['certification_year'],
                    )

                return None


            total_saved = len(saved_certs) # 3
            new_total = len(data['certifications']) # 4

            if new_total < total_saved:
                len_diff = abs(new_total - total_saved)
                delete_from_index = ((total_saved - 1) - len_diff) + 1

                # Delete extra entries
                for index in range(delete_from_index, len(saved_certs)):
                    saved_certs[index].delete()

                updated_entries = JobseekerCertification.objects.filter(
                    profile=profile
                )

                # Update remaining entries
                for index, cert in enumerate(updated_entries, start=0):
                    serializer = cert_serializer(data=data['certifications'][index])
                    serializer.is_valid(raise_exception=True)
                    cert.title = serializer.data['title']
                    cert.certification_year = serializer.data['certification_year']
                    cert.save()

                    return None


            if new_total == total_saved:
                # Update existing entries
                for index, cert in enumerate(saved_certs, start=0):
                    serializer = cert_serializer(data=data['certifications'][index])
                    serializer.is_valid(raise_exception=True)
                    cert.title = serializer.data['title']
                    cert.certification_year = serializer.data['certification_year']
                    cert.save()

                return None


            if new_total > total_saved:
                len_diff = abs(new_total - total_saved)     
                create_from_index = (total_saved - 1) + 1

                # Update existing entries
                for index, cert in enumerate(saved_certs, start=0):
                    serializer = cert_serializer(data=data['certifications'][index])
                    serializer.is_valid(raise_exception=True)

                    cert.title = serializer.data['title']
                    cert.certification_year = serializer.data['certification_year']
                    cert.save()


                # Create extra records
                for index in range(create_from_index, len(data['certifications'])):
                    serializer = cert_serializer(data=data['certifications'][index])
                    serializer.is_valid(raise_exception=True)

                    JobseekerCertification.objects.create(
                        profile=profile,
                        title=serializer.data['title'],
                        certification_year=serializer.data['certification_year']
                    )


                return None
