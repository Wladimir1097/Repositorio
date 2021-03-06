# -*- coding: utf-8 -*-
from pydoc import cli

from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
import json
from django.shortcuts import render
from django.template.defaultfilters import safe
from django.utils.timezone import now

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
def sales(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'sales/sales_frm.html'
            if action == 'new':
                data['form'] = SalesForm(request.user.bodega_id, request.POST)
                data['title'] = 'Nuevo Registro de Despacho'
                data['button'] = 'Guardar Transacción'
            elif action == 'delete':
                if InventoryMedidor.objects.filter(numeracion__exact=request.GET['num']).exists():
                    InventoryMedidor.objects.filter(numeracion__exact=request.GET['num']).update(
                        cli_id=None, sales_id=None, estado=False)
                if InventorySello.objects.filter(numeracion__exact=request.GET['num']).exists():
                    InventorySello.objects.filter(numeracion__exact=request.GET['num']).update(
                        cli_id=None, sales_id=None, estado=False)
                return HttpResponseRedirect(src)
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                data['id'] = id
                if Sales.objects.filter(pk=id).exists():
                    model = Sales.objects.get(pk=id)
                    data['form'] = SalesForm(request.user.bodega_id, instance=model,
                                             initial={'id': model.id})
                    data['details'] = SalesProducts.objects.filter(sales=id)
                    data['servicios'] = SalesServices.objects.filter(sales=id)
                    data['title'] = 'Edición de Egreso'
                    data['button'] = 'Editar Orden'
                    # return render(request, 'ingress/editarIngreso.html', data)
                else:
                    return HttpResponseRedirect(src)
            elif action == 'reuse' and 'id' in request.GET:
                id = request.GET['id']
                data['id'] = id
                if Sales.objects.filter(pk=id).exists():
                    model = Sales.objects.get(pk=id)
                    data['form'] = SalesForm(request.user.bodega_id, instance=model, initial={'id': model.id})
                    data['details'] = SalesProducts.objects.filter(sales=id)
                    data['servicios'] = SalesServices.objects.filter(sales=id)
                    data['title'] = 'Reutilizar este Egreso'
                    data['button'] = 'Registrar Orden'
                    # return render(request, 'ingress/editarIngreso.html', data)
                else:
                    return HttpResponseRedirect(src)
            elif action == 'pdf' and 'id' in request.GET:
                id = request.GET['id']
                for e in Bodega.objects.filter(pk=request.user.bodega_id):
                    direccion = e.address
                if Sales.objects.filter(id=id):
                    template = get_template('sales/sales_bill.html')
                    cliente = 0
                    for e in Sales.objects.filter(id=id):
                        cliente = e.cli_id
                    context = {
                        'company': Company.objects.first(), 'sales': Sales.objects.get(id=id),
                        'details': SalesProducts.objects.filter(sales_id=id).order_by('id'),
                        'ubicacion': direccion,
                        'medidorf': [e.numeracion for e in
                                     InventoryMedidor.objects.filter(sales_id=id, cli_id=cliente).order_by('id')[:1]],
                        'medidorl': [e.numeracion for e in
                                     InventoryMedidor.objects.filter(sales_id=id, cli_id=cliente).order_by('-id')[:1]],
                        'sellof': [e.numeracion for e in
                                   InventorySello.objects.filter(sales_id=id, cli_id=cliente).order_by('id')[:1]],
                        'sellol': [e.numeracion for e in
                                   InventorySello.objects.filter(sales_id=id, cli_id=cliente).order_by('-id')[:1]],
                        'vacio': request.user.bodega_id,
                        'medidor': InventoryMedidor.objects.filter(sales_id=id, cli_id=cliente).order_by('numeracion'),
                        'sello': InventorySello.objects.filter(sales_id=id, cli_id=cliente).order_by('numeracion'),
                        'contador': 12
                    }
                    html = template.render(context)
                    result = BytesIO()
                    links = lambda uri, rel: os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ''))
                    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8',
                                            link_callback=links)
                    return HttpResponse(result.getvalue(), content_type='application/pdf')
                return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(HOME)
        else:
            data['items'] = Sales.objects.all().order_by('id')
            data['title'] = 'Listado de Despachos de Materiales'
            data['button'] = 'Nueva Despacho'
            template = 'sales/sales_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'get_client':
                id = request.POST['id']
                data = {
                    'dni': '', 'phone': '', 'email': ''
                }
                if not id == "" and not id is None:
                    items = Client.objects.filter(id=id)
                    if items.exists():
                        items = items[0]
                        data = {
                            'dni': items.ruc, 'phone': items.mobile, 'email': items.email,
                            'address': items.address
                        }
            elif action == 'delete':
                sales = Sales.objects.get(pk=request.POST['id'])
                if InventoryMedidor.objects.filter(cli_id=sales.cli, sales_id=request.POST['id']).exists():
                    InventoryMedidor.objects.filter(cli_id=sales.cli.id, sales_id=request.POST['id']).update(
                        cli_id=None, sales_id=None, estado=False)
                if InventorySello.objects.filter(cli_id=sales.cli, sales_id=request.POST['id']).exists():
                    InventorySello.objects.filter(cli_id=sales.cli.id, sales_id=request.POST['id']).update(
                        cli_id=None, sales_id=None, estado=False)
                for d in SalesProducts.objects.filter(sales=sales):
                    if d.sales.type == 2:
                        d.prod.stock += d.cant_ent
                    else:
                        d.prod.stock += d.cant
                    d.prod.save()
                    d.delete()
                sales.delete()
                data['resp'] = True
            elif action == 'details':
                data = []
                type = request.POST['type']
                if type == 'products':
                    for s in SalesProducts.objects.filter(sales_id=request.POST['id']):
                        data.append([s.id, s.prod.name, s.price_format(), s.cant, s.subtotal_format(), s.is_dispatched])
                elif type == 'services':
                    for s in SalesServices.objects.filter(sales_id=request.POST['id']):
                        data.append([s.id, s.serv.name, s.total_format()])
                elif type == 'medidor':
                    cliente = 0
                    for e in Sales.objects.filter(id=request.POST['id']):
                        cliente = e.cli_id
                    for s in InventoryMedidor.objects.filter(sales_id=request.POST['id'], cli_id=cliente):
                        data.append([s.id, s.numeracion, True])
                elif type == 'sello':
                    cliente = 0
                    for e in Sales.objects.filter(id=request.POST['id']):
                        cliente = e.cli_id
                    for s in InventorySello.objects.filter(sales_id=request.POST['id'], cli_id=cliente):
                        data.append([s.id, s.numeracion, True])
                elif type == 'adicion':
                    for s in InventoryMedidor.objects.filter(usuario_id__bodega_id=request.user.bodega_id):
                        if s.distribuido:
                            if not s.estado:
                                data.append({
                                    'pk': request.POST['id'], 'id': s.id, 'tipo': True, 'num': s.numeracion,
                                    'state': s.estado
                                })
                    for s in InventorySello.objects.filter(usuario_id__bodega_id=request.user.bodega_id):
                        if s.distribuido:
                            if not s.estado:
                                data.append({
                                    'pk': request.POST['id'], 'id': s.id, 'tipo': False, 'num': s.numeracion,
                                    'state': s.estado
                                })
                elif type == 'dispatch':
                    for s in SalesProducts.objects.filter(sales_id=request.POST['id']):
                        data.append({
                            'id': s.id, 'name': s.prod.name, 'cant': s.cant, 'cant_ent': s.cant_ent,
                            'stock': s.prod.stock, 'cant_dis': 1, 'state': s.is_dispatched
                        })
                elif type == 'devolution':
                    for s in SalesProducts.objects.filter(sales_id=request.POST['id']):
                        data.append({
                            'id': s.id, 'name': s.prod.name, 'cant': s.cant, 'cant_dev': 1, 'state': s.cant == 0
                        })
            elif action == 'search_products':
                data = []
                for p in Product.objects.filter(bodega_id=request.user.bodega_id).exclude(
                        id__in=json.loads(request.POST['items'])):
                    if p.stock > 0:
                        data.append([p.id, p.name, p.stock, p.price_format(), 1])
            elif action == 'search_services':
                data = [[i.id, i.name, i.cost_format(), True] for i in
                        Services.objects.filter().exclude(id__in=json.loads(request.POST['items']))]
            elif action == 'new' or action == 'edit' or action == 'reuse':
                with transaction.atomic():
                    if action == 'edit':
                        sal = Sales.objects.get(pk=request.POST['pk'])
                        for d in SalesProducts.objects.filter(sales=sal):
                            d.prod.stock += d.cant
                            d.prod.save()
                            d.delete()
                        vent = sal

                    items = json.loads(request.POST['items'])
                    if action != 'edit':
                        vent = Sales()
                        vent.cli_id = items['cli']
                    vent.usuario_id = request.user.id
                    vent.date_joined = items['date_joined']
                    vent.date_delivery = items['date_delivery']
                    vent.subtotal = items['subtotal']
                    vent.dscto = items['dscto']
                    vent.iva = items['iva']
                    vent.subtotal = float(items['total'])
                    vent.type = int(items['type'])
                    vent.save()
                    for p in items['products']:
                        det = SalesProducts()
                        det.sales = vent
                        det.prod_id = int(p['id'])
                        det.cant = int(p['cant'])
                        det.price = float(p['cost'])
                        det.subtotal = float(det.price) * int(det.cant)
                        det.is_dispatched = vent.type == 1
                        det.save()

                        if vent.type == 1:
                            prod = Product.objects.get(pk=int(p['id']))
                            prod.stock -= det.cant
                            prod.save()

                    for s in items['services']:
                        serv = SalesServices()
                        serv.sales = vent
                        serv.serv_id = s['id']
                        serv.total = float(s['cost'])
                        serv.save()

                    vent.get_totals()
                    data['resp'] = True

            elif action == 'dispatch_products':
                items = json.loads(request.POST['items'])
                for i in items:
                    if i['state']:
                        det = SalesProducts.objects.get(pk=i['id'])
                        det.cant_ent += int(i['cant_dis'])
                        det.is_dispatched = det.cant_ent == det.cant
                        det.subtotal = float(det.price) * int(det.cant_ent)
                        det.save()
                        sales = Sales.objects.get(pk=det.sales.pk)
                        sales.subtotal += Decimal(det.subtotal)
                        sales.save()
                        prod = Product.objects.get(pk=det.prod_id)
                        prod.stock -= int(i['cant_dis'])
                        prod.save()

                data['resp'] = True
            elif action == 'devolution_products':
                items = json.loads(request.POST['items'])
                for i in items:
                    cant_dev = int(i['cant'])
                    if i['state'] and cant_dev > 0:
                        cant = int(i['cant_dev'])
                        det = SalesProducts.objects.get(pk=i['id'])
                        det.cant -= cant
                        det.save()
                        det.sales.get_totals()
                        prod = Product.objects.get(pk=det.prod_id)
                        prod.stock += cant
                        prod.save()
                        dev = DevolutionSales()
                        dev.det = det
                        dev.cant = cant
                        dev.save()
                data['resp'] = True
            elif action == 'ingress_prod':
                items = json.loads(request.POST['items'])
                for i in items:
                    if i['state']:
                        cliente = 0
                        if i['tipo']:
                            det = InventoryMedidor.objects.get(pk=i['id'])
                            for e in Sales.objects.filter(id=i['pk']):
                                cliente = e.cli_id
                            det.cli_id = cliente
                            det.sales_id = i['pk']
                            det.estado = True
                            det.save()
                        else:
                            det = InventorySello.objects.get(pk=i['id'])
                            for e in Sales.objects.filter(id=i['pk']):
                                cliente = e.cli_id
                            det.cli_id = cliente
                            det.sales_id = i['pk']
                            det.estado = True
                            det.save()
                data['resp'] = True
            elif action == 'ingress_med':
                num1 = int(request.POST['num1'])
                num2 = int(request.POST['num2']) + 1
                items = json.loads(request.POST['items'])
                lista = []
                for i in items:
                    for clave, valor in i.items():
                        if clave == 'num':
                            lista.append(valor)
                for num in range(num1, num2):
                    if str(num) in lista:
                        for i in items:
                            cliente = 0
                            fecha = ""
                            if i['tipo']:
                                det = InventoryMedidor.objects.get(pk=i['id'])
                                if int(i['num']) == num:
                                    for e in Sales.objects.filter(id=i['pk']):
                                        cliente = e.cli_id
                                        fecha = e.date_joined
                                    det.cli_id = cliente
                                    det.date_joined = fecha
                                    det.sales_id = i['pk']
                                    det.estado = True
                                    det.save()
                                    break
                data['resp'] = True
            elif action == 'ingress_sell':
                num1 = int(request.POST['num1'])
                num2 = int(request.POST['num2']) + 1
                items = json.loads(request.POST['items'])
                lista = []
                for i in items:
                    for clave, valor in i.items():
                        if clave == 'num':
                            lista.append(valor)
                for num in range(num1, num2):
                    if str(num) in lista:
                        for i in items:
                            cliente = 0
                            fecha = ""
                            if not i['tipo']:
                                det = InventorySello.objects.get(pk=i['id'])
                                if int(i['num']) == num:
                                    for e in Sales.objects.filter(id=i['pk']):
                                        cliente = e.cli_id
                                        fecha = e.date_joined
                                    det.cli_id = cliente
                                    print(fecha)
                                    det.date_joined = fecha
                                    det.sales_id = i['pk']
                                    det.estado = True
                                    det.save()
                                    break
                data['resp'] = True
            elif action == 'load':

                data = [[i.id, i.get_nro(), [[e.username] for e in User.objects.filter(pk=i.usuario_id)], i.cli.name,
                         i.date_joined_format(), SalesProducts.objects.filter(sales=i).count(),
                         InventoryMedidor.objects.filter(sales=i).count(),
                         InventorySello.objects.filter(sales=i).count(),
                         i.subtotal_format(), i.type] for i in
                        Sales.objects.filter(usuario_id__bodega_id=request.user.bodega_id)]
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
