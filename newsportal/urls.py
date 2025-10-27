from django.urls import include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

#from django.urls import path

urlpatterns = [
    
    re_path(r'^admin/' , admin.site.urls),      # Django Default Admin Panel
    re_path(r'', include('main.urls')),         # here main is an app name
    re_path(r'', include('news.urls')),         # here news is an app name
    re_path(r'', include('cat.urls')),          # here cat is an app name
    re_path(r'', include('subcat.urls')),       # here subcat is an app name
    re_path(r'', include('contactform.urls')),  # here contactform is an app name
    re_path(r'', include('trending.urls')),     # here trending is an app name
    re_path(r'', include('manager.urls')),      # here manager is an app name
    re_path(r'', include('newsletter.urls')),   # here newsletter is an app name
    re_path(r'', include('comment.urls')),      # here comment is an app name
    re_path(r'', include('blacklist.urls')),    # here blacklist is an app name (for IP)
    re_path(r'^2fa/', include('twofa.urls')),   # here twofa is an app name (Two-Factor Authentication)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)