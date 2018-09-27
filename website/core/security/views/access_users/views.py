# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from config.settings.base import HOME
from core.security.decorators.module.decorators import access_module
from core.security.forms import AccessUsers
from core.security.views.module.views import get_module_options

@csrf_exempt
@access_module
def access_users(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        data['items'] = AccessUsers.objects.all().order_by('id')
        data['title'] = 'Listado de Accesos al sistema'
        template = 'access_users/access_users_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'delete':
                AccessUsers.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'load':
                data = [[i.id,i.user.get_full_name(),i.date_joined_format(),i.hour_format(),i.localhost,i.hostname,True] for i in AccessUsers.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
