# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.company.forms import *

@csrf_exempt
@access_module
def expenses(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'expenses/expenses_frm.html'
            if action == 'new':
                data['form'] = ExpensesForm()
                data['title'] = 'Nuevo Gasto'
                data['button'] = 'Guardar Gasto'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Expenses.objects.filter(pk=id).exists():
                    model = Expenses.objects.get(pk=id)
                    data['form'] = ExpensesForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de un Gasto'
                    data['button'] = 'Editar Gasto'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Expenses.objects.all().order_by('id')
            data['title'] = 'Listado de Gastos'
            data['button'] = 'Nuevo Gasto'
            template = 'expenses/expenses_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                   f = ExpensesForm(request.POST)
                elif action == 'edit':
                   f = ExpensesForm(request.POST, instance=Expenses.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Expenses.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'load':
                data = [[i.id, i.type.name, i.details, i.date_joined_format(), i.cost_format(), True] for i in Expenses.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
