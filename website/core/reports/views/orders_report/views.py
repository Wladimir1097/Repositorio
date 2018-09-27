# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
from django.shortcuts import render
from core.reports.forms import ReportForm
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.sales.models import *

@access_module
@csrf_exempt
def orders_report(request):
    data = get_module_options(request)
    if request.method == 'GET':
        data['title'] = 'Reporte de Pedidos'
        data['form'] = ReportForm()
        return render(request, 'orders_report/orders_report_rp.html', data)
    elif request.method == 'POST':
        filter = request.POST['filter']
        month = request.POST['month']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        year = request.POST['year']
        cli = request.POST['cli']
        if month == "" and filter == '3':
            filter = '2'
        try:
            items = Sales.objects.filter(type=2)
            if len(cli):
                items = items.filter(cli_id=cli)
            if filter == '1':
                items = items.filter(date_joined__range=[start_date, end_date])
            elif filter == '2':
                items = items.filter(date_joined__year=year)
            elif filter == '3':
                items = items.filter(date_joined__year=year, date_joined__month=month)
            data = [[i.id,i.get_nro(),i.cli.name,i.date_joined_format(),i.count_products(), i.count_ent_products(),i.count_prods_rest()] for i in items]
        except Exception as e:
            data = {}
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
