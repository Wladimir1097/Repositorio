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
        filtro = request.POST['filter']
        month = request.POST['month']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        year = request.POST['year']
        prod = request.POST.getlist("prod[]")
        data = []
        if month == "" and filtro == '3':
            filtro = '2'
        try:
            print(filtro)
            items = Product.objects.filter(bodega=request.user.bodega_id)
            if len(prod):
                for x in prod:
                    items = Product.objects.filter(bodega=request.user.bodega_id)
                    items = items.filter(id=x)
                    if filtro == '1':
                        for i in items:
                            data.append(
                                [i.id, i.name, i.cost_format(), i.stock, i.get_ingress_range(start_date, end_date),
                                 i.get_sales_range(start_date, end_date), i.get_pedids_range(start_date, end_date)])

                    elif filtro == '2':
                        for i in items:
                            data.append(
                                [i.id, i.name, i.cost_format(), i.stock, i.get_ingress_year(year),
                                 i.get_sales_year(year), i.get_pedids_year(year)])

                    elif filtro == '3':
                        print(year, month)
                        for i in items:
                            data.append(
                                [i.id, i.name, i.cost_format(), i.stock, i.get_ingress_year_month(year, month),
                                 i.get_sales_year_month(year, month), i.get_pedids_year_month(year, month)])

                    else:
                        for i in items:
                            data.append(
                                [i.id, i.name, i.cost_format(), i.stock, i.get_ingress(), i.get_sales(),
                                 i.get_pedids()])

            else:
                if filtro == '1':
                    for i in items:
                        data.append(
                            [i.id, i.name, i.cost_format(), i.stock, i.get_ingress_range(start_date, end_date),
                             i.get_sales_range(start_date, end_date), i.get_pedids_range(start_date, end_date)])

                elif filtro == '2':
                    for i in items:
                        data.append(
                            [i.id, i.name, i.cost_format(), i.stock, i.get_ingress_year(year),
                             i.get_sales_year(year), i.get_pedids_year(year)])

                elif filtro == '3':
                    print(year, month)
                    for i in items:
                        data.append(
                            [i.id, i.name, i.cost_format(), i.stock, i.get_ingress_year_month(year, month),
                             i.get_sales_year_month(year, month), i.get_pedids_year_month(year, month)])

                else:
                    for i in items:
                        data.append(
                            [i.id, i.name, i.cost_format(), i.stock, i.get_ingress(), i.get_sales(), i.get_pedids()])

        except Exception as e:
            data = {'error': str(e), 'resp': False}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
