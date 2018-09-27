from django.conf.urls import re_path
from .views.module.views import module
from .views.groups.views import groups
from .views.access_users.views import access_users
from .views.database.views import database
from .views.module_type.views import module_type

urlpatterns = [
    re_path(r'^groups$', groups, name='groups'),
    re_path(r'^module$', module, name='module'),
    re_path(r'^database$', database, name='database'),
    re_path(r'^access_users$', access_users, name='access_users'),
    re_path(r'^module_type$', module_type, name='module_type'),
]