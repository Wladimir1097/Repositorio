from django.contrib.auth import get_user_model
from django.forms import Textarea
from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from core.ingress.models import *
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


class ProAdmin(admin.ModelAdmin, ExportCsvMixin):
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


admin.site.register(Provider, ProAdmin)
admin.site.register(Brand)


class DocAdmin(admin.ModelAdmin, ExportCsvMixin):
    readonly_fields = ["images"]

    def images(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
        )
        )


admin.site.register(Document, DocAdmin)
admin.site.register(Category)


class ProducAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'id',
        'name',
        'cat',
        'brand',
        'cost',
        'stock',
        'bodega',
    )
    ordering = ('name',)
    search_fields = ('id', 'name', 'stock')
    list_filter = (
        'bodega',
    )
    actions = ["export_as_csv"]


admin.site.register(Product, ProducAdmin)


class ChoiceInline(admin.TabularInline):
    model = Inventory
    extra = 1


class IngresoProductoAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'usuario':
            kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
        return super(IngresoProductoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields + ('usuario',)
        return self.readonly_fields

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data['usuario'] = request.user
        request.GET = data
        return super(IngresoProductoAdmin, self).add_view(request, form_url="", extra_context=extra_context)

    fieldsets = [(None, {'fields': ['prov']}), (None, {'fields': ['usuario']}),
                 ('Informacion Fecha', {'fields': ['date_joined'], 'classes': ['collapse']}),
                 (None, {'fields': ['subtotal']})]
    list_display = ('id', 'prov', 'date_joined', 'usuario', 'subtotal')
    search_fields = ['id']
    # raw_id_fields = ('usuario',)
    inlines = [ChoiceInline]


admin.site.register(Ingress, IngresoProductoAdmin)
