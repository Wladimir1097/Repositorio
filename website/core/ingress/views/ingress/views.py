# -*- coding: utf-8 -*-

from django.db import transaction
from django.http import HttpResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.ingress.forms import *
from core.users.models import *

from core.company.models import Company
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
import os
from config.settings.base import MEDIA_URL, MEDIA_ROOT


@csrf_exempt
@access_module
def ingress(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'ingress/ingress_frm.html'
            if action == 'new':
                data['form'] = IngressForm()
                data['frmProv'] = ProviderForm()
                data['title'] = 'Nuevo Registro de una Compra'
                data['button'] = 'Guardar Compra'
            elif action == 'pdf' and 'id' in request.GET:
                id = request.GET['id']
                if Ingress.objects.filter(id=id):
                    template = get_template('ingress/ingress_bill.html')
                    data['company'] = Company.objects.first()
                    data['Ingress'] = Ingress.objects.filter(id=id)
                    data['details'] = Inventory.objects.filter(ing_id=id).order_by('id')
                    html = template.render(data)
                    result = BytesIO()
                    links = lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
                    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='UTF-8',
                                            link_callback=links)
                    return HttpResponse(result.getvalue(), content_type='application/pdf')
                return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(HOME)
        else:
            data['items'] = Ingress.objects.all().order_by('id')
            data['title'] = 'Listado de Compras'
            data['button'] = 'Nueva Compra'
            template = 'ingress/ingress_dt.html'
        return render(request, template, data)

    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'get_provider':
                id = request.POST['id']
                data = {
                    'ruc': '', 'phone': '', 'email': '', 'name': '', 'address': ''
                }
                if not id == "" or not id is None:
                    items = Provider.objects.filter(id=id)
                    if items.exists():
                        data = items[0].toJSON()
            elif action == 'delete':
                ing = Ingress.objects.get(pk=request.POST['id'])
                for i in Inventory.objects.filter(ing=ing):
                    i.prod.stock -= i.cant
                    i.prod.save()
                    i.delete()
                ing.delete()
                data['resp'] = True
            elif action == 'search_products':
                prods = json.loads(request.POST['prods'])
                data = [[p.id, p.name, p.get_image(), p.get_cat(), p.cost_format(), p.stock, True] for p in
                        Product.objects.filter().exclude(id__in=prods)]
            elif action == 'new':
                with transaction.atomic():
                    items = json.loads(request.POST['items'])
                    ing = Ingress()
                    ing.usuario_id = request.user.id
                    ing.prov_id = items['prov']
                    ing.date_joined = items['date_joined']
                    ing.iva = items['iva']
                    ing.save()
                    for p in items['products']:
                        det = Inventory()
                        det.ing = ing
                        det.prod_id = p['id']
                        det.cant = int(p['cant'])
                        det.price = float(p['cost'])
                        det.subtotal = float(det.price) * int(det.cant)
                        det.save()
                        det.prod.cost=det.prod.price
                        det.prod.price=det.price
                        det.prod.stock += det.cant
                        det.prod.save()
                    ing.get_totals()
                    data['resp'] = True
            elif action == 'details':
                data = [[a.id, a.prod.name, a.price_format(), a.cant, a.subtotal_format()] for a in
                        Inventory.objects.filter(ing_id=request.POST['id'])]
            elif action == 'load':
                data = [
                    [i.id, [[e.first_name +' '+ e.last_name] for e in User.objects.filter(pk=i.usuario_id)], i.prov.name,
                     i.prov.ruc,
                     i.date_joined_format(), i.subtotal_format(), i.iva_format(), i.total_format()] for i in
                    Ingress.objects.filter()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
