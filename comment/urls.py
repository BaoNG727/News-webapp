from django.urls import re_path
from .import views

urlpatterns = [

re_path(r'^comment/add/news/(?P<pk>\d+)/$', views.news_cm_add, name='news_cm_add'),
re_path(r'^comments/list/', views.comments_list, name='comments_list'), # Cooments list in Panel
re_path(r'^comments/del/(?P<pk>\d+)/$', views.comments_del, name='comments_del'), # Cooments delete in Panel
re_path(r'^comments/confirm/(?P<pk>\d+)/$', views.comments_confirm, name='comments_confirm'), # Cooments Confirm in Panel
]