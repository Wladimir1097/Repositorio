from django.contrib import admin

# Register your models here.
from core.company.models import *

admin.site.register(Company)
admin.site.register(Expenses)
admin.site.register(Tools)
admin.site.register(TypeExpense)