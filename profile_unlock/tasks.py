from __future__ import absolute_import, unicode_literals

from celery.utils.log import get_task_logger
from core.settings import celery_app

from . import emails

logger = get_task_logger(__name__)

@celery_app.task(name='send_developer_cron_update')
def send_developer_cron_update(context_data):
    logger.info('Sent the cron update to the developer.')
    return emails.send_developer_cron_update(context_data)
