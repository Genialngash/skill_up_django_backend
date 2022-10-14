from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from faker import Faker
from rest_framework import generics, status, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.pagination import VeetaBasePaginationSet

from .models import EmailNotificationSubscription, Notification
from .serializers import (
    EmailNotificationSubscriptionSerializer,
    MarkAllNotificationAsReadSerializer,
    MarkNotificationAsReadSerializer,
    NotificationSerializer,
)
from .view_fixes import *

fake = Faker()
User = get_user_model()


# def test(request):
#     channel_layer = get_channel_layer()
#     user = User.objects.get(email=USER_ONE)
#     ntf = Notification.objects.create(
#         message = fake.paragraph(nb_sentences=1),
#         user = user
#     )

#     ser = NotificationSerializer(ntf)

#     async_to_sync(channel_layer.group_send)(
#         f'{user.id}', 
#         {
#             "type": 'send_notification',
#             "command": 'new_notification',
#             "notification": ser.data,
#         }
#     )

#     return JsonResponse({'status': 'ok'})

class NotificationViewSet(viewsets.ViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'head', 'options']
    pagination_class = VeetaBasePaginationSet


    def get_queryset(self):
        user = self.request.user
        qs = Notification.objects.filter(user=user)
        return qs

    def get_object(self):
        ntf_id = self.kwargs.get('pk')
        obj = Notification.objects.get(id=ntf_id)
        return obj

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator


    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NotificationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NotificationSerializer(queryset, many=True)
        
        return Response({
            'data': serializer.data,
            'status_code': 200,
            'status': 'ok',
            'message': 'Success.'
        })

        
@extend_schema(parameters=[OpenApiParameter("id", int, OpenApiParameter.PATH)])
class NotificationUpdateViewSet(viewsets.ViewSet):
    serializer_class = MarkNotificationAsReadSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', 'head', 'options']
    lookup_url_kwarg = 'pk'
    lookup_field = 'id'
    
    def get_object(self):
        ntf_id = self.kwargs.get('pk')
        obj = Notification.objects.get(id=ntf_id)
        return obj


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MarkNotificationAsReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.mark_as_read = serializer.validated_data['mark_as_read']
        instance.save()

        if serializer.validated_data['mark_as_read']:
            user = request.user
            user.unread_notifications = user.unread_notifications - 1
            user.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({
            'message': 'Successfully updated the notification read status.',
            'status_code': 200,
            'status': 'ok'
        }, status=status.HTTP_200_OK)


class MarkAllNotificationsAsReadView(views.APIView):
    serializer_class = MarkAllNotificationAsReadSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ('PATCH', 'OPTIONS', 'HEAD')

    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user)
        return qs
    

    def patch(self, request, format=None):
        serializer = MarkAllNotificationAsReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notifications = self.get_queryset()

        for ntf in notifications:
            ntf.mark_as_read = serializer.validated_data['mark_all_as_read']
            ntf.save()

        if serializer.validated_data['mark_all_as_read']:
            user = request.user
            user.unread_notifications = 0
            user.save()

        return Response({
            'message': 'Successfully updated notifications read status.',
            'status_code': 200,
            'status': 'ok'
        }, status=status.HTTP_200_OK)



class EmailNotificationSubscriptionView(generics.RetrieveUpdateAPIView):
    serializer_class = EmailNotificationSubscriptionSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ('PATCH', 'OPTIONS', 'HEAD')


    def get_object(self):
        qs = EmailNotificationSubscription.objects.get(user=self.request.user)
        return qs


    def perform_update(self, serializer):
        serializer.save()


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}


        return Response({
            'message': 'Email notifications updated.',
            'status_code': 200,
            'status': 'ok'
        }, status=status.HTTP_200_OK)
