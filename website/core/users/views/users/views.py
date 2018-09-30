# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from core.security.models import AccessUsers
from core.users.forms import UserForm
from core.security.views.module.views import get_module_options
from core.security.decorators.module.decorators import *
from core.users.models import User
from django.contrib.auth.models import Group

@csrf_exempt
@access_module
def users(request):
    data = get_module_options(request)
    src = data['model'].url
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'users/users_frm.html'
            if action == 'new':
                data['form'] = UserForm()
                data['title'] = 'Registro de Usuarios'
                data['button'] = 'Guardar Usuario'
            elif action == 'edit' and 'id' in request.GET:
                id = request.GET['id']
                if User.objects.filter(token=id).exists():
                    model = User.objects.get(token=id)
                    data['form'] = UserForm(instance=model,initial={'id': model.id, 'token': model.token,'groups': model.groups.filter()})
                    data['title'] = 'Edición de Usuario'
                    data['button'] = 'Editar Usuario'
                else:
                    return HttpResponseRedirect(src)
            else:
                return HttpResponseRedirect(src)
        else:
            data['items'] = User.objects.all()
            data['title'] = 'Listado de Usuarios'
            data['button'] = 'Nuevo Usuario'
            template = 'users/users_dt.html'
        return render(request, template, data)
    elif request.method == 'POST' and 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'new' or action == 'edit':
                if action == 'new':
                    f = UserForm(request.POST, request.FILES)
                elif action == 'edit':
                    f = UserForm(request.POST, request.FILES, instance=User.objects.get(id=request.POST['id'],token=request.POST['token']))
                if f.is_valid():
                    form = f.save(commit=False)
                    if action == 'new':
                        form.set_password(request.POST['dni'])
                    form.save()
                    form.groups.clear()
                    for gr in request.POST.getlist('groups'):
                        form.groups.add(gr)
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            elif action == 'delete':
                User.objects.get(pk=request.POST['id']).delete()
                data['resp'] = True
            elif action == 'repeated':
                type = request.POST['type']
                id = request.POST['id']
                obj = request.POST['obj'].strip()
                if type == 'dni':
                    if id == 0:
                        if User.objects.filter(dni__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if User.objects.filter(dni__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'email':
                    if id == 0:
                        if User.objects.filter(email__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if User.objects.filter(email__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'username':
                    if id == 0:
                        if User.objects.filter(username__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if User.objects.filter(username__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'phone':
                    if id == 0:
                        if User.objects.filter(mobile__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if User.objects.filter(mobile__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'reset_password':
                user = User.objects.get(id=request.POST['id'])
                user.set_password(user.dni)
                user.save()
                data['resp'] = True
            elif action == 'login':
                from django.contrib.auth import login
                admin = User.objects.get(pk=request.POST['id'])
                login(request, admin)
                data['resp'] = True
            elif action == 'access_users':
                data = [[a.id, a.user.get_full_name(),a.date_joined_format(),a.hour_format(), a.localhost, a.hostname] for a in AccessUsers.objects.filter(user_id=request.POST['id'])]
            elif action == 'load':
                data = [[i.id,i.get_full_name(),i.username,i.get_gender_display(),i.email,i.is_active,i.get_image(), str(i.token)] for i in User.objects.filter()]
            elif action == 'get_profiles':
                data = [[i.id,i.name] for i in User.objects.get(pk=request.POST['id']).groups.all()]
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)

@csrf_exempt
def change_profile(request):
    data = get_module_options(request)
    if request.method == 'GET':
        template = ""
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            template = 'users/users_change_password_frm.html'
            if action == 'change_password':
                data['form'] = UserForm()
                data['title'] = 'Cambio de contraseña'
                data['button'] = 'Cambiar Clave'
            elif action == 'personal_information':
                model = User.objects.get(pk=request.user.id)
                data['form'] = UserForm(instance=model,initial={'id': model.id, 'groups': model.groups.filter()},type='profile')
                data['title'] = 'Edición de Usuario'
                data['button'] = 'Editar Usuario'
                template = 'users/users_change_profile_frm.html'
            else:
                return HttpResponseRedirect(HOME)
        return render(request, template, data)
    elif 'action' in request.POST:
        data = {}
        action = request.POST['action']
        try:
            if action == 'repeated':
                type = request.POST['type']
                id = request.POST['id']
                obj = request.POST['obj']
                if type == 'dni':
                    if id == 0:
                        if User.objects.filter(dni__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if User.objects.filter(dni__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                elif type == 'email':
                    if id == 0:
                        if User.objects.filter(email__iexact=obj):
                            return JsonResponse({'valid': 'false'})
                    else:
                        if User.objects.filter(email__iexact=obj).exclude(id=id):
                            return JsonResponse({'valid': 'false'})
                return JsonResponse({'valid': 'true'})
            elif action == 'change_password':
                user = User.objects.get(id=request.user.id)
                user.set_password(request.POST['password'])
                user.save()
                data['resp'] = True
            elif action == 'personal_information':
                model = User.objects.get(pk=request.user.id)
                f = UserForm(request.POST, request.FILES,instance=model,type="profile")
                if f.is_valid():
                    form = f.save(commit=True)
                    form.username = form.generate_username()
                    form.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = f.errors
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = str(e)
            data['resp'] = False
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseRedirect(HOME)

def get_group(id):
    try:
        objs = Group.objects.filter(id=id)
        if objs.exists():
            return objs[0]
        return None
    except:
        return None

def get_group_id_session(request):
    try:
        return int(request.session['group'].id)
    except:
        return 0

@csrf_exempt
def change_groups(request):
    if request.method == 'GET' and 'id' in request.GET:
        try:
            url = request.GET['url']
            objs = get_group(request.GET['id'])
            if objs is None:
                request.session['groups'] = None
            else:
                request.session['group'] = objs
            if not url == "" and not url is None:
                return HttpResponseRedirect(url)
        except Exception as e:
            pass
    return HttpResponseRedirect(HOME)
