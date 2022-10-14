from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsAuthenticatedAndIsEmployer(BasePermission):
    """
    Allows access only to authenticated users and type is Employer.
    """

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            request.user.logged_in_as == 'Employer'
        )

class IsAuthenticatedAndIsJobseeker(BasePermission):
    """
    Allows access only to authenticated users and type is Jobseeker.
    """

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            request.user.logged_in_as == 'Jobseeker'
        )
