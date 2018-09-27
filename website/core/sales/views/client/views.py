# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.sales.forms import *

@csrf_exempt
@access_module
def client(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'client/client_frm.html'
            if action == 'new':
                data['form'] = ClientForm()
                data['title'] = 'Nuevo Registro de un Cliente'
                data['button'] = 'Guardar Cliente'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Client.objects.filter(pk=id).exists():
                    model = Client.objects.get(pk=id)
                    data['form'] = ClientForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de un Cliente'
                    data['button'] = 'Editar Cliente'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Client.objects.all().order_by('name')
            data['title'] = 'Listado de Clientes'
            data['button'] = 'Nuevo Cliente'
            template = 'client/client_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = ClientForm(request.POST)
                elif action == 'edit':
                    f = ClientForm(request.POST,instance=Client.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Client.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj'].strip()
                if type == 'name':
                    if id == 0:
                        if Client.objects.filter(name__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Client.objects.filter(name__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'ruc':
                    if id == 0:
                        if Client.objects.filter(ruc__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Client.objects.filter(ruc__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'phone':
                    if id == 0:
                        if Client.objects.filter(mobile__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Client.objects.filter(mobile__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'email':
                    if id == 0:
                        if Client.objects.filter(email__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Client.objects.filter(email__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load':
                data = [[c.id,c.name,c.ruc,c.mobile,c.address,True] for c in Client.objects.filter()]
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
