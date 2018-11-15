# -*- coding: utf-8 -*-
from django.db.models import Sum
from django.http import HttpResponse
import json
from django.shortcuts import render
from core.reports.forms import ReportForm
from core.employees.models import *
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *

@access_module
@csrf_exempt
def salary_report(request):
    data = get_module_options(request)
    if request.method == 'GET':
        data['title'] = 'Reporte de Empleados y Salarios'
        data['form'] = ReportForm(request.user.bodega_id)
        return render(request, 'salary_report/salary_report_rp.html', data)
    elif request.method == 'POST':
        year = request.POST['year']
        month = request.POST['month']
        cont = request.POST['cont']
        data = []
        try:
            items = Salary.objects.filter()
            if month is None or month == "":
                month = "0"
            if len(cont):
                items = items.filter(cont_id=cont)
            if len(year):
                items = items.filter(year=year)
            if len(month) and month != "0":
                items = items.filter(month=month)
            total = items.aggregate(resp=Coalesce(Sum('total'), 0.00))['resp']
            for i in items:
                data.append([i.cont_id, i.cont.pers.names, i.year, i.get_month_display(),  i.cont.rmu_format(),format(i.cont.get_day_salary(), '.2f'), i.falts, i.dscto_format(), i.total_format()])
            data.append(['-------','-------','-------','-------','-------','-------','-------','-------',format(total, '.2f')])
        except Exception as e:
            data = {}
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
