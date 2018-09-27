# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.company.forms import *

@csrf_exempt
@access_module
def type_expense(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'type_expense/type_expense_frm.html'
            if action == 'new':
                data['form'] = TypeExpenseForm()
                data['title'] = 'Nuevo Tipo de Gasto'
                data['button'] = 'Guardar Tipo de Gasto'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if TypeExpense.objects.filter(pk=id).exists():
                    model = TypeExpense.objects.get(pk=id)
                    data['form'] = TypeExpenseForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de un Tipo de Gasto'
                    data['button'] = 'Editar Tipo de Gasto'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = TypeExpense.objects.all().order_by('id')
            data['title'] = 'Listado de Tipos de Gastos'
            data['button'] = 'Nuevo Tipo de Gasto'
            template = 'type_expense/type_expense_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = TypeExpenseForm(request.POST)
                elif action == 'edit':
                    f = TypeExpenseForm(request.POST, instance=TypeExpense.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                TypeExpense.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj']
                if type == 'name':
                    if id == 0:
                        if TypeExpense.objects.filter(name__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if TypeExpense.objects.filter(name__iexact=obj).exclude(pk=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load':
                data = [[i.id, i.name, True] for i in TypeExpense.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
