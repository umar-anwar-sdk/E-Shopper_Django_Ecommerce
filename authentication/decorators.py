from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse_lazy


def _role_required(role_name, redirect_url='home_page'):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse_lazy('login'))

            user_role_check = getattr(request.user, f'is_{role_name}', None)
            if not callable(user_role_check) or not user_role_check():
                return redirect(reverse_lazy(redirect_url))

            return view_func(request, *args, **kwargs)

        return wrapped
    return decorator


admin_required = _role_required('admin')
vendor_required = _role_required('vendor')
customer_required = _role_required('customer')
