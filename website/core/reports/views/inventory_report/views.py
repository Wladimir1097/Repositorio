# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
from django.shortcuts import render
from core.reports.forms import ReportForm
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.ingress.models import *

@access_module
@csrf_exempt
def inventory_report(request):
    data = get_module_options(request)
    if request.method == 'GET':
        data['title'] = 'Reporte de Inventarios'
        data['form'] = ReportForm(request.user.bodega_id)
        return render(request, 'inventory_report/inventory_report_rp.html', data)
    elif request.method == 'POST':
        prod = request.POST['prod']
        data = []
        try:
            items = Product.objects.filter(bodega=request.user.bodega_id)
            if len(prod):
                items = items.filter(id=prod)
            for i in items:
                data.append([i.id, i.name, i.cost_format(), i.stock, i.get_ingress(), i.get_sales(), i.get_pedids()])
        except Exception as e:
            data = {}
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
