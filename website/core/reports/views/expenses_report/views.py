# -*- coding: utf-8 -*-
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
import json
from django.shortcuts import render
from core.reports.forms import ReportForm
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.company.models import *

@access_module
@csrf_exempt
def expenses_report(request):
    data = get_module_options(request)
    if request.method == 'GET':
        data['title'] = 'Reporte de Gastos'
        data['form'] = ReportForm()
        return render(request, 'expenses_report/expenses_report_rp.html', data)
    elif request.method == 'POST':
        filter = request.POST['filter']
        month = request.POST['month']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        year = request.POST['year']
        type_expenses = request.POST['type_expenses']
        if month == "" and filter == '3':
            filter = '2'
        try:
            items = Expenses.objects.filter()
            if len(type_expenses):
                items = items.filter(type_id=type_expenses)
            if filter == '1':
                items = items.filter(date_joined__range=[start_date, end_date])
            elif filter == '2':
                items = items.filter(date_joined__year=year)
            elif filter == '3':
                items = items.filter(date_joined__year=year, date_joined__month=month)
            total = items.aggregate(resp=Coalesce(Sum('cost'), 0.00))['resp']
            data = [[i.id,i.type.name,i.details,i.date_joined_format(),i.cost_format()] for i in items]
            data.append(['-------','-------','-------','-------',format(total,'.2f')])
        except Exception as e:
            data = {}
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
