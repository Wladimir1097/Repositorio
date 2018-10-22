from django.conf.urls import re_path
from core.reports.views.expenses_report.views import expenses_report
from core.reports.views.sales_report.views import sales_report
from core.reports.views.salary_report.views import salary_report
from core.reports.views.ingress_report.views import ingress_report
from core.reports.views.services_report.views import services_report
from core.reports.views.inventory_report.views import inventory_report
from core.reports.views.results_report.views import results_report
from core.reports.views.orders_report.views import orders_report
from core.reports.views.cli_prod_report.view import cli_prod_report
from core.reports.views.med_report.view import med_report

urlpatterns = [
    re_path(r'^expenses_report$', expenses_report, name='expenses_report'),
    re_path(r'^sales_report$', sales_report, name='sales_report'),
    re_path(r'^salary_report$', salary_report, name='salary_report'),
    re_path(r'^ingress_report$', ingress_report, name='ingress_report'),
    re_path(r'^services_report$', services_report, name='services_report'),
    re_path(r'^inventory_report$', inventory_report, name='inventory_report'),
    re_path(r'^results_report$', results_report, name='results_report'),
    re_path(r'^orders_report$', orders_report, name='orders_report'),
    re_path(r'^cli_prod_report', cli_prod_report, name='cli_prod_report'),
    re_path(r'^med_report', med_report, name='med_report'),
]