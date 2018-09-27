from django.conf.urls import re_path
from core.ingress.views.provider.views import provider
from core.ingress.views.category.views import category
from core.ingress.views.brand.views import brand
from core.ingress.views.product.views import product
from core.ingress.views.ingress.views import ingress

urlpatterns = [
    re_path(r'^provider$', provider, name='provider'),
    re_path(r'^brand$', brand, name='brand'),
    re_path(r'^category$', category, name='category'),
    re_path(r'^product$', product, name='product'),
    re_path(r'^$', ingress, name='ingress'),
]