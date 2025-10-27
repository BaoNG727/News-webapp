"""
Decorators for Two-Factor Authentication
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import TwoFactorAuth


def require_2fa(view_func):
    """
    Decorator to require 2FA verification for a view.
    
    Usage:
        @login_required
        @require_2fa
        def my_secure_view(request):
            # This view requires 2FA
            pass
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('mylogin')
        
        # Check if user has 2FA enabled
        try:
            twofa = TwoFactorAuth.objects.get(user=request.user, is_enabled=True)
            
            # Check if verified in this session
            if not request.session.get('2fa_verified', False):
                request.session['2fa_next'] = request.get_full_path()
                messages.warning(request, "This page requires 2FA verification.")
                return redirect('twofa_verify_page')
        
        except TwoFactorAuth.DoesNotExist:
            # User doesn't have 2FA enabled
            messages.warning(request, "This page requires Two-Factor Authentication. Please enable it first.")
            return redirect('twofa_setup')
        
        # Proceed with the view
        return view_func(request, *args, **kwargs)
    
    return wrapper


def skip_2fa(view_func):
    """
    Decorator to explicitly skip 2FA verification for a view.
    Useful when using TwoFactorAuthMiddleware globally.
    
    Usage:
        @login_required
        @skip_2fa
        def public_profile(request):
            # This view doesn't require 2FA
            pass
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Mark this view as 2FA-exempt
        request._skip_2fa = True
        return view_func(request, *args, **kwargs)
    
    return wrapper
