from builtins import range

from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
import json
from django.shortcuts import render
from django.template.defaultfilters import safe

from core.ingress.models import Product
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.sales.forms import *
from core.company.models import Company
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
import os
from config.settings.base import MEDIA_URL, MEDIA_ROOT
from decimal import Decimal


@csrf_exempt
@access_module
def medidores(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'medidores/med_frm.html'
            if action == 'new':
                data['form'] = MedidorForm(request.user.bodega_id)
                data['title'] = 'Nuevo Registro de Medidores'
                data['button'] = 'Guardar Registro'
                data['fecha'] = datetime.now().strftime('%Y-%m-%d')
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                data['id'] = id
                if GestionMedidor.objects.filter(pk=id).exists():
                    model = GestionMedidor.objects.get(pk=id)
                    data['form'] = MedidorForm(request.user.bodega_id, instance=model,
                                               initial={'id': model.id})
                    data['title'] = 'Edicion Registro de Medidores'
                    data['button'] = 'Editar Registro'
            else:
                return HttpResponseRedirect(HOME)
        else:
            data['items'] = GestionMedidor.objects.all().order_by('id')
            data['title'] = 'Listado en Registro de Medidores'
            data['button'] = 'Nuevo Registro'
            template = 'medidores/med_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'delete':
                GestionMedidor.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'deletemed':
                InventoryMedidor.objects.filter(gestion_id__exact=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'deletesell':
                InventorySello.objects.filter(gestion_id__exact=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'details':
                data = []
                type = request.POST['type']
                if type == 'medidor':
                    for index, s in enumerate(InventoryMedidor.objects.filter(gestion_id=request.POST['id'])):
                        data.append([index + 1, s.numeracion, s.medtype.name, s.distribuido])
                if type == 'sello':
                    for index, s in enumerate(InventorySello.objects.filter(gestion_id=request.POST['id'])):
                        data.append(
                            [index + 1, s.numeracion, s.distribuido])
            elif action == 'edit':
                with transaction.atomic():
                    items = json.loads(request.POST['items'])
                    ges = GestionMedidor.objects.get(pk=request.POST['pk'])

                    for p in items['medidores']:
                        if int(p['ban']) == 1:
                            num1 = int(p['num1'])
                            num2 = (int(p['num2']) + 1)
                            for num in range(num1, num2):
                                if InventoryMedidor.objects.filter(numeracion__exact=num).exists():
                                    InventoryMedidor.objects.filter(numeracion__exact=num).update(
                                        cli_id=None, medtype_id=int(p['tipo']), sales_id=None,
                                        distribuido=bool(p['bod']), date_joined=ges.date_joined,
                                        estado=False)
                                else:
                                    det = InventoryMedidor()
                                    det.gestion = ges
                                    det.usuario_id = request.user.id
                                    det.medtype_id = int(p['tipo'])
                                    det.date_joined = ges.date_joined
                                    det.numeracion = num
                                    if bool(p['bod']):
                                        det.distribuido = bool(p['bod'])
                                    det.save()
                        else:
                            if InventoryMedidor.objects.filter(numeracion__exact=int(p['num1'])).exists():
                                InventoryMedidor.objects.filter(numeracion__exact=int(p['num1'])).update(
                                    cli_id=None, medtype_id=int(p['tipo']), date_joined=ges.date_joined, sales_id=None,
                                    distribuido=bool(p['bod']),
                                    estado=False)
                            else:
                                det = InventoryMedidor()
                                det.gestion = ges
                                det.usuario_id = request.user.id
                                det.medtype_id = int(p['tipo'])
                                det.date_joined = ges.date_joined
                                det.numeracion = int(p['num1'])
                                if bool(p['bod']):
                                    det.distribuido = bool(p['bod'])
                                det.save()

                    for p in items['sellos']:
                        if int(p['ban']) == 1:
                            num1 = int(p['num1'])
                            num2 = (int(p['num2']) + 1)
                            print(num1, num2)
                            for num in range(num1, num2):
                                if InventorySello.objects.filter(numeracion__exact=num).exists():
                                    InventorySello.objects.filter(numeracion__exact=num).update(
                                        cli_id=None, date_joined=ges.date_joined, sales_id=None,
                                        distribuido=bool(p['bod']), estado=False)
                                else:
                                    det = InventorySello()
                                    det.gestion = ges
                                    det.usuario_id = request.user.id
                                    det.date_joined = ges.date_joined
                                    det.numeracion = num
                                    if bool(p['bod']):
                                        det.distribuido = bool(p['bod'])
                                    det.save()
                        else:
                            if InventorySello.objects.filter(numeracion__exact=int(p['num1'])).exists():
                                InventorySello.objects.filter(numeracion__exact=int(p['num1'])).update(
                                    cli_id=None, date_joined=ges.date_joined, sales_id=None, distribuido=bool(p['bod']),
                                    estado=False)
                            else:
                                det = InventorySello()
                                det.gestion = ges
                                det.usuario_id = request.user.id
                                det.date_joined = ges.date_joined
                                det.numeracion = int(p['num1'])
                                if bool(p['bod']):
                                    det.distribuido = bool(p['bod'])
                                det.save()
                    data['resp'] = True

            elif action == 'new':
                with transaction.atomic():

                    cantmed = 0
                    cantsell = 0
                    items = json.loads(request.POST['items'])
                    ges = GestionMedidor()
                    ges.usuario_id = request.user.id
                    ges.date_joined = items['date_joined']
                    ges.save()

                    for p in items['medidores']:
                        if int(p['ban']) == 1:
                            num1 = int(p['num1'])
                            num2 = (int(p['num2']) + 1)
                            for num in range(num1, num2):
                                if InventoryMedidor.objects.filter(numeracion__exact=num).exists():
                                    InventoryMedidor.objects.filter(numeracion__exact=num).update(
                                        cli_id=None, medtype_id=int(p['tipo']), sales_id=None,
                                        distribuido=bool(p['bod']), date_joined=ges.date_joined,
                                        estado=False)
                                    cantmed += 1
                                else:
                                    det = InventoryMedidor()
                                    det.gestion = ges
                                    det.usuario_id = request.user.id
                                    det.medtype_id = int(p['tipo'])
                                    det.date_joined = ges.date_joined
                                    det.numeracion = num
                                    cantmed += 1
                                    if bool(p['bod']):
                                        det.distribuido = bool(p['bod'])
                                    det.save()
                        else:
                            if InventoryMedidor.objects.filter(numeracion__exact=int(p['num1'])).exists():
                                InventoryMedidor.objects.filter(numeracion__exact=int(p['num1'])).update(
                                    cli_id=None, medtype_id=int(p['tipo']), date_joined=ges.date_joined, sales_id=None,
                                    distribuido=bool(p['bod']),
                                    estado=False)
                                cantmed += 1
                            else:
                                det = InventoryMedidor()
                                det.gestion = ges
                                det.usuario_id = request.user.id
                                det.medtype_id = int(p['tipo'])
                                det.date_joined = ges.date_joined
                                det.numeracion = int(p['num1'])
                                cantmed += 1
                                if bool(p['bod']):
                                    det.distribuido = bool(p['bod'])
                                det.save()

                    for p in items['sellos']:
                        if int(p['ban']) == 1:
                            num1 = int(p['num1'])
                            num2 = (int(p['num2']) + 1)
                            print(num1, num2)
                            for num in range(num1, num2):
                                if InventorySello.objects.filter(numeracion__exact=num).exists():
                                    InventorySello.objects.filter(numeracion__exact=num).update(
                                        cli_id=None, date_joined=ges.date_joined, sales_id=None,
                                        distribuido=bool(p['bod']), estado=False)
                                    cantsell += 1
                                else:
                                    det = InventorySello()
                                    det.gestion = ges
                                    det.usuario_id = request.user.id
                                    det.date_joined = ges.date_joined
                                    det.numeracion = num
                                    cantsell += 1
                                    if bool(p['bod']):
                                        det.distribuido = bool(p['bod'])
                                    det.save()
                        else:
                            if InventorySello.objects.filter(numeracion__exact=int(p['num1'])).exists():
                                InventorySello.objects.filter(numeracion__exact=int(p['num1'])).update(
                                    cli_id=None, date_joined=ges.date_joined, sales_id=None, distribuido=bool(p['bod']),
                                    estado=False)
                                cantsell += 1
                            else:
                                det = InventorySello()
                                det.gestion = ges
                                det.usuario_id = request.user.id
                                det.date_joined = ges.date_joined
                                det.numeracion = int(p['num1'])
                                cantsell += 1
                                if bool(p['bod']):
                                    det.distribuido = bool(p['bod'])
                                det.save()
                    ges.cantsell = cantsell
                    ges.cantmed = cantmed
                    ges.save()
                    data['resp'] = True
            elif action == 'load':

                data = [[i.id, i.date_joined_format(), i.cantmed, i.cantsell,
                         [[e.username] for e in User.objects.filter(pk=i.usuario_id)], ] for i in
                        GestionMedidor.objects.filter(usuario_id__bodega_id=request.user.bodega_id)]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            print(e)
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
