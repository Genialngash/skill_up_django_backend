"""
Plucks the JWT access token from the query string and retrieves the associated user.
Once the WebSocket connection is opened, all messages can be sent and received without
verifying the user again. Closing the connection and opening it again 
requires re-authorization.
example url: 
ws://localhost:8000/<route>/?token=<token_of_the_user>
"""

import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

User = get_user_model()


@database_sync_to_async
def get_user(token_key):
    # If you are using jwt
    try:
        user_id: int = jwt.decode(token_key, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT['ALGORITHM']]).get(settings.SIMPLE_JWT['USER_ID_CLAIM'])
    except jwt.exceptions.DecodeError:
        return AnonymousUser()
    except jwt.exceptions.ExpiredSignatureError:
        return AnonymousUser()
    try:
        return AnonymousUser() if user_id is None else User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()



class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)
