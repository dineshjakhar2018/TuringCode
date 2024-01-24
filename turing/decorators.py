# decorators.py
from django.shortcuts import redirect

def login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if 'email' not in request.session or not request.session['email']:
            return redirect('login')  # Replace 'login_view' with the actual URL name for the login view
        return view_func(request, *args, **kwargs)
    return wrapped_view

def anonymous_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if 'email' in request.session and request.session['email']:
            return redirect('home')  # Replace 'dashboard_view' with the actual URL name for the dashboard view
        return view_func(request, *args, **kwargs)
    return wrapped_view
