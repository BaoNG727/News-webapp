# 🔐 Two-Factor Authentication (2FA) System

## Overview

This is a **custom-built Two-Factor Authentication system** implemented from scratch without using external libraries like `pyotp`. The system follows industry standards (RFC 4226 and RFC 6238) and provides enterprise-grade security.

---

## ✨ Features

### Core Features
- ✅ **TOTP (Time-based OTP)** - Compatible with Google Authenticator, Authy, Microsoft Authenticator
- ✅ **QR Code Setup** - Easy onboarding with QR code scanning
- ✅ **Backup Codes** - 10 one-time recovery codes
- ✅ **Activity Logging** - Complete audit trail of 2FA attempts
- ✅ **User Management** - Enable/Disable 2FA per user
- ✅ **Security Features** - IP logging, failed attempt tracking

### Implementation Details
- 🔒 **Base32 Encoding/Decoding** (RFC 4648)
- 🔒 **HOTP Algorithm** (RFC 4226) with Dynamic Truncation
- 🔒 **TOTP Algorithm** (RFC 6238) with time-step calculation
- 🔒 **HMAC-SHA1** for cryptographic security
- 🔒 **Cryptographically Secure Random** for secret generation

---

## 📁 Project Structure

```
News-webapp/
├── crypto_core.py              # Core 2FA implementation (RFC 4226, RFC 6238)
│
├── twofa/                      # Django app for 2FA
│   ├── models.py              # TwoFactorAuth, BackupCode, TwoFactorLog
│   ├── views.py               # Setup, verify, manage views
│   ├── admin.py               # Admin interface
│   ├── middleware.py          # 2FA enforcement middleware
│   ├── decorators.py          # @require_2fa, @skip_2fa
│   ├── urls.py                # URL routing
│   │
│   └── templates/twofa/
│       ├── setup.html         # QR code setup page
│       ├── backup_codes.html  # Backup codes display
│       ├── manage.html        # Manage 2FA settings
│       └── verify.html        # 2FA verification page
│
└── TWO_FACTOR_AUTH_README.md  # This file
```

---

## 🚀 Installation

### Step 1: Add to Django Settings

Edit `newsportal/settings.py`:

```python
INSTALLED_APPS = [
    # ... existing apps ...
    'twofa',  # Add this
]

# Optional: Add middleware to enforce 2FA globally
MIDDLEWARE = [
    # ... existing middleware ...
    'twofa.middleware.TwoFactorAuthMiddleware',  # Add this at the end
]
```

### Step 2: Update URLs

Edit `newsportal/urls.py`:

```python
from django.urls import include, re_path

urlpatterns = [
    # ... existing patterns ...
    re_path(r'^2fa/', include('twofa.urls')),  # Add this
]
```

### Step 3: Run Migrations

```bash
python manage.py makemigrations twofa
python manage.py migrate twofa
```

---

## 📖 Usage Guide

### For Users

#### 1. Enable 2FA

1. Login to your account
2. Go to: http://127.0.0.1:8000/2fa/setup/
3. Scan the QR code with your authenticator app
4. Enter the 6-digit code to verify
5. Save your backup codes in a safe place

#### 2. Login with 2FA

1. Enter username and password as normal
2. If 2FA is enabled, you'll be asked for a code
3. Enter the 6-digit code from your app
4. Or use a backup code (format: XXXX-XXXX)

#### 3. Manage 2FA

- **View Status**: http://127.0.0.1:8000/2fa/manage/
- **Regenerate Backup Codes**: Click "Regenerate" button
- **Disable 2FA**: Enter 2FA code to confirm

### For Administrators

#### 1. View User 2FA Status

- Go to: http://127.0.0.1:8000/admin/twofa/twofactorauth/
- See all users with 2FA enabled/disabled
- View last usage time

#### 2. View Security Logs

- Go to: http://127.0.0.1:8000/admin/twofa/twofactorlog/
- Monitor failed/successful 2FA attempts
- Track IP addresses and timestamps

#### 3. Manually Disable 2FA (Emergency)

```python
from django.contrib.auth.models import User
from twofa.models import TwoFactorAuth

user = User.objects.get(username='username')
twofa = TwoFactorAuth.objects.get(user=user)
twofa.disable()
```

---

## 🔧 API Reference

### crypto_core.py

#### Base32 Class

```python
from crypto_core import Base32

# Encode bytes to Base32
encoded = Base32.encode(b"Hello World")  # Returns: "JBSWY3DPEBLW64TMMQQQ===="

# Decode Base32 to bytes
decoded = Base32.decode("JBSWY3DPEBLW64TMMQQQ====")  # Returns: b"Hello World"
```

#### HOTP Class

```python
from crypto_core import HOTP

secret = b"12345678901234567890"
counter = 0

# Generate HOTP code
code = HOTP.generate(secret, counter)  # Returns: "755224"

# Verify HOTP code
is_valid = HOTP.verify(secret, "755224", counter, window=1)  # Returns: True
```

#### TOTP Class

```python
from crypto_core import TOTP

secret = b"12345678901234567890"

# Generate TOTP code (current time)
code = TOTP.generate(secret)  # Returns: "287082" (varies with time)

# Verify TOTP code
is_valid = TOTP.verify(secret, code, window=1)  # Returns: True

# Get provisioning URI for QR code
uri = TOTP.get_provisioning_uri(secret, "user@example.com", "News Portal")
# Returns: "otpauth://totp/News%20Portal:user@example.com?secret=..."
```

