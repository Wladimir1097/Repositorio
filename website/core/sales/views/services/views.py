# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.sales.forms import *

@csrf_exempt
@access_module
def services(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'services/services_frm.html'
            if action == 'new':
                data['form'] = ServicesForm()
                data['title'] = 'Nuevo Registro de un Servicio'
                data['button'] = 'Guardar Servicio'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Services.objects.filter(pk=id).exists():
                    model = Services.objects.get(pk=id)
                    data['form'] = ServicesForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de un Servicio'
                    data['button'] = 'Editar Servicio'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Services.objects.all().order_by('name')
            data['title'] = 'Listado de Servicios'
            data['button'] = 'Nuevo Servicio'
            template = 'services/services_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = ServicesForm(request.POST)
                elif action == 'edit':
                    f = ServicesForm(request.POST,instance=Services.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Services.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj'].strip()
                if type == 'name':
                    if id == 0:
                        if Services.objects.filter(name__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Client.objects.filter(name__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load':
                data = [[c.id,c.name,c.cost_format(),True] for c in Services.objects.filter()]
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
