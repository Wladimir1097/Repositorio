from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.ingress.forms import *


@csrf_exempt
@access_module
def document(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'document/document_fr.html'
            if action == 'new':
                data['form'] = DocumentForm()
                data['title'] = 'Nuevo Documento'
                data['button'] = 'Guardar Documento'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if Document.objects.filter(pk=id).exists():
                    model = Document.objects.get(pk=id)
                    data['form'] = DocumentForm(instance=model, initial={'id': model.id})
                    data['title'] = 'Edición de un Documento'
                    data['button'] = 'Editar Documento'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = Document.objects.all().order_by('description')
            data['title'] = 'Listado de Documentos'
            data['button'] = 'Nuevo Documento'
            template = 'document/document_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = DocumentForm(request.POST, request.FILES)
                elif action == 'edit':
                    f = DocumentForm(request.POST, request.FILES, instance=Document.objects.get(pk=request.POST['id']))
                if f.is_valid():
                    p = f.save()
                    p.bodega_id = request.user.bodega_id
                    p.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                Document.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'load':
                data = [[i.id, i.date_joined_format(), i.get_image(), i.description, True] for i in
                        Document.objects.filter(bodega_id=request.user.bodega_id)]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)
