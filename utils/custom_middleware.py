import json

from django.utils.deprecation import MiddlewareMixin


class YankTokenRefreshFromHeaderIntoTheBody(MiddlewareMixin):
    """
    For dj-rest-auth refresh token endpoint.
    Check for a 'token' in the request.COOKIES and if found,
    add it to the body payload.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path == '/accounts/auth/logout/' and 'refresh' in request.COOKIES:
            data = json.loads(request.body)
            data['refresh'] = request.COOKIES['refresh']
            request._body = json.dumps(data).encode('utf-8')
        else:
            # the client has to pass an empty object as the body '{}'
            pass
        return None
