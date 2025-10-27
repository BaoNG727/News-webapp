from django.urls import re_path
from .import views

urlpatterns = [

re_path(r'^contact/submit/$', views.contact_add, name='contact_add'),  # when we click the send button, it will take me msgbox.html page
re_path(r'^panel/contactform/$', views.contact_show, name='contact_show'),  # This is for admin panel
re_path(r'^panel/contactform/del/(?P<pk>\d+)/$', views.contact_del, name='contact_del'),  ## Messages Delete in admin panel
]