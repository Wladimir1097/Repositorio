from django.conf.urls import re_path
from core.employees.views.contracts.views import contracts
from core.employees.views.faults.views import faults
from core.employees.views.salary.views import salary
from core.employees.views.personal.views import personal

urlpatterns = [
    re_path(r'^personal$', personal, name='personal'),
    re_path(r'^faults$', faults, name='faults'),
    re_path(r'^contracts$', contracts, name='contracts'),
    re_path(r'^salary$', salary, name='salary'),
]
