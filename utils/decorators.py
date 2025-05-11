from django.shortcuts import render
from functools import wraps

def require_auth(template='main/auth_required.html'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return render(request, template, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
