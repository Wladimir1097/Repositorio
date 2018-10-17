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
def sales_report(request):
    data = get_module_options(request)
    if request.method == 'GET':
        data['title'] = 'Reporte de Egresos'
        data['form'] = ReportForm(request.user.bodega_id)
        return render(request, 'sales_report/sales_report_rp.html', data)
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
            items = Sales.objects.filter(type=1, usuario_id__bodega_id=request.user.bodega_id)
            if len(cli):
                items = items.filter(cli_id=cli)
            if filter == '1':
                items = items.filter(date_joined__range=[start_date, end_date])
            elif filter == '2':
                items = items.filter(date_joined__year=year)
            elif filter == '3':
                items = items.filter(date_joined__year=year, date_joined__month=month)
            subtotal = items.aggregate(resp=Coalesce(Sum('subtotal'), 0.00))['resp']
            iva = items.aggregate(resp=Coalesce(Sum('iva'), 0.00))['resp']
            total = items.aggregate(resp=Coalesce(Sum('total'), 0.00))['resp']
            data = [[i.id, i.get_nro(), i.cli.name, i.date_joined_format(), i.subtotal_format(), i.iva_format(),
                     i.total_format()] for i in items]
            data.append(['-------', '-------', '-------', '-------', format(subtotal, '.2f'), format(iva, '.2f'),
                         format(total, '.2f')])
        except Exception as e:
            data = {}
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
