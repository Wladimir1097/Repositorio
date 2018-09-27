"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from core.login.views.login import views as v_login
from config.settings import local
from core.dashboard.views.dashboard.views import handler404, handler500, login_default
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', login_default, name='login_default'),
    path('login/', include('core.login.urls')),
    path('dashboard/', include('core.dashboard.urls')),
    path('users/', include('core.users.urls')),
    path('security/', include('core.security.urls')),
    path('company/', include('core.company.urls')),
    path('ingress/', include('core.ingress.urls')),
    path('sales/', include('core.sales.urls')),
    path('employees/', include('core.employees.urls')),
    path('reports/', include('core.reports.urls')),
]

handler404 = handler404
handler500 = handler500

if local.DEBUG:
    urlpatterns += static(local.STATIC_URL, document_root=local.STATIC_ROOT)
    urlpatterns += static(local.MEDIA_URL, document_root=local.MEDIA_ROOT)
