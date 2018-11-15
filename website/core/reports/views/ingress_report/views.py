# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
from django.shortcuts import render
from core.reports.forms import ReportForm
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.ingress.models import *


@access_module
@csrf_exempt
def ingress_report(request):
    data = get_module_options(request)
    if request.method == 'GET':
        data['title'] = 'Reporte de Ingresos'
        data['form'] = ReportForm(request.user.bodega_id)
        return render(request, 'ingress_report/ingress_report_rp.html', data)
    elif request.method == 'POST':
        filtro = request.POST['filter']
        month = request.POST['month']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        year = request.POST['year']
        provs = request.POST['provs']
        prod = request.POST.getlist("prod[]")
        data = []
        if month == "" and filtro == '3':
            filtro = '2'
        try:
            items = Product.objects.filter(bodega=request.user.bodega_id)
            # items = Ingress.objects.filter(usuario_id__bodega_id=request.user.bodega_id)
            if len(prod):
                for y in prod:
                    items = Product.objects.filter(bodega=request.user.bodega_id)
                    items = items.filter(id=y)
                    if filtro == '1':
                        for i in items:
                            inv = Inventory.objects.filter(prod__id=i.id,
                                                           ing__date_joined__range=[start_date, end_date])
                            if len(provs):
                                inv = inv.filter(ing__prov_id=provs)
                            cantidad = 0
                            total = 0
                            material = ""
                            for x in inv:
                                cantidad += int(x.cant - x.diferencia)
                                total += float(x.subtotal_format())
                                material = x.prod.name
                                data.append(
                                    [x.id, x.ing.prov.name, x.prod.name, x.ing.date_joined_format(),
                                     x.cant - x.diferencia,
                                     x.subtotal_format(),
                                     i.get_sales()])
                            if len(inv) > 1:
                                data.append(
                                    ['-------', '-------', material, '-------', cantidad, format(total, '.2f')])

                    elif filtro == '2':
                        for i in items:
                            inv = Inventory.objects.filter(prod__id=i.id, ing__date_joined__year=year)
                            if len(provs):
                                inv = inv.filter(ing__prov_id=provs)
                            cantidad = 0
                            total = 0
                            material = ""
                            for x in inv:
                                cantidad += int(x.cant - x.diferencia)
                                total += float(x.subtotal_format())
                                material = x.prod.name
                                data.append(
                                    [x.id, x.ing.prov.name, x.prod.name, x.ing.date_joined_format(),
                                     x.cant - x.diferencia,
                                     x.subtotal_format(),
                                     i.get_sales()])
                            if len(inv) > 1:
                                data.append(
                                    ['-------', '-------', material, '-------', cantidad, format(total, '.2f')])

                    elif filtro == '3':
                        for i in items:
                            inv = Inventory.objects.filter(prod__id=i.id, ing__date_joined__year=year,
                                                           ing__date_joined__month=month)
                            if len(provs):
                                inv = inv.filter(ing__prov_id=provs)
                            cantidad = 0
                            total = 0
                            material = ""
                            for x in inv:
                                cantidad += int(x.cant - x.diferencia)
                                total += float(x.subtotal_format())
                                material = x.prod.name
                                data.append(
                                    [x.id, x.ing.prov.name, x.prod.name, x.ing.date_joined_format(),
                                     x.cant - x.diferencia,
                                     x.subtotal_format(),
                                     i.get_sales()])
                            if len(inv) > 1:
                                data.append(
                                    ['-------', '-------', material, '-------', cantidad, format(total, '.2f')])

                    else:
                        for i in items:
                            inv = Inventory.objects.filter(prod__id=i.id)
                            if len(provs):
                                inv = inv.filter(ing__prov_id=provs)
                            cantidad = 0
                            total = 0
                            material = ""
                            for x in inv:
                                cantidad += int(x.cant - x.diferencia)
                                total += float(x.subtotal_format())
                                material = x.prod.name
                                data.append(
                                    [x.id, x.ing.prov.name, x.prod.name, x.ing.date_joined_format(),
                                     x.cant - x.diferencia,
                                     x.subtotal_format(),
                                     i.get_sales()])
                            if len(inv) > 1:
                                data.append(
                                    ['-------', '-------', material, '-------', cantidad, format(total, '.2f')])



            else:
                if filtro == '1':
                    for i in items:
                        inv = Inventory.objects.filter(prod__id=i.id, ing__date_joined__range=[start_date, end_date])
                        if len(provs):
                            inv = inv.filter(ing__prov_id=provs)
                        cantidad = 0
                        total = 0
                        material = ""
                        for x in inv:
                            cantidad += int(x.cant - x.diferencia)
                            total += float(x.subtotal_format())
                            material = x.prod.name
                            data.append(
                                [x.id, x.ing.prov.name, x.prod.name, x.ing.date_joined_format(), x.cant - x.diferencia,
                                 x.subtotal_format(),
                                 i.get_sales()])
                        if len(inv) > 1:
                            data.append(
                                ['-------', '-------', material, '-------', cantidad, format(total, '.2f')])

                elif filtro == '2':
                    for i in items:
                        inv = Inventory.objects.filter(prod__id=i.id, ing__date_joined__year=year)
                        if len(provs):
                            inv = inv.filter(ing__prov_id=provs)
                        cantidad = 0
                        total = 0
                        material = ""
                        for x in inv:
                            cantidad += int(x.cant - x.diferencia)
                            total += float(x.subtotal_format())
                            material = x.prod.name
                            data.append(
                                [x.id, x.ing.prov.name, x.prod.name, x.ing.date_joined_format(), x.cant - x.diferencia,
                                 x.subtotal_format(),
                                 i.get_sales()])
                        if len(inv) > 1:
                            data.append(
                                ['-------', '-------', material, '-------', cantidad, format(total, '.2f')])

                elif filtro == '3':
                    for i in items:
                        inv = Inventory.objects.filter(prod__id=i.id, ing__date_joined__year=year,
                                                       ing__date_joined__month=month)
                        if len(provs):
                            inv = inv.filter(ing__prov_id=provs)
                        cantidad = 0
                        total = 0
                        material = ""
                        for x in inv:
                            cantidad += int(x.cant - x.diferencia)
                            total += float(x.subtotal_format())
                            material = x.prod.name
                            data.append(
                                [x.id, x.ing.prov.name, x.prod.name, x.ing.date_joined_format(), x.cant - x.diferencia,
                                 x.subtotal_format(),
                                 i.get_sales()])
                        if len(inv) > 1:
                            data.append(
                                ['-------', '-------', material, '-------', cantidad, format(total, '.2f')])

                else:
                    for i in items:
                        inv = Inventory.objects.filter(prod__id=i.id)
                        if len(provs):
                            inv = inv.filter(ing__prov_id=provs)
                        cantidad = 0
                        total = 0
                        material = ""
                        for x in inv:
                            cantidad += int(x.cant - x.diferencia)
                            total += float(x.subtotal_format())
                            material = x.prod.name
                            data.append(
                                [x.id, x.ing.prov.name, x.prod.name, x.ing.date_joined_format(), x.cant - x.diferencia,
                                 x.subtotal_format(),
                                 i.get_sales()])
                        if len(inv) > 1:
                            data.append(
                                ['-------', '-------', material, '-------', cantidad, format(total, '.2f')])

            '''
            if len(provs):
                items = items.filter(prov_id=provs)
            if filter == '1':
                items = items.filter(date_joined__range=[start_date, end_date])
            elif filter == '2':
                items = items.filter(date_joined__year=year)
            elif filter == '3':
                items = items.filter(date_joined__year=year, date_joined__month=month)



            subtotal = items.aggregate(resp=Coalesce(Sum('subtotal'), 0.00))['resp']
            dscto = items.aggregate(resp=Coalesce(Sum('dscto'), 0.00))['resp']
            iva = items.aggregate(resp=Coalesce(Sum('iva'), 0.00))['resp']
            total = items.aggregate(resp=Coalesce(Sum('total'), 0.00))['resp']
            data = [[i.id, i.prov.name, '-----------', i.date_joined_format(), i.subtotal_format(), i.total_format()]
                    for i in items]
            data.append(['-------', '-------', '-------', '-------', format(subtotal, '.2f'), format(total, '.2f')])
            '''
        except Exception as e:
            data = {}
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
