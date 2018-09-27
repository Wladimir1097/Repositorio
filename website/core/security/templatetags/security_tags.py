from django import template
from core.security.models import Module
register = template.Library()

@register.filter()
def get_modules_vertical(type,group):
    return Module.objects.filter(groupmodule__groups_id=group,type_id=type,is_active=True,is_vertical=True).order_by('name')

@register.filter()
def get_modules_by_group(id):
    return Module.objects.filter(groupmodule__groups_id=id,is_active=True)

@register.filter()
def get_count_modules_by_group(id):
    return Module.objects.filter(groupmodule__groups_id=id,is_active=True).count()
