# -*- coding: utf-8 -*-
import uuid
from django.shortcuts import render
from django.contrib.auth import *
from django.http import *
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from config.settings.base import LOGIN_URL
from core.security.models import AccessUsers
from core.users.models import User

@csrf_exempt
def session_login(request):
    data = {
        'title': 'Inicio de sesión',
    }
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET['action']
            data['action'] = action
            if action == 'change_password' and 'id' in request.GET:
                users = User.objects.filter(token=request.GET['id'], is_change_password=True)
                if users.exists():
                    data['id'] = users[0].token
                    return render(request, 'login/login_change_password_frm.html', data)
                return HttpResponseRedirect(LOGIN_URL)
            else:
                return HttpResponseRedirect(LOGIN_URL)
        return render(request, 'login/login.html', data)
    elif request.method == 'POST':
        try:
            data = {}
            action = request.POST['action']
            if action == 'reset_password':
                info = User.objects.filter(email=request.POST['email'])
                if info:
                    user = User.objects.get(pk=info[0].id)
                    server = request.META['HTTP_HOST']
                    user.is_change_password = True
                    user.token = uuid.uuid4()
                    user.save()
                    send_email_reset_password(user.id, server)
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = 'El correo ingresado no se encuentra registrado..!'
            elif action == 'change_password':
                if User.objects.filter(token=request.POST['id'], is_change_password=True):
                    user = User.objects.get(token=request.POST['id'])
                    user.set_password(request.POST['password'])
                    user.is_change_password = False
                    user.save()
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = 'Ha ocurrido un error, la contraseña no ha podido cambiar'
            elif action == 'connect':
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    login(request, user)
                    AccessUsers(user=user).save()
                    data['msg'] = 'Iniciando sesión..'
                    data['resp'] = True
                    data['url'] = settings.HOME
                else:
                    data['resp'] = False
                    data['error'] = 'Credenciales incorrectas'
            else:
                data['error'] = 'Ha ocurrido un error'
                data['resp'] = False
        except Exception as e:
            data['error'] = e
        return HttpResponse(json.dumps(data), content_type="application/json")

def send_email_reset_password(id, server):
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    user = User.objects.get(pk=id)
    activate_account = "{}{}{}{}".format('http://', server, '/login/?action=change_password&id=',
                                         user.token)
    msg_html = render_to_string('login/login_reset_email.html', {'user': user, 'link': activate_account})
    subject = "Reseteo de contraseña"
    msg = EmailMessage(subject=subject, body=msg_html, to=[user.email])
    msg.content_subtype = "html"
    msg.send()

def login_default(request):
    return HttpResponseRedirect(LOGIN_URL)
