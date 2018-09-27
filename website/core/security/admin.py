from django.contrib import admin

# Register your models here.
from core.security.models import *

admin.site.register(Module)
admin.site.register(ModuleType)
admin.site.register(GroupModule)
admin.site.register(Database)
admin.site.register(AccessUsers)