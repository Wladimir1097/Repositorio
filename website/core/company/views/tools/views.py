# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.company.forms import *

@csrf_exempt
@access_module
def tools(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'tools/tools_frm.html'
            if action == 'new':
                data['form'] = ToolsForm()
                data['title'] = 'Nueva Herramienta'
                data['button'] = 'Guardar Herramienta'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Tools.objects.filter(pk=id).exists():
                    model = Tools.objects.get(pk=id)
                    data['form'] = ToolsForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de una Herramienta'
                    data['button'] = 'Editar Herramienta'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Tools.objects.all().order_by('id')
            data['title'] = 'Listado de Herramientas'
            data['button'] = 'Nueva Herramienta'
            template = 'tools/tools_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = ToolsForm(request.POST)
                elif action == 'edit':
                    f = ToolsForm(request.POST, instance=Tools.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    form = f.save(commit=False)
                    form.dep = (form.cost / form.guarantee) / 365
                    form.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Tools.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj']
                if type == 'code':
                    if id == 0:
                        if Tools.objects.filter(code__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Tools.objects.filter(code__iexact=obj).exclude(pk=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load':
                data = [[i.id, i.name, i.code, i.cost_format(), i.guarantee, i.dep_format(), True] for i in Tools.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
