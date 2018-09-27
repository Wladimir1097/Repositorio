from django.db import models
from datetime import datetime

from django.db.models.functions import Coalesce

from core.dashboard.choices import months_choices
from core.company.models import Company
from config.settings.base import STATIC_URL, MEDIA_URL

class Personal(models.Model):
    comp = models.ForeignKey(Company, null=True, blank=True, on_delete=models.PROTECT)
    names = models.CharField(max_length=150, unique=True, verbose_name='Nombres')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Cédula')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono Celular')
    email = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='Dirección')
    avatar = models.ImageField(upload_to='personal/%Y/%m/%d', verbose_name='Avatar', null=True, blank=True)

    def __str__(self):
        return self.names

    def get_avatar(self):
        if self.avatar:
            return "{0}{1}".format(MEDIA_URL, self.avatar)
        return "{0}{1}".format(STATIC_URL, 'img/default/user.png')

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['id']


class Contracts(models.Model):
    pers = models.ForeignKey(Personal,verbose_name='Personal', on_delete=models.PROTECT)
    start_date = models.DateField(default=datetime.now, verbose_name='Fecha de inicio')
    end_date = models.DateField(default=datetime.now, verbose_name='Fecha de finalización')
    rmu = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor')
    is_active = models.BooleanField(default=True, verbose_name='¿Es activo?')

    def __str__(self):
        return self.pers.names

    def get_nro(self):
        return '%06d' % self.id

    def rmu_format(self):
        return format(self.rmu, '.2f')

    def start_date_format(self):
        return self.start_date.strftime('%Y-%m-%d')

    def end_date_format(self):
        return self.end_date.strftime('%Y-%m-%d')

    def get_day_salary(self):
        return self.rmu / 24

    def get_falts_count(self, year, month):
        return Faults.objects.filter(cont_id=self.id,date_joined__month=month, date_joined__year=year).count()

    def get_dsctos(self, year, month):
        return self.get_falts_count(year=year, month=month) * float(self.get_day_salary())

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['id']


class Faults(models.Model):
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
    cont = models.ForeignKey(Contracts, verbose_name='Empleado', on_delete=models.PROTECT)
    details = models.CharField(max_length=1000, null=True, blank=True, default='Sin detalles', verbose_name='Detalles')

    def __str__(self):
        return self.details

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    class Meta:
        verbose_name = 'Falta'
        verbose_name_plural = 'Faltas'
        ordering = ['id']


class Salary(models.Model):
    date_joined = models.DateField(default=datetime.now)
    cont = models.ForeignKey(Contracts, on_delete=models.PROTECT)
    year = models.IntegerField()
    month = models.IntegerField(choices=months_choices)
    falts = models.IntegerField(default=0)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.get_month_display()

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def dscto_format(self):
        return format(self.dscto, '.2f')

    def total_format(self):
        return format(self.total, '.2f')

    class Meta:
        verbose_name = 'Salario'
        verbose_name_plural = 'Salarios'
        ordering = ['id']
