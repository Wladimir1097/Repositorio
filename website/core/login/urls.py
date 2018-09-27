from django.conf.urls import re_path
from django.contrib.auth.views import logout_then_login
from .views.login.views import session_login

urlpatterns = [
    re_path(r'^$',session_login, name='login'),
    re_path(r'^logout/$', logout_then_login,name='logout'),
]
