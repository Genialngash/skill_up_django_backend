from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class NotificationsPaginationSet(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 16

    def get_paginated_response(self, data):
        return Response({
            'data': OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('results', data)
            ]),
        })
