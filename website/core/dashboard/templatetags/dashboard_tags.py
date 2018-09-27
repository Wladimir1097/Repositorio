from django import template
from django.forms import CheckboxInput
from core.security.models import Module
register = template.Library()

@register.filter()
def is_checkbox(field):
  return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__

@register.filter()
def get_modules(id, grupo):
   return Module.objects.filter(is_active=True,groupmodule__groups_id=grupo,type_id=id).order_by('name')