# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.ingress.forms import *

@csrf_exempt
@access_module
def category(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'category/category_frm.html'
            if action == 'new':
                data['form'] = CategoryForm()
                data['title'] = 'Nueva Categoria de Producto'
                data['button'] = 'Guardar Categoria'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Category.objects.filter(pk=id).exists():
                    model = Category.objects.get(pk=id)
                    data['form'] = CategoryForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de una Categoria de Producto'
                    data['button'] = 'Editar Categoria'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Category.objects.all().order_by('name')
            data['title'] = 'Listado de Categorias de Productos'
            data['button'] = 'Nueva Categoria'
            template = 'category/category_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = CategoryForm(request.POST)
                elif action == 'edit':
                    f = CategoryForm(request.POST, instance=Category.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Category.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj'].strip()
                if type == 'name':
                    if id == 0:
                        if Category.objects.filter(name__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Category.objects.filter(name__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load':
                data = [[i.id, i.name,i.description, True] for i in Category.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
