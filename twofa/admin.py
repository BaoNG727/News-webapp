from django.contrib import admin
from .models import TwoFactorAuth, BackupCode, TwoFactorLog


@admin.register(TwoFactorAuth)
class TwoFactorAuthAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_enabled', 'created_at', 'last_used']
    list_filter = ['is_enabled', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'last_used']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'is_enabled')
        }),
        ('Secret Key', {
            'fields': ('secret_key',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_used'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent manual creation through admin
        return False


@admin.register(BackupCode)
class BackupCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'twofa', 'is_used', 'created_at', 'used_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['code', 'twofa__user__username']
    readonly_fields = ['created_at', 'used_at']
    
    def has_add_permission(self, request):
        return False


@admin.register(TwoFactorLog)
class TwoFactorLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'method', 'success', 'ip_address', 'timestamp']
    list_filter = ['success', 'method', 'timestamp']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['user', 'success', 'method', 'ip_address', 'user_agent', 'timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
