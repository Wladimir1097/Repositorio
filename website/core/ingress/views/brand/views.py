# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.ingress.forms import *

@csrf_exempt
@access_module
def brand(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'brand/brand_frm.html'
            if action == 'new':
                data['form'] = BrandForm()
                data['title'] = 'Nueva Tipo de Producto'
                data['button'] = 'Guardar Tipo'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Brand.objects.filter(pk=id).exists():
                    model = Brand.objects.get(pk=id)
                    data['form'] = BrandForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de una Tipo de Producto'
                    data['button'] = 'Editar Tipo'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Brand.objects.all().order_by('name')
            data['title'] = 'Listado de Tipos de Productos'
            data['button'] = 'Nueva Tipo'
            template = 'brand/brand_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = BrandForm(request.POST)
                elif action == 'edit':
                    f = BrandForm(request.POST, instance=Brand.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    p = f.save()
                    p.bodega_id = request.user.bodega_id
                    p.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Brand.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj'].strip()
                if type == 'name':
                    if id == 0:
                        if Brand.objects.filter(name__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Brand.objects.filter(name__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load':
                data = [[i.id, i.name, True] for i in Brand.objects.filter(bodega_id=request.user.bodega_id)]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
