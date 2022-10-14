from jobseekers.models import WorkExperience

from .save_experience import create_experience, update_experience


def handler(**kwargs):
    data = kwargs.get('data')
    work_experience_serializer = kwargs.get('work_experience_serializer')
    profile = kwargs.get('profile')
    user = kwargs.get('user')


    if 'work_experience' in data:
        if len(data['work_experience']) == 0:
            # Delete all
            saved_work_exp = WorkExperience.objects.filter(
                profile=profile
            )

            if len(saved_work_exp) > 0:
                for xp in saved_work_exp:
                    xp.delete()

                return

            return None

        if len(data['work_experience']) > 0:
            saved_work_exp = WorkExperience.objects.filter(
                profile=profile
            )

            if len(saved_work_exp) == 0:
                # Create new user languages
                print('Create New....')
                for index, lang in enumerate(data['work_experience'], start=0):
                    serializer = work_experience_serializer(data=data['work_experience'][index])
                    serializer.is_valid(raise_exception=True)
                    create_experience(serializer, profile)

                return


            total_saved = len(saved_work_exp) # 3
            new_total = len(data['work_experience']) # 4

            if new_total < total_saved:
                len_diff = abs(new_total - total_saved)
                delete_from_index = ((total_saved - 1) - len_diff) + 1

                # Delete extra entries
                for index in range(delete_from_index, len(saved_work_exp)):
                    saved_work_exp[index].delete()

                updated_entries = WorkExperience.objects.filter(
                    profile=profile
                )

                # Update remaining entries
                for index, saved_exp in enumerate(updated_entries, start=0):
                    serializer = work_experience_serializer(data=data['work_experience'][index])
                    serializer.is_valid(raise_exception=True)
                    
                    resp = update_experience(serializer.data, saved_exp)
                    if resp:
                        return resp
                return


            if new_total == total_saved:
                # Update existing entries
                for index, saved_exp in enumerate(saved_work_exp, start=0):
                    serializer = work_experience_serializer(data=data['work_experience'][index])
                    serializer.is_valid(raise_exception=True)  
                    resp = update_experience(serializer.data, saved_exp)
                    if resp:
                        return resp

                return


            if new_total > total_saved:
                print('New is bigger than old...')
                len_diff = abs(new_total - total_saved)     
                
                create_from_index = (total_saved - 1) + 1

                # Update existing entries
                for index, saved_exp in enumerate(saved_work_exp, start=0):
                    serializer = work_experience_serializer(data=data['work_experience'][index])
                    serializer.is_valid(raise_exception=True)

                    resp = update_experience(serializer.data, saved_exp)
                    if resp:
                        return resp

                # Create extra records
                for index in range(create_from_index, len(data['work_experience'])):
                    serializer = work_experience_serializer(data=data['work_experience'][index])
                    serializer.is_valid(raise_exception=True)
                    create_experience(serializer, profile)

                return
    return
