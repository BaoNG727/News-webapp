# 🔐 Two-Factor Authentication - Setup Guide

## ⚡ Quick Setup (3 Steps)

### Step 1: Add to Django Settings

Edit `newsportal/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... other apps ...
    
    'twofa',  # ← ADD THIS LINE
]

# Optional: Enable 2FA middleware (enforces 2FA for all users)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... other middleware ...
    
    'twofa.middleware.TwoFactorAuthMiddleware',  # ← ADD THIS LINE (at the end)
]
```

### Step 2: Update URLs

Edit `newsportal/urls.py`:

```python
from django.urls import include, re_path
from django.contrib import admin

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    # ... existing urls ...
    
    re_path(r'^2fa/', include('twofa.urls')),  # ← ADD THIS LINE
]
```

### Step 3: Run Migrations

```bash
# Create migrations
python manage.py makemigrations twofa

# Apply migrations
python manage.py migrate twofa

# Or use the batch script
migrate.bat
```

---

## ✅ Verification

### Test crypto_core Module

```bash
python crypto_core.py
```

You should see:
```
[TEST 1] Base32 Encoding/Decoding - [PASS]
[TEST 2] HOTP (RFC 4226 Test Vectors) - [OK] x5
[TEST 3] TOTP - [PASS]
[TEST 4] Provisioning URI - Generated
[TEST 5] Backup Codes - Generated
```

### Test in Browser

1. Start server: `run.bat` or `python manage.py runserver`
2. Login to your account
3. Visit: http://127.0.0.1:8000/2fa/setup/
4. You should see the QR code setup page

---

## 📱 User Guide

### How to Enable 2FA

1. **Login** to your account
2. Go to **2FA Setup**: http://127.0.0.1:8000/2fa/setup/
3. **Install authenticator app** on your phone:
   - 📱 Google Authenticator (iOS/Android)
   - 🔐 Authy (iOS/Android)  
   - 🔑 Microsoft Authenticator (iOS/Android)
4. **Scan the QR code** with your app
5. **Enter the 6-digit code** to verify
6. **Save backup codes** shown on next page

### How to Login with 2FA

1. Enter **username** and **password** as normal
2. If 2FA is enabled, you'll see **verification page**
3. Open your **authenticator app**
4. Enter the **6-digit code**
5. Click **Verify**

### Lost Your Phone?

Use a backup code instead:
- Format: `XXXX-XXXX` (e.g., `8829-BCBD`)
- Each code can only be used **once**
- You have **10 backup codes**

---

## 🛡️ Features

### ✅ What's Included

- [x] **QR Code Setup** - Easy scanning with authenticator apps
- [x] **TOTP Codes** - 6-digit codes that change every 30 seconds
- [x] **Backup Codes** - 10 recovery codes for emergencies
- [x] **Activity Logs** - Track all 2FA verification attempts
- [x] **Admin Dashboard** - View all users' 2FA status
- [x] **Enable/Disable** - Users can toggle 2FA on/off
- [x] **Regenerate Codes** - Generate new backup codes anytime
- [x] **Time Window** - ±60 seconds tolerance for clock differences

### 🔒 Security Features

- **RFC Compliant** - Follows RFC 4226 (HOTP) and RFC 6238 (TOTP)
- **Custom Implementation** - Built from scratch, no external 2FA libraries
- **Secure Storage** - Secrets stored encrypted in database
- **IP Logging** - Track verification attempts by IP address
- **Failed Attempt Tracking** - Monitor suspicious activity
- **One-Time Codes** - Backup codes can only be used once

---

## 🎯 Advanced Usage

### Require 2FA for Specific Views

Use the `@require_2fa` decorator:

```python
from django.contrib.auth.decorators import login_required
from twofa.decorators import require_2fa

@login_required
@require_2fa
def sensitive_data(request):
    """This view requires 2FA verification"""
    return render(request, 'sensitive.html')
```

### Skip 2FA for Public Pages

Use the `@skip_2fa` decorator:

```python
from twofa.decorators import skip_2fa

@login_required
@skip_2fa
def public_profile(request):
    """This view doesn't require 2FA"""
    return render(request, 'profile.html')
```

### Check 2FA Status in Code

```python
from twofa.models import TwoFactorAuth

# Check if user has 2FA enabled
try:
    twofa = TwoFactorAuth.objects.get(user=request.user, is_enabled=True)
    has_2fa = True
except TwoFactorAuth.DoesNotExist:
    has_2fa = False
```

### In Templates

