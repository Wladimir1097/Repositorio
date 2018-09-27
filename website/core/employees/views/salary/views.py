# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from config.settings.base import HOME
from core.security.decorators.module.decorators import access_module
from core.employees.forms import *
from core.security.views.module.views import get_module_options

@csrf_exempt
@access_module
def salary(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        data['form'] = SalaryForm()
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'salary/salary_frm.html'
            if action == 'new':
                data['title'] = 'Registro de un Nuevo Rol de Salarios'
                data['button'] = 'Guardar Salario'
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = []
            data['title'] = 'Listado de Salarios'
            data['button'] = 'Generar Salarios'
            template = 'salary/salary_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                month = request.POST['month']
                year = request.POST['year']
                if exists_salary(year, month):
                    for c in Contracts.objects.filter(is_active=True):
                        dscto = c.get_dsctos(year=year, month=month)
                        salary_neto = float(c.rmu) - dscto
                        s = Salary()
                        s.cont = c
                        s.month = month
                        s.falts = c.get_falts_count(year=year, month=month)
                        s.year = year
                        s.dscto = dscto
                        s.total = salary_neto
                        s.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = 'Ya se encuentra registrado este rol de sueldo con este año y mes'
            elif action == 'generate_salaries':
                data = []
                month = request.POST['month']
                year = request.POST['year']
                if exists_salary(year,month):
                    for c in Contracts.objects.filter(is_active=True):
                        falts = c.get_falts_count(year=year, month=month)
                        salary_day = c.get_day_salary()
                        dscto = c.get_dsctos(year=year, month=month)
                        salary_neto = float(c.rmu) -float(dscto)
                        m = months_choices[int(month)][1]
                        data.append([c.id,c.pers.names, year, m, c.rmu_format(), format(salary_day, '.2f'), falts, format(dscto, '.2f'),salary_neto])
            elif action == 'delete':
                Salary.objects.filter(year=request.POST['year'],month=request.POST['month']).delete()
                data['resp'] = True
            elif action == 'search_salaries':
                data = []
                month = request.POST['month']
                year = request.POST['year']
                if len(year) and len(month):
                    for s in Salary.objects.filter(year=year,month=month):
                        data.append([s.id, s.cont.pers.names, year,s.get_month_display(), s.cont.rmu_format(), format(s.cont.get_day_salary(), '.2f'),s.falts,s.dscto_format(), s.total_format()])
            elif action == 'repeated':
                id = request.POST['id']
                year = request.POST['year']
                month = request.POST['month']
                if len(year) and len(month):
                    if id == 0:
                        if Salary.objects.filter(month=month,year=year):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Salary.objects.filter(month=month, year=year).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'get_dscto_salary':
                data = []
                for i in Faults.objects.filter(cont_id=request.POST['id'], date_joined__year=request.POST['year'], date_joined__month=request.POST['month']):
                    data.append([i.id, i.date_joined_format(), i.details])
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)

def exists_salary(year,month):
    return len(year) and len(month) and not Salary.objects.filter(year=year,month=month)

