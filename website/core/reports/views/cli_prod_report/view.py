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
def cli_prod_report(request):
    data = get_module_options(request)
    if request.method == 'GET':
        data['title'] = 'Reporte de Materiales'
        data['form'] = ReportForm(request.user.bodega_id)
        return render(request, 'cli_prod_report/cli_prod_report_rp.html', data)
    elif request.method == 'POST':
        filter = request.POST['filter']
        month = request.POST['month']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        year = request.POST['year']
        cli = request.POST['cli']
        prod = request.POST['prod']
        data = []
        if month == "" and filter == '3':
            filter = '2'
        try:
            items = Sales.objects.filter(type=1, usuario_id__bodega_id=request.user.bodega_id)
            productos = SalesProducts.objects.all()
            if len(prod):
                productos = productos.filter(prod=prod)
            if len(cli):
                items = items.filter(cli_id=cli)
            if filter == '1':
                items = items.filter(date_joined__range=[start_date, end_date])
            elif filter == '2':
                items = items.filter(date_joined__year=year)
            elif filter == '3':
                items = items.filter(date_joined__year=year, date_joined__month=month)

            for i in items:
                for j in productos.filter(sales=i.id):
                    data.append([i.id, i.get_nro(), i.date_joined_format(), i.cli.name, j.prod.name,
                                 format(float(j.subtotal_format()) * int(j.cant), '.2f'), j.cant])
        except Exception as e:
            data = {}
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
