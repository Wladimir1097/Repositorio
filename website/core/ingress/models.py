from django.conf import settings
from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import Sum
from config.settings.base import STATIC_URL, MEDIA_URL
from datetime import datetime

from core.company.models import Bodega
from core.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name="Descripción")
    bodega = models.ForeignKey(Bodega, verbose_name='Bodega', blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-name']


class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    bodega = models.ForeignKey(Bodega, verbose_name='Bodega', blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
        ordering = ['-name']


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    cat = models.ForeignKey(Category, verbose_name='Categoria', null=True, blank=True, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, verbose_name='Marca', null=True, blank=True, on_delete=models.PROTECT)
    cost = models.DecimalField(decimal_places=5, max_digits=9, default=0.00, verbose_name='Costo')
    price = models.DecimalField(decimal_places=5, max_digits=9, default=0.00, verbose_name='Precio')
    image = models.ImageField(upload_to='product/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    bodega = models.ForeignKey(Bodega, verbose_name='Bodega', blank=True, null=True, on_delete=models.PROTECT)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_cat(self):
        if self.cat:
            return self.cat.name
        return None

    def get_image(self):
        if self.image:
            return "{0}{1}".format(MEDIA_URL, self.image)
        return "{0}{1}".format(STATIC_URL, 'img/default/product.png')

    def get_ingress(self):
        cant = Inventory.objects.filter(prod=self).aggregate(resp=Coalesce(Sum('cant'), 0))['resp']
        dif = Inventory.objects.filter(prod=self).aggregate(resp=Coalesce(Sum('diferencia'), 0))['resp']
        return cant - dif

    def get_sales(self):
        from core.sales.models import SalesProducts
        return SalesProducts.objects.filter(prod=self, sales__type=1).aggregate(resp=Coalesce(Sum('cant'), 0))['resp']

    def get_pedids(self):
        from core.sales.models import SalesProducts
        return SalesProducts.objects.filter(prod=self, sales__type=2).aggregate(resp=Coalesce(Sum('cant_ent'), 0))[
            'resp']

    def cost_format(self):
        return format(self.cost, '.5f')

    def price_format(self):
        return format(self.price, '.5f')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-name']


class Provider(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, verbose_name='Ruc', blank=True, null=True)
    mobile = models.CharField(max_length=10, null=True, blank=True, verbose_name='Celular')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    email = models.CharField(max_length=500, null=True, blank=True, verbose_name='Email')
    bodega = models.ForeignKey(Bodega, verbose_name='Bodega', blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def toJSON(self):
        return {'ruc': self.ruc, 'phone': self.mobile, 'email': self.email, 'address': self.address, 'name': self.name}

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-name']


class Ingress(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    prov = models.ForeignKey(Provider, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return self.prov.name

    def get_nro(self):
        return format(self.id, '%06d')

    def get_cant_products(self):
        return Inventory.objects.filter(ing=self).aggregate(val=Coalesce(Sum('cant'), 0))['val']

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def subtotal_format(self):
        return format(self.subtotal, '.2f')

    def iva_format(self):
        return format(self.iva, '.2f')

    def dscto_format(self):
        return format(self.dscto, '.2f')

    def total_format(self):
        return format(self.total, '.2f')

    def get_totals(self):
        subtotal = 0.00
        for d in Inventory.objects.filter(ing=self):
            subtotal += float(d.subtotal)
            # subtotal += float(d.price) * int(d.cant)
        self.subtotal = subtotal
        # self.iva = float(0.12) * float(self.subtotal)
        self.iva = 0
        self.total = float(self.subtotal) + float(self.iva)
        self.save()

    class Meta:
        verbose_name = 'Despacho'
        verbose_name_plural = 'Despachos'
        ordering = ['-id']


class Inventory(models.Model):
    ing = models.ForeignKey(Ingress, on_delete=models.PROTECT)
    prod = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=5, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    diferencia = models.IntegerField(default=0)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return self.prod.name

    def price_format(self):
        return format(self.price, '.5f')

    def dscto_format(self):
        return format(self.dscto, '.5f')

    def subtotal_format(self):
        return format(self.subtotal, '.2f')

    def total_format(self):
        return format(self.total, '.2f')

    def get_dscto(self):
        return str((self.dscto / self.subtotal) * 100)

    def get_sub(self):
        return float(self.price) * int(self.diferencia)

    def get_subTotal(self):
        subtotal = 0.00
        for d in Inventory.objects.filter(ing=self):
            subtotal += d.get_sub()
        return subtotal

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['-id']

