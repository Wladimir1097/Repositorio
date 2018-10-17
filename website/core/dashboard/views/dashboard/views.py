import socket
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from core.employees.models import *
from core.security.decorators.module.decorators import get_modules_hrz_vrt_treev
from core.company.models import *
from core.sales.models import *
import json

from core.users.models import User


@login_required
def dashboard(request):
    data = {
        'title': 'Panel de Administración',
        'vents': Sales.objects.filter()[:10],
        'prodts': Product.objects.filter(stock__gt=0, bodega_id=request.user.bodega_id).order_by('stock')[:10],
        'sales_by_month': json.dumps(Sales().sales_by_month())
    }
    get_modules_hrz_vrt_treev(request)
    return render(request, 'bs_panel.html', data)


def information(request):
    try:
        data = {
            'icon_base64': Company.objects.all()[0].get_icon_base64(),
            'comp': Company.objects.first(),
            'clientes': Client.objects.filter(bodega_id=request.user.bodega_id).count(),
            'usuarios': User.objects.filter(bodega_id=request.user.bodega_id).count(),
            'productos': Product.objects.filter(bodega_id=request.user.bodega_id).count(),
            'ingresos': Ingress.objects.filter(usuario_id__bodega_id=request.user.bodega_id).count(),
            'hostname': socket.gethostname(),
            'localhost': socket.gethostbyname(socket.gethostname()),
            'date_joined': datetime.now(),
            'year': datetime.now().year,
        }
    except Exception as e:
        data = {
            'icon_base64': Company.objects.all()[0].get_icon_base64(),
            'comp': Company.objects.first(),
            'clientes': 0,
            'usuarios': 0,
            'productos': 0,
            'ingresos':0,
            'hostname': socket.gethostname(),
            'localhost': socket.gethostbyname(socket.gethostname()),
            'date_joined': datetime.now(),
            'year': datetime.now().year,
        }
    return data


def handler404(request):
    return HttpResponseRedirect('/login')


def handler500(request):
    return HttpResponseRedirect('/login')


def login_default(request):
    return HttpResponseRedirect('/login')
