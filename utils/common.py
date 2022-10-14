import math


def get_date_suffix(date):
    if int(date.day) == 1 or \
        int(date.day) == 21 or \
        int(date.day) == 31:
        return 'st'

    if int(date.day) == 2 or int(date.day) == 22:
        return 'nd'
    if int(date.day) == 3 or int(date.day) == 23:
        return 'rd'
    if int(date.day) >= 4 and int(date.day) <= 30:
        return 'th'

def calculate_profile_completeness(user, profile):
    """
    Calculate profile completeness in percentage.
    This is based on the number of fields that are filled.
    """
    completeness = 0
    all_fields = [
        'first_name',
        'last_name',
        'phone_number',
        'contact_is_verified',
        'birthday',
        "bio",
        "country",
        "location",
        "profession",
        "education_level",
        "hourly_rate",
        "languages"
    ]

    total_fields = len(all_fields)
    portion = (1 / total_fields) * 100
    jobseeker_profile = profile


    if len(user.first_name) > 0:
        completeness += portion

    if len(user.last_name) > 0:
        completeness += portion

    if user.phone_number and len(user.phone_number) > 0:
        completeness += portion
    
    if user.contact_is_verified:
        completeness += portion

    if user.birthday and len(str(user.birthday)) > 0:
        completeness += portion

    if jobseeker_profile.bio and len(jobseeker_profile.bio) > 0:
        completeness += portion

    if jobseeker_profile.country and len(jobseeker_profile.country) > 0:
        completeness += portion

    if jobseeker_profile.location and len(jobseeker_profile.location) > 0:
        completeness += portion

    if jobseeker_profile.profession and len(jobseeker_profile.profession) > 0:
        completeness += portion

    if jobseeker_profile.education_level and len(jobseeker_profile.education_level) > 0:
        completeness += portion

    if jobseeker_profile.hourly_rate and jobseeker_profile.hourly_rate > 0:
        completeness += portion

    # Languages must be atleast one
    from jobseekers.models import JobseekerLanguage
    saved_langs = JobseekerLanguage.objects.filter(profile=jobseeker_profile)

    if len(saved_langs) > 0:
        completeness += portion

    ans = int(math.ceil(completeness))
    return ans
