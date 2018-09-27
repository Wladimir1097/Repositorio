# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
from django.shortcuts import render
from core.company.models import Expenses
from core.employees.models import Salary
from core.reports.forms import ReportForm
from core.sales.models import Sales
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.ingress.models import *

@access_module
@csrf_exempt
def results_report(request):
    data = get_module_options(request)
    if request.method == 'GET':
        data['title'] = 'Reporte de Ganancias y Perdidas'
        data['form'] = ReportForm()
        return render(request, 'results_report/result_report_rp.html', data)
    elif request.method == 'POST':
        filter = request.POST['filter']
        month = request.POST['month']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        year = request.POST['year']
        if month == "" and filter == '3':
            filter = '2'
        try:
            data = []
            purchase = Ingress.objects.filter()
            sales = Sales.objects.filter(type=1)
            pedids = Sales.objects.filter(type=2)
            expenses = Expenses.objects.filter()
            salary = Salary.objects.filter()
            if filter == '1':
                purchase = purchase.filter(date_joined__range=[start_date, end_date])
                sales = sales.filter(date_joined__range=[start_date, end_date])
                pedids = pedids.filter(date_joined__range=[start_date, end_date])
                expenses = expenses.filter(date_joined__range=[start_date, end_date])
                salary = salary.filter(date_joined__range=[start_date, end_date])
            elif filter == '2':
                purchase = purchase.filter(date_joined__year=year)
                sales = sales.filter(date_joined__year=year)
                pedids = pedids.filter(date_joined__year=year)
                expenses = expenses.filter(date_joined__year=year)
                salary = salary.filter(year=year)
            elif filter == '3':
                purchase = purchase.filter(date_joined__year=year, date_joined__month=month)
                sales = sales.filter(date_joined__year=year, date_joined__month=month)
                pedids = pedids.filter(date_joined__year=year, date_joined__month=month)
                expenses = expenses.filter(date_joined__year=year, date_joined__month=month)
                salary = salary.filter(year=year, month=month)
            purchase = purchase.aggregate(resp=Coalesce(Sum('total'), 0.00))['resp']
            sales = sales.aggregate(resp=Coalesce(Sum('total'), 0.00))['resp']
            pedids = pedids.aggregate(resp=Coalesce(Sum('total'), 0.00))['resp']
            expenses = expenses.aggregate(resp=Coalesce(Sum('cost'), 0.00))['resp']
            salary = salary.aggregate(resp=Coalesce(Sum('total'), 0.00))['resp']
            utility = sales - expenses - purchase - salary + pedids
            status = 2
            if utility > 0:
                status = 1
            elif utility < 0:
                status = 3
            data.append([format(purchase,'.2f'),format(expenses,'.2f'),format(salary,'.2f'),format(sales,'.2f'),format(pedids,'.2f'),format(utility,'.2f'),status])
        except Exception as e:
            data = {}
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)


# for i in Sales.objects.filter():
#     i.get_totals()
# print("Terminado")