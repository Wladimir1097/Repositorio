from django.conf.urls import re_path
from core.sales.views.client.views import client
from core.sales.views.services.views import services
from core.sales.views.sales.views import sales
from core.sales.views.devolution.views import devolution
from core.sales.views.medidores.view import medidores

urlpatterns = [
    re_path(r'^client$', client, name='client'),
    re_path(r'^services$', services, name='services'),
    re_path(r'^$', sales, name='sales'),
    re_path(r'^devolution$', devolution, name='devolution'),
    re_path(r'^medidores$', medidores, name='medidores'),
]
