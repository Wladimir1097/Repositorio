# -*- coding: utf-8 -*-
import json
from django.core.files.base import File
from django.core.management import call_command
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from config.settings.base import HOME
from core.security.decorators.module.decorators import access_module
from core.security.forms import Database
from core.security.views.module.views import get_module_options

@csrf_exempt
@access_module
def database(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        data['items'] = Database.objects.all().order_by('id')
        data['title'] = 'Listado de Respaldos BD'
        data['button'] = 'Nuevo Respaldo'
        template = 'database/database_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new':
                file = open('database.txt', 'rb')
                output = open('database.txt', 'w')
                call_command('dumpdata', format='json', indent=3, stdout=output)
                output.close()
                Database(user_id=request.user.id,localhost=request.META['SERVER_PORT'],archive=File(file)).save()
                data['resp'] = True
            elif action == 'delete':
                Database.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'load':
                data = [[i.id,i.user.get_full_name(),i.localhost,i.hostname,i.date_joined_format(),i.hour_format(),i.get_archive(),True] for i in Database.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
