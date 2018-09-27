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
def ingress_report(request):
    data = get_module_options(request)
    if request.method == 'GET':
        data['title'] = 'Reporte de Compras'
        data['form'] = ReportForm()
        return render(request, 'ingress_report/ingress_report_rp.html', data)
    elif request.method == 'POST':
        filter = request.POST['filter']
        month = request.POST['month']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        year = request.POST['year']
        provs = request.POST['provs']
        if month == "" and filter == '3':
            filter = '2'
        try:
            items = Ingress.objects.filter()
            if len(provs):
                items = items.filter(prov_id=provs)
            if filter == '1':
                items = items.filter(date_joined__range=[start_date, end_date])
            elif filter == '2':
                items = items.filter(date_joined__year=year)
            elif filter == '3':
                items = items.filter(date_joined__year=year, date_joined__month=month)
            subtotal = items.aggregate(resp=Coalesce(Sum('subtotal'), 0.00))['resp']
            dscto = items.aggregate(resp=Coalesce(Sum('dscto'), 0.00))['resp']
            iva = items.aggregate(resp=Coalesce(Sum('iva'), 0.00))['resp']
            total = items.aggregate(resp=Coalesce(Sum('total'), 0.00))['resp']
            data = [[i.id,i.prov.name,i.date_joined_format(),i.subtotal_format(),i.dscto_format(),i.iva_format(),i.total_format()] for i in items]
            data.append(['-------','-------','-------',format(subtotal,'.2f'),format(dscto,'.2f'),format(iva,'.2f'),format(total,'.2f')])
        except Exception as e:
            data = {}
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
