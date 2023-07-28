from django.shortcuts import redirect
from functools import wraps


def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' in request.session:
            # User is authenticated, allow access to the view
            return view_func(request, *args, **kwargs)
        else:
            # User is not authenticated, redirect to the login page
            return redirect('login')  # Replace 'login' with the URL name of your login page

    return _wrapped_view
