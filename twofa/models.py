from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import sys
import os

# Add parent directory to path to import crypto_core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto_core import Base32, TwoFactorUtils


class TwoFactorAuth(models.Model):
    """
    Stores 2FA configuration for each user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='twofa')
    secret_key = models.CharField(max_length=100, help_text="Base32 encoded secret key")
    is_enabled = models.BooleanField(default=False, help_text="Is 2FA enabled for this user")
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Two-Factor Authentication"
        verbose_name_plural = "Two-Factor Authentications"
        db_table = 'twofa_auth'
    
    def __str__(self):
        return f"2FA for {self.user.username} ({'Enabled' if self.is_enabled else 'Disabled'})"
    
    @classmethod
    def create_for_user(cls, user):
        """
        Create 2FA configuration for a user with a new secret.
        """
        secret_b32 = TwoFactorUtils.generate_secret_base32()
        return cls.objects.create(user=user, secret_key=secret_b32, is_enabled=False)
    
    def get_secret_bytes(self):
        """
        Get secret as bytes for TOTP generation.
        """
        return Base32.decode(self.secret_key)
    
    def regenerate_secret(self):
        """
        Generate a new secret key.
        """
        self.secret_key = TwoFactorUtils.generate_secret_base32()
        self.save()
    
    def enable(self):
        """
        Enable 2FA for this user.
        """
        self.is_enabled = True
        self.save()
    
    def disable(self):
        """
        Disable 2FA for this user.
        """
        self.is_enabled = False
        self.save()
    
    def mark_used(self):
        """
        Update last used timestamp.
        """
        self.last_used = timezone.now()
        self.save(update_fields=['last_used'])


class BackupCode(models.Model):
    """
    Stores backup recovery codes for 2FA.
    """
    twofa = models.ForeignKey(TwoFactorAuth, on_delete=models.CASCADE, related_name='backup_codes')
    code = models.CharField(max_length=20, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Backup Code"
        verbose_name_plural = "Backup Codes"
        db_table = 'twofa_backup_codes'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['twofa', 'is_used']),
        ]
    
    def __str__(self):
        return f"{self.code} ({'Used' if self.is_used else 'Active'})"
    
    def use(self):
        """
        Mark this backup code as used.
        """
        self.is_used = True
        self.used_at = timezone.now()
        self.save()
    
    @classmethod
    def generate_for_user(cls, twofa_obj, count=10):
        """
        Generate backup codes for a user's 2FA.
        """
        # Delete existing codes
        cls.objects.filter(twofa=twofa_obj).delete()
        
        # Generate new codes
        codes = TwoFactorUtils.generate_backup_codes(count)
        backup_objs = [cls(twofa=twofa_obj, code=code) for code in codes]
        cls.objects.bulk_create(backup_objs)
        
        return codes


class TwoFactorLog(models.Model):
    """
    Logs 2FA verification attempts for security auditing.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='twofa_logs')
    success = models.BooleanField(help_text="Was the verification successful")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=[
        ('totp', 'TOTP Code'),
        ('backup', 'Backup Code'),
    ])
    
    class Meta:
        verbose_name = "Two-Factor Log"
        verbose_name_plural = "Two-Factor Logs"
        db_table = 'twofa_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['success', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.method} - {'Success' if self.success else 'Failed'} at {self.timestamp}"
    
    @classmethod
    def log_attempt(cls, user, success, method='totp', ip_address=None, user_agent=''):
        """
        Create a log entry for a 2FA attempt.
        """
        return cls.objects.create(
            user=user,
            success=success,
            method=method,
            ip_address=ip_address,
            user_agent=user_agent
        )
