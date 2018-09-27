# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.ingress.forms import *

@csrf_exempt
@access_module
def provider(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'provider/provider_frm.html'
            if action == 'new':
                data['form'] = ProviderForm()
                data['title'] = 'Nuevo Registro de un Proveedor'
                data['button'] = 'Guardar Proveedor'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Provider.objects.filter(pk=id).exists():
                    model = Provider.objects.get(pk=id)
                    data['form'] = ProviderForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de un Proveedor'
                    data['button'] = 'Editar Proveedor'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Provider.objects.all().order_by('name')
            data['title'] = 'Listado de Proveedores'
            data['button'] = 'Nuevo Proveedor'
            template = 'provider/provider_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = ProviderForm(request.POST, request.FILES)
                elif action == 'edit':
                    f = ProviderForm(request.POST, request.FILES, instance=Provider.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Provider.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj'].strip()
                if type == 'name':
                    if id == 0:
                        if Provider.objects.filter(name__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Provider.objects.filter(name__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'ruc':
                    if id == 0:
                        if Provider.objects.filter(ruc__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Provider.objects.filter(ruc__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'mobile':
                    if id == 0:
                        if Provider.objects.filter(mobile__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Provider.objects.filter(mobile__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'email':
                    if id == 0:
                        if Provider.objects.filter(email__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Provider.objects.filter(email__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load':
                data = [[i.id, i.name, i.ruc, i.mobile, i.email, i.address, True] for i in Provider.objects.filter()]
            else:
                data['resp'] = False
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
