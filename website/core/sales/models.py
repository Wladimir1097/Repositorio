from django.db import models

from core.ingress.models import *
from datetime import datetime
from core.dashboard.choices import sales_choices, ESTADOS_SOLICITUD


class Services(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    cost = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor')

    def __str__(self):
        return self.name

    def cost_format(self):
        return format(self.cost, '.2f')

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['-name']


class Client(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, unique=True, verbose_name='Ruc', null=True, blank=True)
    mobile = models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name='Teléfono')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    email = models.CharField(max_length=500, null=True, blank=True, verbose_name='Email')
    bodega = models.ForeignKey(Bodega, verbose_name='Bodega', blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-name']


class Sales(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    cli = models.ForeignKey(Client, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    date_delivery = models.DateField(default=datetime.now)
    type = models.IntegerField(choices=sales_choices, default=1)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)

    def get_iva(self):
        return self.iva / self.subtotal

    def get_nro(self):
        return '%06d' % self.id

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def count_products(self):
        return SalesProducts.objects.filter(sales_id=self.id).aggregate(val=Coalesce(Sum('cant'), 0))['val']

    def count_ent_products(self):
        return SalesProducts.objects.filter(sales_id=self.id).aggregate(val=Coalesce(Sum('cant_ent'), 0))['val']

    def count_prods_rest(self):
        return self.count_products() - self.count_ent_products()

    def subtotal_format(self):
        return format(self.subtotal, '.2f')

    def iva_format(self):
        return format(self.iva, '.2f')

    def dscto_format(self):
        return format(self.dscto, '.2f')

    def total_format(self):
        return format(self.total, '.2f')

    def sales_by_month(self, bodega):
        data = []
        for i in range(1, 13):
            result = Sales.objects.filter(date_joined__month=i, usuario_id__bodega_id=bodega).aggregate(
                resp=Coalesce(Sum('total'), 0.00))['resp']
            data.append(format(result, '.2f'))
        return data

    def get_totals(self):
        subtotal = 0.00
        for d in SalesProducts.objects.filter(sales=self):
            cant = int(d.cant)
            if d.sales.type == 2:
                cant = d.cant_ent
            subtotal += float(d.price) * cant
            d.subtotal = float(d.price) * cant
            d.save()
        for d in SalesServices.objects.filter(sales=self):
            subtotal += float(d.total)
        self.subtotal = float(subtotal)
        self.iva = float(0.12) * float(self.subtotal)
        self.total = float(self.subtotal) + float(self.iva)
        self.save()

    class Meta:
        db_table = 'sales'
        verbose_name = 'Despacho'
        verbose_name_plural = 'Despachos'
        ordering = ['-id']


class SalesProducts(models.Model):
    sales = models.ForeignKey(Sales, on_delete=models.PROTECT)
    prod = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    cant_ent = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    is_dispatched = models.BooleanField(default=True)

    def __str__(self):
        return str(self.prod.name)

    def get_dscto(self):
        return format(self.dscto / self.subtotal, '.2f')

    def price_format(self):
        return format(self.price, '.2f')

    def dscto_format(self):
        return format(self.dscto, '.2f')

    def subtotal_format(self):
        return format(self.subtotal, '.2f')

    class Meta:
        verbose_name = 'Detalle de Producto'
        verbose_name_plural = 'Detalle de Productos'
        ordering = ['-id']


class SalesServices(models.Model):
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE)
    serv = models.ForeignKey(Services, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)

    def total_format(self):
        return format(self.total, '.2f')

    class Meta:
        verbose_name = 'Detalle de la Despacho'
        verbose_name_plural = 'Detalle de las Despachos'
        ordering = ['-id']


class DevolutionSales(models.Model):
    date_joined = models.DateField(default=datetime.now)
    det = models.ForeignKey(SalesProducts, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)

    def __str__(self):
        return str(self.det.prod.name)

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    class Meta:
        verbose_name = 'Devolución'
        verbose_name_plural = 'Devoluciones'
        ordering = ['-id']


class GestionMedidor(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    cantmed = models.IntegerField(default=0)
    cantsell = models.IntegerField(default=0)
    date_joined = models.DateField(default=datetime.now)

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')


class MedidorType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class InventoryMedidor(models.Model):
    gestion = models.ForeignKey(GestionMedidor, on_delete=models.PROTECT)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    sales = models.ForeignKey(Sales, on_delete=models.PROTECT, blank=True, null=True)
    medtype = models.ForeignKey(MedidorType, on_delete=models.PROTECT, blank=True, null=True)
    cli = models.ForeignKey(Client, on_delete=models.PROTECT, blank=True, null=True)
    date_joined = models.DateField(default=datetime.now)
    date_delivery = models.DateField(default=datetime.now)
    numeracion = models.CharField(max_length=100)
    distribuido = models.BooleanField(default=False)
    estado = models.BooleanField(default=False)

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def date_delivery_format(self):
        return self.date_delivery.strftime('%Y-%m-%d')


class InventorySello(models.Model):
    gestion = models.ForeignKey(GestionMedidor, on_delete=models.PROTECT)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    sales = models.ForeignKey(Sales, on_delete=models.PROTECT, blank=True, null=True)
    cli = models.ForeignKey(Client, on_delete=models.PROTECT, blank=True, null=True)
    date_joined = models.DateField(default=datetime.now)
    date_delivery = models.DateField(default=datetime.now)
    numeracion = models.CharField(max_length=100)
    distribuido = models.BooleanField(default=False)
    estado = models.BooleanField(default=False)

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def date_delivery_format(self):
        return self.date_delivery.strftime('%Y-%m-%d')
