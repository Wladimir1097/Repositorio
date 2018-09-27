# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.employees.forms import *

@csrf_exempt
@access_module
def faults(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'faults/faults_frm.html'
            if action == 'new':
                data['form'] = FaultsForm()
                data['title'] = 'Nuevo Registro de una Falta'
                data['button'] = 'Guardar Falta'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Faults.objects.filter(pk=id).exists():
                    model = Faults.objects.get(pk=id)
                    data['form'] = FaultsForm(instance=model, initial={'id': model.id}, action=True)
                    data['title'] = 'Edición de una Sanción'
                    data['button'] = 'Editar Sanción'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Faults.objects.all().order_by('id')
            data['title'] = 'Listado de Faltas'
            data['button'] = 'Nueva Falta'
            template = 'faults/faults_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = FaultsForm(request.POST, request.FILES)
                elif action == 'edit':
                    f = FaultsForm(request.POST, request.FILES, instance=Faults.objects.get(pk=request.POST['id']),action=True)
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Faults.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'load':
                data = [[i.id, i.date_joined_format(), i.cont.get_nro() ,i.cont.pers.names, i.cont.pers.dni, i.details, True] for i in Faults.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
