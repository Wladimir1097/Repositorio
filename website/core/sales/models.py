from core.ingress.models import *
from datetime import datetime
from core.dashboard.choices import sales_choices


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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-name']


class Sales(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    date_delivery = models.DateField(default=datetime.now)
    type = models.IntegerField(choices=sales_choices, default=1)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.id

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
        return self.count_products()-self.count_ent_products()

    def subtotal_format(self):
        return format(self.subtotal, '.2f')

    def iva_format(self):
        return format(self.iva, '.2f')

    def dscto_format(self):
        return format(self.dscto, '.2f')

    def total_format(self):
        return format(self.total, '.2f')

    def sales_by_month(self):
        data = []
        for i in range(1, 13):
            result = Sales.objects.filter(date_joined__month=i).aggregate(resp=Coalesce(Sum('total'), 0.00))['resp']
            data.append(format(result,'.2f'))
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
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
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
        return self.prod.name

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
    sales = models.ForeignKey(Sales, on_delete=models.PROTECT)
    serv = models.ForeignKey(Services, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.id

    def total_format(self):
        return format(self.total, '.2f')

    class Meta:
        verbose_name = 'Detalle de la Venta'
        verbose_name_plural = 'Detalle de las Ventas'
        ordering = ['-id']


class DevolutionSales(models.Model):
    date_joined = models.DateField(default=datetime.now)
    det = models.ForeignKey(SalesProducts, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)

    def __str__(self):
        return self.det.prod.name

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    class Meta:
        verbose_name = 'Devolución'
        verbose_name_plural = 'Devoluciones'
        ordering = ['-id']