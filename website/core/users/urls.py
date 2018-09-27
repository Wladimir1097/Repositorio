from django.conf.urls import re_path
from .views.users.views import *

urlpatterns = [
    re_path(r'^$', users, name='users'),
    re_path(r'^change_profile', change_profile, name='change_profile'),
    re_path(r'^change_groups', change_groups, name='change_groups'),
]