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
def services_report(request):
    data = get_module_options(request)
    if request.method == 'GET':
        data['title'] = 'Reporte de Servicios'
        data['form'] = ReportForm()
        return render(request, 'services_report/services_report_rp.html', data)
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
            items = SalesServices.objects.filter()
            if len(cli):
                items = items.filter(sales__cli_id=cli)
            if filter == '1':
                items = items.filter(sales__date_joined__range=[start_date, end_date])
            elif filter == '2':
                items = items.filter(sales__date_joined__year=year)
            elif filter == '3':
                items = items.filter(sales__date_joined__year=year, sales__date_joined__month=month)
            total = items.aggregate(resp=Coalesce(Sum('total'), 0.00))['resp']
            data = [[i.id,i.sales.get_nro(),i.sales.cli.name,i.sales.date_joined_format(),i.serv.name,i.total_format()] for i in items]
            data.append(['-------','-------','-------','-------','-------',format(total,'.2f')])
        except Exception as e:
            data = {}
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
