from jobseekers.models import JobseekerLanguage
from utils.common import calculate_profile_completeness


def handler(**kwargs):
    data = kwargs.get('data')
    lang_serializer = kwargs.get('lang_serializer')
    profile = kwargs.get('profile')
    user = kwargs.get('user')

    if 'languages' in data:
        if len(data['languages']) == 0:
            # Delete all
            saved_languages = JobseekerLanguage.objects.filter(
                profile=profile
            )

            if len(saved_languages) > 0:
                for lang in saved_languages:
                    lang.delete()

                completeness = calculate_profile_completeness(user, profile)
                jobseeker_profile = profile
                jobseeker_profile.profile_completeness = completeness
                jobseeker_profile.save()
                return
            return

        if len(data['languages']) > 0:
            saved_languages = JobseekerLanguage.objects.filter(
                profile=profile
            )

            if len(saved_languages) == 0:
                # Create new user languages
                print('Create New....')
                for index, lang in enumerate(data['languages'], start=0):
                    serializer = lang_serializer(data=data['languages'][index])
                    serializer.is_valid(raise_exception=True)

                    JobseekerLanguage.objects.create(
                        profile = profile,
                        name = serializer.data['name'],
                        proficiency_level = serializer.data['proficiency_level']
                    )


                completeness = calculate_profile_completeness(user, profile)
                jobseeker_profile = profile
                jobseeker_profile.profile_completeness = completeness
                jobseeker_profile.save()

                return


            total_saved = len(saved_languages) # 3
            new_total = len(data['languages']) # 4

            if new_total < total_saved:
                len_diff = abs(new_total - total_saved)
                delete_from_index = ((total_saved - 1) - len_diff) + 1

                # Delete extra entries
                for index in range(delete_from_index, len(saved_languages)):
                    saved_languages[index].delete()

                updated_entries = JobseekerLanguage.objects.filter(
                    profile=profile
                )

                # Update remaining entries
                for index, lang in enumerate(updated_entries, start=0):
                    serializer = lang_serializer(data=data['languages'][index])
                    serializer.is_valid(raise_exception=True)
                    lang.name = serializer.data['name']
                    lang.proficiency_level = serializer.data['proficiency_level']
                    lang.save()

                completeness = calculate_profile_completeness(user, profile)
                jobseeker_profile = profile
                jobseeker_profile.profile_completeness = completeness
                jobseeker_profile.save()

                return


            if new_total == total_saved:
                # Update existing entries
                for index, lang in enumerate(saved_languages, start=0):
                    serializer = lang_serializer(data=data['languages'][index])
                    serializer.is_valid(raise_exception=True)

                    lang.name = serializer.data['name']
                    lang.proficiency_level = serializer.data['proficiency_level']
                    lang.save()

                return


            if new_total > total_saved:
                len_diff = abs(new_total - total_saved)     
                create_from_index = (total_saved - 1) + 1

                # Update existing entries
                for index, lang in enumerate(saved_languages, start=0):
                    serializer = lang_serializer(data=data['languages'][index])
                    serializer.is_valid(raise_exception=True)
                    lang.name = serializer.data['name']
                    lang.proficiency_level = serializer.data['proficiency_level']
                    lang.save()


                # Create extra records
                for index in range(create_from_index, len(data['languages'])):
                    serializer = lang_serializer(data=data['languages'][index])
                    serializer.is_valid(raise_exception=True)

                    JobseekerLanguage.objects.create(
                        profile=profile,
                        name=serializer.data['name'],
                        proficiency_level=serializer.data['proficiency_level']
                    )


                completeness = calculate_profile_completeness(user, profile)
                jobseeker_profile = profile
                jobseeker_profile.profile_completeness = completeness
                jobseeker_profile.save()

                return
