from django.contrib import admin

from core.employees.models import *

admin.site.register(Personal)
admin.site.register(Contracts)
admin.site.register(Faults)
admin.site.register(Salary)
# Register your models here.
