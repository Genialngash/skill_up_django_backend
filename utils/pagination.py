from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class VeetaBasePaginationSet(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 25

    def get_paginated_response(self, data):
        # print(self.page.__dict__)
        # print(dir(self.page))

        # ('previous_page', self.page.previous_page_number()),
        # ('next_page', self.page.next_page_number()),

        # Links
        # ('next', self.get_next_link()),
        # ('previous', self.get_previous_link())

        next_page = None
        previous_page = None

        if self.page.has_previous():
            previous_page = self.page.previous_page_number()

        if self.page.has_next():
            next_page = self.page.next_page_number()


        return Response({
            'data': OrderedDict([
                ('current_page', self.page.number),
                ('previous_page', previous_page),
                ('next_page', next_page),
                ('count', self.page.paginator.count),
                ('results', data)
            ]),
            'message': 'Success.',
            'status': 'ok.',
            'status_code': 200,
        })
