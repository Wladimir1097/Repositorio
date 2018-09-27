# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.forms import *
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *

@access_module
@csrf_exempt
def module_type(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'module_type/module_type_frm.html'
            if action == 'new':
                data['form'] = ModuleTypeForm()
                data['title'] = 'Registro de Tipo de Módulo'
                data['button'] = 'Guardar Tipo de Módulo'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if ModuleType.objects.filter(pk=id).exists():
                    model = ModuleType.objects.get(pk=id)
                    data['form'] = ModuleTypeForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de Tipo de Módulo'
                    data['button'] = 'Editar Tipo de Módulo'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = ModuleType.objects.all().order_by('name')
            data['title'] = 'Listado de Tipos de Módulos'
            data['button'] = 'Nuevo Tipo de Módulo'
            template = 'module_type/module_type_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = ModuleTypeForm(request.POST, request.FILES)
                elif action == 'edit':
                    f = ModuleTypeForm(request.POST, request.FILES,
                                       instance=ModuleType.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                ModuleType.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj']
                if type == 'name':
                    if id == 0:
                        if ModuleType.objects.filter(name__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if ModuleType.objects.filter(name__iexact=obj).exclude(pk=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'icon':
                    if id == 0:
                        if ModuleType.objects.filter(icon__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if ModuleType.objects.filter(icon__iexact=obj).exclude(pk=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load':
                data = [[i.id, i.name, i.icon, i.is_active] for i in ModuleType.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)


@csrf_exempt
def test(request):
    data = {
        'title': 'Mi pagina dashboard'
    }
    return render(request, 'bs_footer.html', data)
