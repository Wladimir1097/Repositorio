from django.contrib import admin

# Register your models here.
from core.ingress.models import *

admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Ingress)
admin.site.register(Provider)
admin.site.register(Brand)
admin.site.register(Category)