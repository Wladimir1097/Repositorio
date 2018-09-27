# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
import json
from django.shortcuts import render
from core.ingress.models import Product
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.sales.forms import *
from core.company.models import Company
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
import os
from config.settings.base import MEDIA_URL,MEDIA_ROOT

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
                data['form'] = SalesForm()
                data['title'] = 'Nuevo Registro de Venta y Pedidos'
                data['button'] = 'Guardar Transacción'
            elif action == 'pdf' and 'id' in request.GET:
                id = request.GET['id']
                if Sales.objects.filter(id=id):
                    template = get_template('sales/sales_bill.html')
                    context = {
                        'company': Company.objects.first(), 'sales': Sales.objects.get(id=id),
                        'details': SalesProducts.objects.filter(sales_id=id).order_by('id'),
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
            data['title'] = 'Listado de Ventas y Pedidos de Productos'
            data['button'] = 'Nueva Venta o Pedido'
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
                for d in SalesProducts.objects.filter(sales=sales):
                    d.prod.stock += d.cant
                    d.prod.save()
                    d.delete()
                sales.delete()
                data['resp'] = True
            elif action == 'details':
                data = []
                type =  request.POST['type']
                if type == 'products':
                    for s in SalesProducts.objects.filter(sales_id=request.POST['id']):
                        data.append([s.id, s.prod.name, s.price_format(), s.cant, s.subtotal_format(), s.is_dispatched])
                elif type == 'services':
                    for s in SalesServices.objects.filter(sales_id=request.POST['id']):
                        data.append([s.id, s.serv.name, s.total_format()])
                elif type == 'dispatch':
                    for s in SalesProducts.objects.filter(sales_id=request.POST['id']):
                        data.append({
                            'id':s.id, 'name':s.prod.name, 'cant':s.cant, 'cant_ent': s.cant_ent, 'stock':s.prod.stock, 'cant_dis': 1, 'state':s.is_dispatched
                        })
                elif type == 'devolution':
                    for s in SalesProducts.objects.filter(sales_id=request.POST['id']):
                        data.append({
                            'id':s.id, 'name':s.prod.name, 'cant':s.cant, 'cant_dev': 1, 'state': s.cant == 0
                        })
            elif action == 'search_products':
                data = []
                for p in Product.objects.filter().exclude(id__in=json.loads(request.POST['items'])):
                    if p.stock > 0:
                        data.append([p.id, p.name, p.stock, p.price_format(), 1])
            elif action == 'search_services':
                data = [[i.id, i.name, i.cost_format(), True] for i in Services.objects.filter().exclude(id__in=json.loads(request.POST['items']))]
            elif action == 'new':
                with transaction.atomic():
                    items = json.loads(request.POST['items'])
                    vent = Sales()
                    vent.cli_id = items['cli']
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
                        det.save()
                        prod = Product.objects.get(pk=det.prod_id)
                        prod.stock-=int(i['cant_dis'])
                        prod.save()
                data['resp'] = True
            elif action == 'devolution_products':
                items = json.loads(request.POST['items'])
                for i in items:
                    cant_dev = int(i['cant'])
                    if i['state'] and cant_dev > 0:
                        cant = int(i['cant_dev'])
                        det = SalesProducts.objects.get(pk=i['id'])
                        det.cant-=cant
                        det.save()
                        det.sales.get_totals()
                        prod = Product.objects.get(pk=det.prod_id)
                        prod.stock+=cant
                        prod.save()
                        dev = DevolutionSales()
                        dev.det = det
                        dev.cant = cant
                        dev.save()
                data['resp'] = True
            elif action == 'load':
                data = [[i.id, i.get_nro(), i.cli.name, i.date_joined_format(), i.get_type_display(), i.subtotal_format(), i.iva_format(), i.total_format(), i.type] for i in Sales.objects.filter()]
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

