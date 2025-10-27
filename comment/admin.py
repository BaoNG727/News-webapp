from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'get_comment_preview', 'news_id', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'cm']
    readonly_fields = ['created_at']
    actions = ['approve_comments', 'disapprove_comments']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('name', 'email', 'cm')
        }),
        ('Related News', {
            'fields': ('news_id',)
        }),
        ('Status & Date', {
            'fields': ('status', 'date', 'time', 'created_at')
        }),
    )
    
    def get_comment_preview(self, obj):
        return obj.cm[:50] + '...' if len(obj.cm) > 50 else obj.cm
    get_comment_preview.short_description = 'Comment'
    
    def approve_comments(self, request, queryset):
        queryset.update(status=1)
        self.message_user(request, f"{queryset.count()} comments approved successfully.")
    approve_comments.short_description = "Approve selected comments"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(status=0)
        self.message_user(request, f"{queryset.count()} comments disapproved.")
    disapprove_comments.short_description = "Disapprove selected comments"
