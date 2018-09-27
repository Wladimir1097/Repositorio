from django.conf.urls import re_path
from core.dashboard.views.dashboard.views import *

urlpatterns = [
    re_path(r'^$', dashboard, name='dashboard'),
]
