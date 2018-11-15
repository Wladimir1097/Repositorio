from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from core.sales.models import *
import csv
from django.http import HttpResponse


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


admin.site.register(Services)


class CliAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'id',
        'name',
        'ruc',
        'bodega',
    )
    ordering = ('id',)
    search_fields = ('ruc', 'name')
    list_filter = (
        'bodega',
    )
    actions = ["export_as_csv"]


admin.site.register(Client, CliAdmin)
admin.site.register(DevolutionSales)


class ChoiceInlineSales(admin.TabularInline):
    model = SalesProducts
    extra = 1


class ChoiceInlineServ(admin.TabularInline):
    model = SalesServices
    extra = 1


class SalesAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'usuario':
            kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
        return super(SalesAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields + ('usuario',)
        return self.readonly_fields

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data['usuario'] = request.user
        request.GET = data
        return super(SalesAdmin, self).add_view(request, form_url="", extra_context=extra_context)

    fieldsets = [(None, {'fields': ['cli']}), (None, {'fields': ['usuario']}),(None, {'fields': ['type']}),
                 ('Informacion Fecha', {'fields': ['date_joined', 'date_delivery'], 'classes': ['collapse']}),
                 (None, {'fields': ['subtotal']})]
    list_display = ('id', 'cli', 'date_joined', 'usuario', 'subtotal')
    search_fields = ['id']
    # raw_id_fields = ('usuario',)
    inlines = [ChoiceInlineSales, ChoiceInlineServ]


admin.site.register(Sales, SalesAdmin)


class GesAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'id',
        'usuario',
        'cantmed',
        'cantsell',
        'date_joined',
    )
    ordering = ('id',)
    search_fields = ('date_joined',)
    list_filter = (
        'usuario',
    )
    actions = ["export_as_csv"]


admin.site.register(GestionMedidor, GesAdmin)


class medAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'id',
        'numeracion',
        'numeracion',
        'estado',
        'date_joined',
    )
    ordering = ('id',)
    search_fields = ('numeracion',)
    list_filter = (
        'gestion', 'usuario'
    )
    actions = ["export_as_csv"]


admin.site.register(InventoryMedidor, medAdmin)


class selAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'id',
        'numeracion',
        'numeracion',
        'estado',
        'date_joined',
    )
    ordering = ('id',)
    search_fields = ('numeracion',)
    list_filter = (
        'gestion', 'usuario'
    )
    actions = ["export_as_csv"]


admin.site.register(InventorySello, selAdmin)
