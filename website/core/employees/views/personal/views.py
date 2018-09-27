# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.employees.forms import *

@csrf_exempt
@access_module
def personal(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'personal/personal_frm.html'
            if action == 'new':
                data['form'] = PersonalForm()
                data['title'] = 'Nuevo Registro de un Empleado'
                data['button'] = 'Guardar Empleado'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Personal.objects.filter(pk=id).exists():
                    model = Personal.objects.get(pk=id)
                    data['form'] = PersonalForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de un Empleado'
                    data['button'] = 'Editar Empleado'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Personal.objects.all().order_by('name')
            data['title'] = 'Listado de Empleados'
            data['button'] = 'Nuevo Empleado'
            template = 'personal/personal_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = PersonalForm(request.POST, request.FILES)
                elif action == 'edit':
                    f = PersonalForm(request.POST, request.FILES, instance=Personal.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Personal.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj'].strip()
                if type == 'mobile':
                    if id == 0:
                        if Personal.objects.filter(mobile__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Personal.objects.filter(mobile__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'dni':
                    if id == 0:
                        if Personal.objects.filter(dni__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Personal.objects.filter(dni__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'email':
                    if id == 0:
                        if Personal.objects.filter(email__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Personal.objects.filter(email__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load':
                data = [[c.id, c.get_avatar(),c.names,c.dni,c.mobile,c.email,c.address,True] for c in Personal.objects.filter()]
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
