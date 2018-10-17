# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.company.forms import *

@csrf_exempt
@access_module
def bodega(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'bodega/bodega_frm.html'
            if action == 'new':
                data['form'] = BodegaForm()
                data['title'] = 'Nueva Bodega'
                data['button'] = 'Guardar Bodega'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if TypeExpense.objects.filter(pk=id).exists():
                    model = Bodega.objects.get(pk=id)
                    data['form'] = BodegaForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de una Bodega'
                    data['button'] = 'Editar Bodega'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Bodega.objects.all().order_by('id')
            data['title'] = 'Listado de Bodegas'
            data['button'] = 'Nueva Bodega'
            template = 'bodega/bodegabd.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = BodegaForm(request.POST)
                elif action == 'edit':
                    f = BodegaForm(request.POST, instance=Bodega.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Bodega.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj']
                if type == 'name':
                    if id == 0:
                        if Bodega.objects.filter(name__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Bodega.objects.filter(name__iexact=obj).exclude(pk=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load':
                data = [[i.id, i.name,i.address, True] for i in Bodega.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
