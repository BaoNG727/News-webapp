from django.urls import re_path
from .import views

urlpatterns = [

    re_path(r'^panel/category/list/$', views.cat_list, name='cat_list'),  ## For Admin Panel Category List
    re_path(r'^panel/category/add/$', views.cat_add, name='cat_add'),    ## For Admin Panel Category Add
    re_path(r'^export/cat/csv/$', views.export_cat_csv, name='export_cat_csv'),    ## To download/export csv file
    re_path(r'^import/cat/csv/$', views.import_cat_csv, name='import_cat_csv'),    ## To import csv file

]                                                                               






# word is a variable and d means digit. w means digit or number
# used P for received the value as a Parenthesis