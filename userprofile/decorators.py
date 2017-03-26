from django.core.exceptions import PermissionDenied
from .factory import UserFactory


def user_is_employee(function):
    def wrap(request, *args, **kwargs):
        user = UserFactory.get_user(request)

        if UserFactory.isNurse(user) or UserFactory.isDoctor(user):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap