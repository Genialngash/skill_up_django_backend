from __future__ import absolute_import, unicode_literals

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from faker import Faker

fake = Faker()

from celery.utils.log import get_task_logger
from core.settings import celery_app

logger = get_task_logger(__name__)


@celery_app.task(name='broadcast_notification_to_user')
def broadcast_notification_to_user(data):
	try:
		logger.info('Sent the notification to the user.')
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
		f"{data['user']}", 
			{
				"type": 'send_notification',
				"command": 'new_notification',
				"notification": data,
			}
		)					
	except:
		pass
