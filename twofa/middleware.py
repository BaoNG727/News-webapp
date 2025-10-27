"""
Two-Factor Authentication Middleware

This middleware enforces 2FA verification for users who have it enabled.
"""

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from .models import TwoFactorAuth


class TwoFactorAuthMiddleware:
    """
    Middleware to enforce 2FA verification.
    
    If a user has 2FA enabled and hasn't verified in this session,
    redirect them to verification page.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that don't require 2FA verification
        self.exempt_urls = [
            '/2fa/',  # All 2FA URLs are exempt
            '/logout/',
            '/static/',
            '/media/',
        ]
    
    def __call__(self, request):
        # Skip if user is not authenticated
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Skip if accessing exempt URLs
        if any(request.path.startswith(url) for url in self.exempt_urls):
            return self.get_response(request)
        
        # Check if user has 2FA enabled
        try:
            twofa = TwoFactorAuth.objects.get(user=request.user, is_enabled=True)
            
            # Check if already verified in this session
            if not request.session.get('2fa_verified', False):
                # Store the original URL to redirect back after verification
                request.session['2fa_next'] = request.get_full_path()
                
                messages.warning(request, "Please enter your 2FA code to continue.")
                return redirect('twofa_verify_page')
        
        except TwoFactorAuth.DoesNotExist:
            # User doesn't have 2FA enabled, proceed normally
            pass
        
        response = self.get_response(request)
        return response
