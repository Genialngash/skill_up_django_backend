from __future__ import absolute_import, unicode_literals

from celery.utils.log import get_task_logger
from core.settings import celery_app

from . import emails

logger = get_task_logger(__name__)


# Send User Unlock Code
@celery_app.task(name='send_user_activation_code')
def send_user_activation_code(
    user_email, context_data
):
    logger.info('Sent the unlock code to the the customer.')
    return emails.send_user_their_unlock_code(
       user_email, context_data
    )
