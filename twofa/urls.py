from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^setup/$', views.setup_2fa, name='twofa_setup'),
    re_path(r'^backup-codes/$', views.backup_codes, name='twofa_backup_codes'),
    re_path(r'^manage/$', views.manage_2fa, name='twofa_manage'),
    re_path(r'^verify/$', views.verify_2fa, name='twofa_verify'),
    re_path(r'^verify-page/$', views.verify_2fa_page, name='twofa_verify_page'),
]
