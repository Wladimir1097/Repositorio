from django.contrib.auth.models import Group
from django.db import models
from datetime import *
from django.utils import timezone
import socket
from config.settings.base import STATIC_URL, MEDIA_URL


class ModuleType(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
    icon = models.CharField(max_length=100, unique=True, verbose_name='Icono')
    is_active = models.BooleanField(default=True, verbose_name='¿Esta activo?')

    def __str__(self):
        return self.name

    def get_is_active_icon(self):
        if self.is_active:
            return 'fa fa-check'
        return 'fa fa-times'

    class Meta:
        verbose_name = 'Tipo de Módulo'
        verbose_name_plural = 'Tipos de Módulos'
        ordering = ['-name']


class Module(models.Model):
    url = models.CharField(max_length=100, verbose_name='Url', unique=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    type = models.ForeignKey(ModuleType, null=True, blank=True, verbose_name='Tipo de Módulo', on_delete=models.PROTECT)
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='Descripción')
    icon = models.CharField(max_length=100, verbose_name='Icono', null=True, blank=True)
    image = models.ImageField(upload_to='module/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    is_vertical = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return "{} [{}]".format(self.name, self.url)

    def get_icon(self):
        if self.icon:
            return self.icon
        return "fa fa-times"

    def get_image(self):
        if self.image:
            return "{0}{1}".format(MEDIA_URL, self.image)
        return "{0}{1}".format(STATIC_URL, 'img/default/module.png')

    def get_image_icon(self):
        if self.image:
            return "{0}{1}".format(MEDIA_URL, self.image)
        if self.icon:
            return self.icon
        return "{0}{1}".format(STATIC_URL, 'img/default/module.png')

    def get_type(self):
        if self.type:
            return self.type.name
        return None

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['-name']


class GroupModule(models.Model):
    groups = models.ForeignKey(Group, on_delete=models.PROTECT)
    modules = models.ForeignKey(Module, on_delete=models.PROTECT)

    def __str__(self):
        return '%s' % (self.id)

    class Meta:
        verbose_name = 'Grupo Módulo'
        verbose_name_plural = 'Grupos Módulos'
        ordering = ['-id']


class Database(models.Model):
    from core.users.models import User
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date_joined = models.DateTimeField(default=datetime.now)
    hour = models.TimeField(default=datetime.now)
    localhost = models.CharField(max_length=100, null=True, blank=True)
    hostname = models.TextField(default=socket.gethostname(), null=True, blank=True)
    archive = models.FileField(upload_to='backup/%Y/%m/%d')

    def date_joined_format(self):
        return self.date_joined.strftime("%d-%m-%Y")

    def hour_format(self):
        return self.hour.strftime("%H:%M %p")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.localhost = socket.gethostbyname(socket.gethostname())
        except:
            self.localhost = None
        super(Database, self).save()

    def get_archive(self):
        if self.archive:
            return "{0}{1}".format(MEDIA_URL, self.archive)
        return "{0}{1}".format(STATIC_URL, 'backup_bd/database.txt')

    class Meta:
        verbose_name_plural = 'Respaldo de BD'
        verbose_name = 'Respaldos de BD'
        ordering = ['-id']


class AccessUsers(models.Model):
    from core.users.models import User
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date_joined = models.DateTimeField(default=timezone.now)
    hour = models.TimeField(default=datetime.now)
    localhost = models.TextField()
    hostname = models.TextField(default=socket.gethostname())

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.localhost = socket.gethostbyname(socket.gethostname())
        except:
            self.localhost = None
        super(AccessUsers, self).save()

    def date_joined_format(self):
        return self.date_joined.strftime("%d-%m-%Y")

    def hour_format(self):
        return self.hour.strftime("%H:%M %p")

    class Meta:
        verbose_name = "Acceso del usuario"
        verbose_name_plural = "Accesos de los usuarios"
        ordering = ['-id']
        default_permissions = ()
