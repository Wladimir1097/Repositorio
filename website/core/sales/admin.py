from django.contrib import admin

# Register your models here.
from core.sales.models import *

admin.site.register(Services)
admin.site.register(Client)
admin.site.register(Sales)
admin.site.register(SalesProducts)
admin.site.register(SalesServices)
admin.site.register(DevolutionSales)