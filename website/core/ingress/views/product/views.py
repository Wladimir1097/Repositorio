# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.ingress.forms import *

@csrf_exempt
@access_module
def product(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'product/product_frm.html'
            if action == 'new':
                data['form'] = ProductForm()
                data['title'] = 'Nuevo Registro de un Producto'
                data['button'] = 'Guardar Producto'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Product.objects.filter(pk=id).exists():
                    model = Product.objects.get(pk=id)
                    data['form'] = ProductForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de un Producto'
                    data['button'] = 'Editar Producto'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Product.objects.all().order_by('name')
            data['title'] = 'Listado de Productos'
            data['button'] = 'Nuevo Producto'
            template = 'product/product_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = ProductForm(request.POST, request.FILES)
                elif action == 'edit':
                    f = ProductForm(request.POST, request.FILES , instance=Product.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    f.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Product.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = int(request.POST['id'])
                obj = request.POST['obj'].strip()
                if type == 'name':
                    if id == 0:
                        if Product.objects.filter(name__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if Product.objects.filter(name__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'load':
                data = [[i.id, i.name, i.get_image(), i.cat.name, i.brand.name,i.stock,i.cost_format(), i.price_format(), True] for i in Product.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