#### TwoFactorUtils Class

```python
from crypto_core import TwoFactorUtils

# Generate random secret (20 bytes)
secret = TwoFactorUtils.generate_secret()

# Generate secret as Base32 string
secret_b32 = TwoFactorUtils.generate_secret_base32()

# Generate backup codes
codes = TwoFactorUtils.generate_backup_codes(count=10)
# Returns: ['8829-BCBD', '4EBC-17F9', ...]
```

---

## 🎨 Frontend Integration

### Protect Views with 2FA

```python
from django.contrib.auth.decorators import login_required
from twofa.decorators import require_2fa

@login_required
@require_2fa
def sensitive_data(request):
    # This view requires 2FA verification
    return render(request, 'sensitive.html')
```

### Skip 2FA for Specific Views

```python
from twofa.decorators import skip_2fa

@login_required
@skip_2fa
def public_profile(request):
    # This view doesn't require 2FA
    return render(request, 'profile.html')
```

### Check 2FA Status in Templates

```django
{% if request.user.twofa.is_enabled %}
    <span class="badge badge-success">2FA Enabled</span>
{% else %}
    <a href="{% url 'twofa_setup' %}">Enable 2FA</a>
{% endif %}
```

---

## 🔒 Security Considerations

### Best Practices

1. **Secret Storage**
   - Secrets are stored encrypted in database
   - Never log or display full secret keys
   - Use environment variables for sensitive data

2. **Time Synchronization**
   - Server time must be accurate
   - TOTP uses 30-second time windows
   - Allow ±1 window for clock skew

3. **Backup Codes**
   - Generate 10 codes per user
   - Each code can only be used once
   - Store hashed in database
   - Regenerate after use

4. **Rate Limiting**
   - Implement login attempt limits
   - Lock accounts after multiple failures
   - Log all verification attempts

5. **Recovery Process**
   - Backup codes for lost devices
   - Admin override for emergencies
   - Email verification for 2FA reset

### Attack Mitigation

- **Brute Force**: Codes expire every 30 seconds
- **Replay Attacks**: Codes are one-time use
- **MITM**: Use HTTPS for all 2FA pages
- **Social Engineering**: Educate users about phishing

---

## 🧪 Testing

### Run crypto_core Tests

```bash
python crypto_core.py
```

Expected output:
```
[TEST 1] Base32 Encoding/Decoding - [PASS]
[TEST 2] HOTP (RFC 4226 Test Vectors) - [OK] x5
[TEST 3] TOTP - [PASS]
[TEST 4] Provisioning URI - Generated
[TEST 5] Backup Codes - Generated 5 codes
```

### Manual Testing

1. **Setup 2FA**
   - Visit `/2fa/setup/`
   - Scan QR code with Google Authenticator
   - Verify code works

2. **Test Login**
   - Logout and login again
   - Should prompt for 2FA code
   - Test both TOTP and backup codes

3. **Test Backup Codes**
   - Try logging in with a backup code
   - Code should only work once

---

## 📊 Database Schema

### TwoFactorAuth Table

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| user_id | ForeignKey | Reference to User |
| secret_key | CharField | Base32 encoded secret |
| is_enabled | Boolean | 2FA status |
| created_at | DateTime | Setup date |
| last_used | DateTime | Last verification |

### BackupCode Table

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| twofa_id | ForeignKey | Reference to TwoFactorAuth |
| code | CharField | Backup code (XXXX-XXXX) |
| is_used | Boolean | Usage status |
| created_at | DateTime | Generation date |
| used_at | DateTime | Usage date |

### TwoFactorLog Table

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| user_id | ForeignKey | Reference to User |
| success | Boolean | Verification result |
| method | CharField | 'totp' or 'backup' |
| ip_address | IPAddress | Client IP |
| user_agent | TextField | Browser info |
| timestamp | DateTime | Attempt time |

---

## 🚧 Troubleshooting

### Common Issues

**1. QR Code Not Displaying**
- Check if QRCode.js library is loaded
- Verify provisioning URI is correct
- Check browser console for errors

**2. Codes Not Working**
- Verify server time is correct: `date`
- Check time zone settings
- Ensure authenticator app time is synced

**3. "Invalid Code" Error**
- Try the next code (wait 30 seconds)
- Check if caps lock is on
- Use backup code as alternative

**4. Lost Authenticator App**
- Use backup codes
- Contact administrator for reset
- Generate new backup codes after recovery

**5. Backup Codes Not Generated**
- Check database connection
- Verify migrations ran successfully
- Check logs for errors

---

## 📚 References

- [RFC 4226 - HOTP](https://tools.ietf.org/html/rfc4226)
- [RFC 6238 - TOTP](https://tools.ietf.org/html/rfc6238)
- [RFC 4648 - Base32](https://tools.ietf.org/html/rfc4648)
- [Google Authenticator](https://github.com/google/google-authenticator)

---

## 🤝 Contributing

Improvements welcome:

1. Enhanced UI/UX
2. Additional authenticator app support
3. SMS/Email fallback
4. Biometric authentication
5. WebAuthn/FIDO2 support

---

## 📄 License

MIT License - Same as main project

---

## 👤 Author

News Portal Development Team

---

**Security Notice**: This implementation has been thoroughly tested but should undergo a professional security audit before use in production environments.
