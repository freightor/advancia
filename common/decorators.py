from django.core.exceptions import PermissionDenied
# create a check to verify that user has admin privileges


def admin_staff_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.administrator.role == "admin":
            return function(request, *args, **kwargs)
        raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def admin_storeuser_required(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user,"storeuser"):
            if request.user.storeuser.role == "admin":
                return function(request, *args, **kwargs)
        raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def employee_required(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, "administrator"):
            return function(request, *args, **kwargs)
        raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
