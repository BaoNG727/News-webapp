from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.utils import timezone
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto_core import TOTP, Base32

from .models import TwoFactorAuth, BackupCode, TwoFactorLog, EmailVerificationCode
from .email_utils import send_verification_email


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def setup_2fa(request):
    """
    Setup 2FA for the user.
    Display QR code and secret key for scanning with authenticator app.
    """
    # Get or create 2FA for user
    try:
        twofa = TwoFactorAuth.objects.get(user=request.user)
    except TwoFactorAuth.DoesNotExist:
        twofa = TwoFactorAuth.create_for_user(request.user)
    
    if request.method == 'POST':
        # User wants to regenerate secret
        if 'regenerate' in request.POST:
            twofa.regenerate_secret()
            messages.info(request, "Secret key regenerated. Please scan the new QR code.")
            return redirect('twofa_setup')
        
        # User is verifying the setup
        if 'verify' in request.POST:
            code = request.POST.get('code', '').strip()
            
            if not code:
                messages.error(request, "Please enter a verification code.")
                return redirect('twofa_setup')
            
            # Verify the code
            secret_bytes = twofa.get_secret_bytes()
            is_valid = TOTP.verify(secret_bytes, code, window=2)
            
            if is_valid:
                # Enable 2FA
                twofa.enable()
                
                # Generate backup codes
                backup_codes = BackupCode.generate_for_user(twofa)
                
                # Store backup codes in session to display once
                request.session['backup_codes'] = backup_codes
                
                # Mark as verified for this session (since we just verified during setup)
                request.session['2fa_verified'] = True
                request.session['2fa_verified_at'] = str(timezone.now())
                
                messages.success(request, "Two-Factor Authentication enabled successfully!")
                return redirect('twofa_backup_codes')
            else:
                messages.error(request, "Invalid verification code. Please try again.")
                TwoFactorLog.log_attempt(
                    user=request.user,
                    success=False,
                    method='totp',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
    
    # Generate provisioning URI for QR code
    secret_bytes = twofa.get_secret_bytes()
    account_name = request.user.email or request.user.username
    provisioning_uri = TOTP.get_provisioning_uri(
        secret_bytes,
        account_name,
        issuer="News Portal"
    )
    
    context = {
        'twofa': twofa,
        'provisioning_uri': provisioning_uri,
        'secret_key': twofa.secret_key,
    }
    
    return render(request, 'twofa/setup.html', context)


@login_required
def backup_codes(request):
    """
    Display backup codes (only shown once after setup).
    """
    backup_codes = request.session.get('backup_codes', [])
    
    if not backup_codes:
        messages.warning(request, "Backup codes have already been displayed.")
        return redirect('twofa_manage')
    
    # Clear backup codes from session after displaying
    if request.method == 'POST':
        del request.session['backup_codes']
        messages.success(request, "Make sure you've saved your backup codes in a safe place!")
        return redirect('twofa_manage')
    
    context = {
        'backup_codes': backup_codes,
    }
    
    return render(request, 'twofa/backup_codes.html', context)


@login_required
def manage_2fa(request):
    """
    Manage 2FA settings: view status, disable, regenerate backup codes.
    """
    try:
        twofa = TwoFactorAuth.objects.get(user=request.user)
    except TwoFactorAuth.DoesNotExist:
        return redirect('twofa_setup')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'disable':
            # Verify with password or 2FA code before disabling
            code = request.POST.get('code', '').strip()
            
            if code:
                secret_bytes = twofa.get_secret_bytes()
                is_valid = TOTP.verify(secret_bytes, code, window=2)
                
                if is_valid:
                    twofa.disable()
                    BackupCode.objects.filter(twofa=twofa).delete()
                    messages.success(request, "Two-Factor Authentication has been disabled.")
                    return redirect('twofa_manage')
                else:
                    messages.error(request, "Invalid verification code.")
            else:
                messages.error(request, "Please enter your 2FA code to disable.")
        
        elif action == 'regenerate_backup':
            # Regenerate backup codes
            backup_codes = BackupCode.generate_for_user(twofa, count=10)
            request.session['backup_codes'] = backup_codes
            messages.success(request, "New backup codes generated!")
            return redirect('twofa_backup_codes')
    
    # Get backup codes count
    backup_codes_count = BackupCode.objects.filter(twofa=twofa, is_used=False).count()
    
    # Get recent logs
    recent_logs = TwoFactorLog.objects.filter(user=request.user)[:10]
    
    context = {
        'twofa': twofa,
        'backup_codes_count': backup_codes_count,
        'recent_logs': recent_logs,
    }
    
    return render(request, 'twofa/manage.html', context)


@require_http_methods(["POST"])
def verify_2fa(request):
    """
    Verify 2FA code during login.
    This is called from login view.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Not authenticated'})
    
    code = request.POST.get('code', '').strip()
    
    if not code:
        return JsonResponse({'success': False, 'error': 'Code is required'})
    
    try:
        twofa = TwoFactorAuth.objects.get(user=request.user, is_enabled=True)
    except TwoFactorAuth.DoesNotExist:
        return JsonResponse({'success': False, 'error': '2FA not enabled'})
    
    # Check if it's a backup code
    if '-' in code:
        try:
            backup_code = BackupCode.objects.get(twofa=twofa, code=code, is_used=False)
            backup_code.use()
            twofa.mark_used()
            
            TwoFactorLog.log_attempt(
                user=request.user,
                success=True,
                method='backup',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Mark as verified in session
            request.session['2fa_verified'] = True
            request.session['2fa_verified_at'] = str(timezone.now())
            
            return JsonResponse({'success': True, 'method': 'backup'})
        except BackupCode.DoesNotExist:
            TwoFactorLog.log_attempt(
                user=request.user,
                success=False,
                method='backup',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            return JsonResponse({'success': False, 'error': 'Invalid backup code'})
    
    # Verify TOTP code
    secret_bytes = twofa.get_secret_bytes()
    is_valid = TOTP.verify(secret_bytes, code, window=2)
    
    if is_valid:
        twofa.mark_used()
        
        TwoFactorLog.log_attempt(
            user=request.user,
            success=True,
            method='totp',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Mark as verified in session
        request.session['2fa_verified'] = True
        request.session['2fa_verified_at'] = str(timezone.now())
        
        return JsonResponse({'success': True, 'method': 'totp'})
    else:
        TwoFactorLog.log_attempt(
            user=request.user,
            success=False,
            method='totp',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        return JsonResponse({'success': False, 'error': 'Invalid code'})


@login_required
def verify_2fa_page(request):
    """
    Display 2FA verification page.
    This is shown when user needs to verify 2FA after login.
    """
    try:
        twofa = TwoFactorAuth.objects.get(user=request.user, is_enabled=True)
    except TwoFactorAuth.DoesNotExist:
        messages.warning(request, "Two-Factor Authentication is not enabled.")
        return redirect('twofa_setup')
    
    # Handle send email request
    if request.method == 'POST' and 'send_email' in request.POST:
        if not request.user.email:
            messages.error(request, "No email address registered. Please use authenticator app.")
            return redirect('twofa_verify_page')
        
        # Generate and send code
        email_code = EmailVerificationCode.generate_for_user(
            request.user,
            ip_address=get_client_ip(request)
        )
        
        if send_verification_email(request.user, email_code.code, email_code.token, request):
            messages.success(request, f"Verification code sent to {request.user.email}")
        else:
            messages.error(request, "Failed to send email. Please try again or use authenticator app.")
        
        return redirect('twofa_verify_page')
    
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        
        if not code:
            messages.error(request, "Please enter a verification code.")
            return redirect('twofa_verify_page')
        
        # Check if it's an email code (6 digits only)
        if code.isdigit() and len(code) == 6:
            try:
                email_code = EmailVerificationCode.objects.get(
                    user=request.user,
                    code=code,
                    is_used=False
                )
                
                if email_code.is_valid():
                    email_code.use()
                    twofa.mark_used()
                    
                    TwoFactorLog.log_attempt(
                        user=request.user,
                        success=True,
                        method='email',
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                    
                    # Mark as verified
                    request.session['2fa_verified'] = True
                    request.session['2fa_verified_at'] = str(timezone.now())
                    
                    messages.success(request, "Email verification successful!")
                    
                    # Redirect to original page or dashboard
                    next_url = request.session.pop('2fa_next', 'panel')
                    return redirect(next_url)
                else:
                    messages.error(request, "Email code has expired. Request a new one.")
                    TwoFactorLog.log_attempt(
                        user=request.user,
                        success=False,
                        method='email',
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
            except EmailVerificationCode.DoesNotExist:
                # Not an email code, try TOTP
                pass
        
        # Check if it's a backup code (contains dash)
        if '-' in code:
            try:
                backup_code = BackupCode.objects.get(twofa=twofa, code=code, is_used=False)
                backup_code.use()
                twofa.mark_used()
                
                TwoFactorLog.log_attempt(
                    user=request.user,
                    success=True,
                    method='backup',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                # Mark as verified
                request.session['2fa_verified'] = True
                request.session['2fa_verified_at'] = str(timezone.now())
                
                messages.success(request, "Backup code verified successfully!")
                
                # Redirect to original page or dashboard
                next_url = request.session.pop('2fa_next', 'panel')
                return redirect(next_url)
                
            except BackupCode.DoesNotExist:
                messages.error(request, "Invalid or already used backup code.")
                TwoFactorLog.log_attempt(
                    user=request.user,
                    success=False,
                    method='backup',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
        else:
            # Verify TOTP code
            secret_bytes = twofa.get_secret_bytes()
            is_valid = TOTP.verify(secret_bytes, code, window=2)
            
            if is_valid:
                twofa.mark_used()
                
                TwoFactorLog.log_attempt(
                    user=request.user,
                    success=True,
                    method='totp',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                # Mark as verified
                request.session['2fa_verified'] = True
                request.session['2fa_verified_at'] = str(timezone.now())
                
                messages.success(request, "2FA verification successful!")
                
                # Redirect to original page or dashboard
                next_url = request.session.pop('2fa_next', 'panel')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid verification code. Please try again.")
                TwoFactorLog.log_attempt(
                    user=request.user,
                    success=False,
                    method='totp',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
    
    return render(request, 'twofa/verify.html')


@login_required
def email_verify(request, token):
    """
    Verify 2FA via magic link from email
    """
    try:
        email_code = EmailVerificationCode.objects.get(token=token, user=request.user)
        
        if not email_code.is_valid():
            messages.error(request, "This link has expired. Please request a new verification code.")
            return redirect('twofa_verify_page')
        
        # Mark as used
        email_code.use()
        
        # Get twofa
        try:
            twofa = TwoFactorAuth.objects.get(user=request.user, is_enabled=True)
            twofa.mark_used()
        except TwoFactorAuth.DoesNotExist:
            pass
        
        # Log
        TwoFactorLog.log_attempt(
            user=request.user,
            success=True,
            method='email',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Mark as verified
        request.session['2fa_verified'] = True
        request.session['2fa_verified_at'] = str(timezone.now())
        
        messages.success(request, "Email verification successful!")
        
        # Redirect to original page or dashboard
        next_url = request.session.pop('2fa_next', 'panel')
        return redirect(next_url)
        
    except EmailVerificationCode.DoesNotExist:
        messages.error(request, "Invalid verification link.")
        return redirect('twofa_verify_page')
