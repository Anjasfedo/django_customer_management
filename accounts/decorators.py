from django.http import HttpResponse
from django.shortcuts import redirect


def already_login(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return function(request, *args, **kwargs)

    return wrap


def allow_users(allow_roles=[]):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allow_roles:
                return function(request, *args, **kwargs)

            if group == 'admin':
                return redirect('dashboard')

            if group == 'customer':
                return redirect('user_page')

            return HttpResponse("You don't have permission to view this page.")

        return wrap

    return decorator


def admin_only(function):
    def wrap(request, *args, **kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user_page')

        if group == 'admin':
            return function(request, *args, **kwargs)

        return HttpResponse("You don't have permission to view this page.")

    return wrap
