from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from config.settings.base import HOME
from core.security.models import Module


def access_module(f):
    @login_required
    @csrf_exempt
    def access(*args, **kwargs):
        request = args[0]
        try:
            from core.users.views.users.views import get_group_id_session
            id = get_group_id_session(request)
            get_modules_hrz_vrt_treev(request)
            if request.user.is_authenticated:
                modules = Module.objects.filter(groupmodule__groups_id__in=[id], is_active=True, url=request.path,
                                                is_visible=True)
                if modules.exists() and modules.filter().exclude(type_id__isnull=True).exclude(
                        type__is_active=False).exists():
                    return f(request)
                else:
                    return HttpResponseRedirect(HOME)
            else:
                return HttpResponseRedirect(HOME)
        except Exception as e:
            print(e)
            return HttpResponseRedirect(HOME)
    return access



def get_modules_hrz_vrt_treev(request):
    from core.security.models import ModuleType
    from core.company.views.company.views import get_company
    if request.user.groups.filter():
        request.session['comp'] = get_company()
        id = request.user.groups.all()[0].id
        request.session['groups'] = request.user.groups.all()
        groups_first = request.user.groups.all()[0]
        if 'group' in request.session:
            groups_first = request.session['group']
            id = groups_first.id
        request.session['group'] = groups_first
        request.session['modules'] = ModuleType.objects.filter(module__groupmodule__groups_id=id,is_active=True).distinct().order_by('name')
        request.session['modules_horizontal'] = Module.objects.filter(groupmodule__groups_id=id, is_active=True,is_vertical=False,is_visible=True).distinct().order_by('name')
    else:
        request.session['modules'] = None
