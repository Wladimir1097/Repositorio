# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json
from django.shortcuts import render
from config.settings.base import HOME
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import access_module
from core.security.forms import Group,GroupForm,Module,GroupModule

@csrf_exempt
@access_module
def groups(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'groups/groups_frm.html'
            if action == 'new':
                data['form'] = GroupForm()
                data['title'] = 'Registro de un Perfil'
                data['button'] = 'Guardar Perfil'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Group.objects.filter(pk=id).exists():
                    model = Group.objects.get(pk=id)
                    modules = Module.objects.filter(groupmodule__groups__id=id)
                    data['form'] = GroupForm(instance=model,initial={'id': model.id, 'modules': modules})
                    data['title'] = 'Edición de un Perfil'
                    data['button'] = 'Editar Perfil'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Group.objects.all().order_by('name')
            data['title'] = 'Listado de Perfiles'
            data['button'] = 'Nuevo Perfil'
            template = 'groups/groups_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = GroupForm(request.POST)
                elif action == 'edit':
                    model = Group.objects.get(pk=request.POST['id'])
                    f = GroupForm(request.POST, instance=model)
                    GroupModule.objects.filter(groups=model).delete()
                if f.is_valid():
                    form = f.save(commit=False)
                    form.save()
                    for m in request.POST.getlist('modules'):
                        GroupModule(groups=form, modules_id=m).save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Group.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj']
                if type == 'name':
                    if id == 0:
                        if Group.objects.filter(name__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Group.objects.filter(name__iexact=obj).exclude(pk=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load_modules':
                data = [[m.name,m.get_icon(),m.get_image(),m.get_type(),m.is_vertical,m.is_visible,m.is_active] for m in Module.objects.filter(groupmodule__groups_id=request.POST['id'])]
            elif action == 'load':
                data = [[i.id,i.name,i.groupmodule_set.count(),True] for i in Group.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
