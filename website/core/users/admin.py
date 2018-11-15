from django.contrib import admin
from django.utils.safestring import mark_safe

from core.users.models import User


class Admin(admin.ModelAdmin):
    readonly_fields = ["images"]

    def images(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
            url=obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
        )
        )


admin.site.register(User, Admin)
