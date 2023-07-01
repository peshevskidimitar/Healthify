from django.shortcuts import redirect


def unauthenticated(redirect_url):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)

            return view_func(request, *args, **kwargs)

        return wrapper_func

    return decorator


def allowed_users(roles=()):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.role not in roles:
                return redirect('accounts:unauthorized')

            return view_func(request, *args, **kwargs)

        return wrapper_func

    return decorator
