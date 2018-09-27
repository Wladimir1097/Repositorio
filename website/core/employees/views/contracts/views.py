# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.employees.forms import *

@csrf_exempt
@access_module
def contracts(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'contracts/contracts_frm.html'
            if action == 'new':
                data['form'] = ContractsForm()
                data['title'] = 'Nuevo Registro de un Empleado'
                data['button'] = 'Guardar Empleado'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Contracts.objects.filter(pk=id).exists():
                    model = Contracts.objects.get(pk=id)
                    data['form'] = ContractsForm(instance=model, initial={'id': model.id}, action=True)
                    data['title'] = 'Edición de un Empleado'
                    data['button'] = 'Editar Empleado'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Contracts.objects.all().order_by('id')
            data['title'] = 'Listado de Empleados'
            data['button'] = 'Nuevo Empleado'
            template = 'contracts/contracts_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = ContractsForm(request.POST)
                    Contracts.objects.filter(pers_id=request.POST['pers']).update(is_active=False)
                elif action == 'edit':
                    f = ContractsForm(request.POST, instance=Contracts.objects.get(pk=request.POST['id']), action=True)
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Contracts.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'load':
                data = [
                    [i.id, i.pers.names, i.pers.dni, i.start_date_format(), i.end_date_format(),i.rmu_format(), i.is_active, True] for i in Contracts.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
