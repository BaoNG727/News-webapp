from django.urls import re_path
from .import views

urlpatterns = [

re_path(r'^newsletter/add/$', views.news_letter, name='news_letter'),
re_path(r'^panel/newsletter/emails/$', views.news_emails, name='news_emails'),
re_path(r'^panel/newsletter/phones/$', views.news_phones, name='news_phones'),
re_path(r'^panel/newsletter/del/(?P<pk>\d+)/(?P<num>\d+)/$', views.news_txt_del, name='news_txt_del'),

]