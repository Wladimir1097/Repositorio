# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.sales.forms import *


@csrf_exempt
@access_module
def devolution(request):
    data = get_module_options(request)
    if request.method == 'GET':
        data['title'] = 'Listado de Devoluciones de Productos'
        return render(request, 'devolution/devolution_dt.html', data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'delete':
                dev = DevolutionSales.objects.get(pk=request.POST['id'])
                det = SalesProducts.objects.get(pk=dev.det_id)
                det.cant += dev.cant
                det.save()
                prod = Product.objects.get(pk=det.prod_id)
                prod.stock -= det.cant
                prod.save()
                det.sales.get_totals()
                dev.delete()
                data['resp'] = True
            elif action == 'load':
                data = [[d.id, d.det.sales.get_nro(), d.det.id, d.det.prod.name, d.date_joined_format(), d.cant, True]
                        for d in DevolutionSales.objects.filter()]
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
