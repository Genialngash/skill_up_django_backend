from establishments.exceptions.company import handler as company_handler
from jobs.exceptions.application import handler as job_application_handler
from jobs.exceptions.bookmark import handler as bookmark_handler
from jobs.exceptions.job_card import handler as job_card_handler
from jobseekers.exceptions.job_offers import handler as jobseeker_offers_handler
from jobseekers.exceptions.prof_info import handler as prof_info_handler
from jobseekers.exceptions.solo_work_experience import (
    handler as solo_work_experience_handler,
)
from notifications.exceptions.email_notifications_subscription import (
    handler as email_notifications_subscription_handler,
)
from notifications.exceptions.notification import handler as notification_handler
from profile_unlock.exceptions.unlock_profile import handler as unlock_profile_handler
from ratings.exceptions.rating import handler as rating_exception_handler
from rest_framework.views import exception_handler
from users.exceptions.change_password import handler as change_password_handler
from users.exceptions.contact_verification import (
    handler as contact_verification_handler,
)
from users.exceptions.contact_verification_confirm import (
    handler as contact_verification_confirm_handler,
)
from users.exceptions.email_verification import handler as email_verification_handler
from users.exceptions.jobseeker_profile import handler as jobseeker_profile_handler
from users.exceptions.login import handler as login_handler
from users.exceptions.login_in_as import handler as switch_handler
from users.exceptions.me import handler as user_details_handler
from users.exceptions.password_reset import handler as password_reset_handler
from users.exceptions.password_reset_confirm import (
    handler as password_reset_confirm_handler,
)
from users.exceptions.register import handler as user_register_handler
from users.exceptions.resend_verification_email import (
    handler as resend_verification_email_handler,
)

from utils.exceptions.detail import handler as detail_handler

from .exceptions import jwt_exception_helper


def handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        # Handle General Errors
        if 'detail' in response.data:
            res = detail_handler(response)
            return res

        # User Registration
        if context['request'].path == '/accounts/registration/':
            res = user_register_handler(response)
            return res

        if context['request'].path == '/accounts/auth/confirm-email/':
            res = email_verification_handler(response)
            return res

        # Resend email verification errors
        if context['request'].path == '/accounts/auth/resend-confirmation-email/':
            res = resend_verification_email_handler(response)
            return res

        if context['request'].path == '/accounts/auth/login/':
            res = login_handler(response)
            return res

        # Password change
        if context['request'].path == '/accounts/auth/password/change/':
            res = change_password_handler(response)
            return res

        # Password reset
        if context['request'].path == '/accounts/auth/password/reset/':
            res = password_reset_handler(response)
            return res

        # Password reset confirm
        if context['request'].path == '/accounts/auth/password/reset/confirm/':
            res = password_reset_confirm_handler(response)
            return res

        # Bookmarks
        if '/jobs/bookmark/create/' in context['request'].path:
            res =  bookmark_handler(response)
            return res

        # Verify contact
        if context['request'].path == '/contact/verify':
            res = contact_verification_handler(response)
            return res

        if context['request'].path == '/contact/verify/confirm':
            res = contact_verification_confirm_handler(response)
            return res

        # User details
        if '/accounts/auth/user/me/' in context['request'].path:
            res = user_details_handler(response)
            return res

        # Jobseeker Ratings
        if context['request'].path == '/ratings/jobseeker/create/':
            res = rating_exception_handler(response)
            return res

        # handle prof info create errors
        if '/jobseekers/professional-info/' in context['request'].path:
            return prof_info_handler(response)

        # handle switch exceptions
        if '/accounts/auth/login-state/switch/' in context['request'].path:
            return switch_handler(response)

        # handle job card 
        if '/jobs/card/' in context['request'].path:
            return job_card_handler(response)

        # handle company create errors
        if '/company/' in context['request'].path:
            return company_handler(response)

        # handle profile updates
        if '/accounts/jobseeker/profile/' in context['request'].path:
            return jobseeker_profile_handler(response)
        
        # unlock profile
        if '/profile/unlock/' in context['request'].path:
            return unlock_profile_handler(response)

        if '/notification/update/' in context['request'].path:
            return notification_handler(response)

        if '/notifications/mark-all/' in context['request'].path:
            return notification_handler(response)

        if '/notifications/email/subscription/' in context['request'].path:
            return email_notifications_subscription_handler(response)

        if '/work-experience/create/' in context['request'].path:
            return solo_work_experience_handler(response)

        if '/work-experience/update/' in context['request'].path:
            return solo_work_experience_handler(response)

        if '/jobseeker/offer/accept/' in context['request'].path:
            return jobseeker_offers_handler(response)


        # TODO
        # handle jwt token errors
        if '/accounts/token' in context['request'].path:
            res = jwt_exception_helper \
                .handle_jwt_errors(response)
            return res

        # Job Applications
        if '/job-applications/' in context['request'].path:
            res = job_application_handler(response)
            return res


    return response
