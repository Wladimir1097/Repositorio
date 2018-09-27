from django import template
from core.users.models import User
register = template.Library()

@register.filter()
def get_group(id):
    user = User.objects.get(pk=id)
    if user.groups.all():
        return user.groups.all()[0].name
    return 'Sin grupo'
