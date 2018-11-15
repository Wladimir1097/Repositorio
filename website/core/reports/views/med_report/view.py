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
def med_report(request):
    data = get_module_options(request)
    if request.method == 'GET':
        data['title'] = 'Reporte de Medidores & Sellos'
        data['form'] = ReportForm(request.user.bodega_id)
        return render(request, 'med_report/med_report_rp.html', data)
    elif request.method == 'POST':
        filter = request.POST['filter']
        month = request.POST['month']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        year = request.POST['year']
        cli = request.POST['cli']
        type = request.POST['type']
        bod = request.POST['bod']
        data = []
        if month == "" and filter == '3':
            filter = '2'
        try:
            items = InventoryMedidor.objects.filter(usuario_id__bodega_id=request.user.bodega_id)
            items1 = InventorySello.objects.filter(usuario_id__bodega_id=request.user.bodega_id)
            if len(cli):
                print(cli)
                items = items.filter(cli_id=cli)
                items1 = items1.filter(cli_id=cli)
                print(items)
            if len(bod):
                if bod == '1':
                    items = items.filter(distribuido=True)
                    items1 = items1.filter(distribuido=True)
                elif bod == '2':
                    items = items.filter(distribuido=False)
                    items1 = items1.filter(distribuido=False)
            if filter == '1':
                items = items.filter(date_joined__range=[start_date, end_date])
                items1 = items1.filter(date_joined__range=[start_date, end_date])
            elif filter == '2':
                items = items.filter(date_joined__year=year)
                items1 = items1.filter(date_joined__year=year)
            elif filter == '3':
                items = items.filter(date_joined__year=year, date_joined__month=month)
                items1 = items1.filter(date_joined__year=year, date_joined__month=month)
            if not len(type):
                for i in items:
                    data.append(
                        [i.id, i.date_joined_format(), '---' if i.cli_id is None else i.cli.name, i.numeracion,
                         i.medtype.name, 'ProEnergy' if i.distribuido is True else 'Wagner'])
                for i in items1:
                    data.append(
                        [i.id, i.date_joined_format(), '---' if i.cli_id is None else i.cli.name, i.numeracion,
                         '------', 'ProEnergy' if i.distribuido is True else 'Wagner'])
            elif type == '1':
                for i in items:
                    data.append(
                        [i.id, i.date_joined_format(), '---' if i.cli_id is None else i.cli.name, i.numeracion,
                         i.medtype.name, 'ProEnergy' if i.distribuido is True else 'Wagner'])
            elif type == '2':
                for i in items1:
                    data.append(
                        [i.id, i.date_joined_format(), '---' if i.cli_id is None else i.cli.name, i.numeracion,
                         '------', 'ProEnergy' if i.distribuido is True else 'Wagner'])
        except Exception as e:

            print('se sale')
            data = {}
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
