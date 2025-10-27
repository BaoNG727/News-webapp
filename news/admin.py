from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'catname', 'writer', 'show', 'act', 'created_at']
    list_filter = ['act', 'catname', 'created_at']
    search_fields = ['name', 'short_txt', 'body_txt', 'tag']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'show', 'rand']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'short_txt', 'body_txt')
        }),
        ('Media', {
            'fields': ('picname', 'picurl')
        }),
        ('Category & Tags', {
            'fields': ('catname', 'catid', 'ocatid', 'tag')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('writer', 'act', 'date', 'time', 'created_at', 'updated_at')
        }),
        ('Statistics', {
            'fields': ('show', 'rand'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(writer=request.user.username)