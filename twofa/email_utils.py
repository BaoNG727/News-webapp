"""
Email utilities for 2FA verification
"""
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


def send_verification_email(user, code, token, request):
    """
    Send verification code via email with magic link
    """
    # Build magic link
    magic_link = request.build_absolute_uri(
        reverse('twofa_email_verify', kwargs={'token': token})
    )
    
    subject = f"Your 2FA Verification Code - {getattr(settings, 'SITE_NAME', 'News Portal')}"
    
    message = f"""
Hello {user.username},

You are attempting to log in to your account. Please use one of the following methods to verify:

METHOD 1: Enter this 6-digit code
{code}

METHOD 2: Click this link to login instantly
{magic_link}

This code will expire in 10 minutes.

If you did not attempt to login, please ignore this email or contact support.

---
{getattr(settings, 'SITE_NAME', 'News Portal')}
    """.strip()
    
    html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #007bff; color: white; padding: 20px; text-align: center; }}
        .content {{ background: #f9f9f9; padding: 30px; border: 1px solid #ddd; }}
        .code-box {{ background: #fff; border: 2px dashed #007bff; padding: 20px; margin: 20px 0; text-align: center; }}
        .code {{ font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #007bff; }}
        .button {{ display: inline-block; background: #28a745; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
        .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Two-Factor Authentication</h1>
        </div>
        <div class="content">
            <p>Hello <strong>{user.username}</strong>,</p>
            
            <p>You are attempting to log in to your account. Please use one of the following methods to verify:</p>
            
            <h3>Method 1: Enter this code</h3>
            <div class="code-box">
                <div class="code">{code}</div>
            </div>
            
            <h3>Method 2: Click to login instantly</h3>
            <p style="text-align: center;">
                <a href="{magic_link}" class="button">Login Now</a>
            </p>
            
            <div class="warning">
                <strong>⏱️ This code expires in 10 minutes</strong>
            </div>
            
            <p style="font-size: 12px; color: #666;">
                If you did not attempt to login, please ignore this email or contact support immediately.
            </p>
        </div>
        <div class="footer">
            <p>&copy; {getattr(settings, 'SITE_NAME', 'News Portal')} - Secure Login</p>
        </div>
    </div>
</body>
</html>
    """.strip()
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
