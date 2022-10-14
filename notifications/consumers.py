"""
import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from .models import Notification, NotificationSerializer
from .pagination import NotificationsPaginationSet

q = "BHxPQ8fZdn6J"
b= "35.178.142.215"
c = "019005589558"



# id_from = id_from + page_size
# https://meet.google.com/gsz-jpej-bwo

def get_all_user_notifications(user_id):
    return Notification.objects.filter(user=user_id)


class NotificationConsumer(WebsocketConsumer):
    def fetch_notifications(self, data):
        notifications = get_all_user_notifications(data['user_id'])
        serializer = NotificationSerializer(notifications, many=True)
        content = {
            'command': 'notifications',
            'notifications': self.notifications_to_json(serializer.data)
        }

        for ntf in notifications:
            ntf.sent = True
            ntf.save()

        self.send_notification(content)


    def notifications_to_json(self, notifications):
        result = []
        for ntf in notifications:
            result.append(self.notification_to_json(ntf))
        return result


    def notification_to_json(self, ntf):
        return {
            'id': ntf['id'],
            'message': ntf['message'],
            'created_on': ntf['created_on'],
            'time_since': ntf['time_since']
        }

    commands = { 'fetch_notifications': fetch_notifications }


    def connect(self):
        user = self.scope['user']
        if user.is_anonymous:
            self.close()

        # Set the room name to the user ID to make it unique to every user
        self.room_name = user.id
        self.room_group_name = f'{self.room_name}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    def send_notification(self, content):
        if 'command' in content and \
            content['command'] == 'new_notification':
            ntf = Notification.objects.get(id=content['notification']['id'])
            ntf.sent = True
            ntf.save()

        self.send(text_data=json.dumps(content))

    
    def receive(self, text_data):
        user = self.scope['user']
        data = json.loads(text_data)
        data['user_id'] = user.id
        self.commands[data['command']](self, data)
"""
