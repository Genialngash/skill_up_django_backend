from __future__ import absolute_import, unicode_literals

from allauth.account.adapter import DefaultAccountAdapter
from celery import shared_task
from celery.utils.log import get_task_logger
from core.settings import celery_app

from . import emails

logger = get_task_logger(__name__)


# User SignUp Email
@celery_app.task(name='send_user_email_activation_after_signup')
def send_user_email_activation_after_signup(
    user_email, context_data
):
    logger.info('Sent the activation email to the new user.')
    return emails.send_user_activation_email(
       user_email, context_data
    )


# User Password Reset Email
@celery_app.task(name='send_user_password_reset_email')
def send_user_password_reset_email(
    user_email, context_data
):
    logger.info('Sent the password reset email to the user.')
    return emails.send_user_password_reset_email(
       user_email, context_data
    )

# Send User Sign Up Unlock Credits
@celery_app.task(name='send_user_signup_credits')
def send_user_signup_credits(user_email, context_data):
    logger.info('Sent the unlock code to the the employer.')
    return emails.send_employer_signup_credits(
       user_email, context_data
    )
