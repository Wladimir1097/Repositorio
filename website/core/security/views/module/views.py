# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from config.settings.base import HOME
from core.security.decorators.module.decorators import access_module
from core.security.forms import Module,ModuleForm

@csrf_exempt
@access_module
def module(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'module/module_frm.html'
            if action == 'new':
                data['form'] = ModuleForm()
                data['title'] = 'Registro de Módulo'
                data['button'] = 'Guardar Módulo'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Module.objects.filter(pk=id).exists():
                    model = Module.objects.get(pk=id)
                    data['form'] = ModuleForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de Módulo'
                    data['button'] = 'Editar Módulo'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Module.objects.all().order_by('name')
            data['title'] = 'Listado de Módulos'
            data['button'] = 'Nuevo Módulo'
            template = 'module/module_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = ModuleForm(request.POST, request.FILES)
                elif action == 'edit':
                    f = ModuleForm(request.POST, request.FILES, instance=Module.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Module.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj'].strip()
                if type == 'url':
                    if id == 0:
                        if Module.objects.filter(url__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Module.objects.filter(url__iexact=obj).exclude(pk=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load':
                data = [[i.id,i.name,i.get_image(),i.get_type(),i.url,i.get_icon(),i.is_vertical,i.is_visible,i.is_active,i.is_active] for i in Module.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)


def get_module_options(request):
    try:
        from core.users.views.users.views import get_group_id_session
        id = get_group_id_session(request)
        module = Module.objects.filter(groupmodule__groups_id__in=[id], is_active=True, url=request.path)
        if module.exists():
            module = module[0]
            data = {
                'model': module,
                'link': module.url,
                'edit': "{}{}".format(module.url, '?action=edit'),
                'delete': "{}{}".format(module.url, '?action=delete'),
                'crud': "{}{}".format(module.url, '?action=new')
            }
            return data
        else:
            return {}
    except:
        return {}