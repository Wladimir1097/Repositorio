from django.conf.urls import re_path
from .views.company.views import company
from .views.expenses.views import expenses
from .views.type_expense.views import type_expense
from .views.tools.views import tools
from .views.bodega.views import bodega

urlpatterns = [
    re_path(r'^$', company, name='company'),
    re_path(r'^expenses$', expenses, name='expenses'),
    re_path(r'^type_expense$', type_expense, name='type_expense'),
    re_path(r'^tools$', tools, name='tools'),
    re_path(r'^bodega$', bodega, name='bodega'),
]
