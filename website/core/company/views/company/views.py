# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.shortcuts import render
from config.settings.base import HOME
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import access_module
from core.company.forms import *

@csrf_exempt
@access_module
def company(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            template = 'company/company_frm.html'
            objs = Company.objects.filter()
            data['action'] = action
            if action == 'new':
                if not objs.exists():
                    data['form'] = CompanyForm()
                    data['title'] = 'Registro de la Empresa'
                    data['button'] = 'Guardar Información'
                else:
                    data['action'] = 'edit'
                    model = Company.objects.first()
                    data['obj'] = model
                    data['form'] = CompanyForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de la Empresa'
                    data['button'] = 'Editar Información'
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Company.objects.all().order_by('name')
            data['title'] = 'Información de la Empresa'
            data['button'] = 'Adjuntar Información'
            template = 'company/company_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        action = request.POST['action']
        data = {}
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = CompanyForm(request.POST, request.FILES)
                elif action == 'edit':
                    f = CompanyForm(request.POST, request.FILES, instance=Company.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    f.save()
                    #model = Company.objects.get(pk=1)
                    #model.generate_img_base64()
                    #model.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Company.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)


def get_company():
    objs = Company.objects.filter()
    if objs.exists():
        return objs[0]
    return None