```django
{% if request.user.twofa.is_enabled %}
    <span class="badge badge-success">
        <i class="fa fa-shield"></i> 2FA Enabled
    </span>
{% else %}
    <a href="{% url 'twofa_setup' %}" class="btn btn-warning">
        <i class="fa fa-shield"></i> Enable 2FA
    </a>
{% endif %}
```

---

## 🎨 Customize Templates

Templates are in `twofa/templates/twofa/`:

- `setup.html` - 2FA setup page with QR code
- `backup_codes.html` - Backup codes display
- `manage.html` - Manage 2FA settings
- `verify.html` - 2FA verification page

You can override these templates by creating your own in your app's templates folder.

---

## 🔧 Configuration

### Time Window Settings

Edit `crypto_core.py`:

```python
class TOTP:
    DEFAULT_PERIOD = 30  # Change time step (default: 30 seconds)
```

### Backup Codes Count

Edit `twofa/views.py`:

```python
# Generate 10 codes (change number as needed)
backup_codes = BackupCode.generate_for_user(twofa, count=10)
```

### Code Verification Window

In views.py, adjust the `window` parameter:

```python
# Allow ±2 time steps (total 5 minutes tolerance)
is_valid = TOTP.verify(secret_bytes, code, window=2)
```

---

## 📊 Admin Panel

### View All Users' 2FA Status

1. Go to: http://127.0.0.1:8000/admin/twofa/twofactorauth/
2. See:
   - Who has 2FA enabled
   - When they set it up
   - Last usage time

### View Security Logs

1. Go to: http://127.0.0.1:8000/admin/twofa/twofactorlog/
2. Monitor:
   - Failed login attempts
   - Successful verifications
   - IP addresses
   - Timestamps

### Emergency Disable 2FA

```python
# In Django shell
python manage.py shell

>>> from django.contrib.auth.models import User
>>> from twofa.models import TwoFactorAuth
>>> 
>>> user = User.objects.get(username='username')
>>> twofa = TwoFactorAuth.objects.get(user=user)
>>> twofa.disable()
```

---

## 🐛 Troubleshooting

### QR Code Not Showing

**Problem**: QR code doesn't appear on setup page

**Solutions**:
1. Check browser console for JavaScript errors
2. Ensure QRCode.js library is loaded:
   ```html
   <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
   ```
3. Clear browser cache

### Codes Not Working

**Problem**: 6-digit codes are always "Invalid"

**Solutions**:
1. **Check server time**: `date` - Must be accurate
2. **Sync authenticator app**: Settings → Time correction
3. **Try next code**: Wait 30 seconds for new code
4. **Use backup code**: If all else fails

### Time Sync Issues

**Problem**: Codes work sporadically

**Solution**:
```bash
# Windows: Sync time
w32tm /resync

# Linux: Install and use NTP
sudo apt-get install ntp
sudo service ntp restart
```

### Database Errors

**Problem**: Table doesn't exist

**Solution**:
```bash
python manage.py makemigrations twofa
python manage.py migrate twofa
```

---

## 📚 File Structure

```
twofa/
├── models.py                   # Database models
│   ├── TwoFactorAuth          # User 2FA configuration
│   ├── BackupCode             # Recovery codes
│   └── TwoFactorLog           # Audit logs
│
├── views.py                    # View logic
│   ├── setup_2fa()            # QR code setup
│   ├── backup_codes()         # Show backup codes
│   ├── manage_2fa()           # Manage settings
│   ├── verify_2fa()           # API verification
│   └── verify_2fa_page()      # Verification page
│
├── admin.py                    # Django admin
├── middleware.py               # 2FA enforcement
├── decorators.py              # @require_2fa, @skip_2fa
├── urls.py                    # URL routing
│
└── templates/twofa/
    ├── setup.html             # Setup page
    ├── backup_codes.html      # Backup codes
    ├── manage.html            # Settings
    └── verify.html            # Verification
```

---

## 🚀 Next Steps

After setup is complete:

1. ✅ Test with your account
2. ✅ Enable 2FA for admin users
3. ✅ Document procedure for your team
4. ✅ Setup email notifications (optional)
5. ✅ Configure rate limiting (recommended)
6. ✅ Review security logs regularly

---

## 📞 Support

Need help?

1. Check [TWO_FACTOR_AUTH_README.md](TWO_FACTOR_AUTH_README.md) for detailed documentation
2. Review logs: `python manage.py shell` → `TwoFactorLog.objects.all()`
3. Test crypto_core: `python crypto_core.py`
4. Check Django logs for errors

---

**Security First! 🔐**
