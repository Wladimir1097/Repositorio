from django.db import models
from config.settings.base import STATIC_URL, MEDIA_URL, MEDIA_ROOT, STATIC_ROOT
from datetime import datetime


class Bodega(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    address = models.CharField(verbose_name="Ubicacion", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        ordering = ['id']


class Company(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=50, unique=True)
    proprietor = models.CharField(verbose_name="Propietario", max_length=255, blank=True, null=True)
    ruc = models.CharField(verbose_name="Ruc", max_length=13, unique=True, blank=True, null=True)
    phone = models.CharField(verbose_name="Teléfono Convencional", max_length=7, unique=True, blank=True, null=True)
    mobile = models.CharField(verbose_name="Teléfono Celular", max_length=10, unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name="Correo Electrónico", max_length=50, unique=True, blank=True, null=True)
    icon = models.ImageField(verbose_name='Logo', upload_to='library/%Y/%m/%d', null=True, blank=True)
    address = models.CharField(verbose_name="Dirección", max_length=255, blank=True, null=True)
    mission = models.CharField(verbose_name="Misión", max_length=1000, blank=True, null=True)
    vision = models.CharField(verbose_name="Visión", max_length=1000, blank=True, null=True)
    about_us = models.CharField(verbose_name="Quienes Somos", max_length=1000, blank=True, null=True)
    schedule = models.CharField(verbose_name="Horario", max_length=255)

    def __str__(self):
        return self.name

    def login(self):
        return "{0}{1}".format(MEDIA_URL, 'library/2018/10/11/MEMBRETE_PROENERGY_SA.JPG')

    def get_icon_base64(self):
        return self.generate_img_base64()

    def generate_img_base64(self):
        try:
            from PIL import Image
            import base64
            if self.icon:
                # image = base64.b64encode(open(self.icon.path, "rb").read()).decode('utf-8')
                image = base64.b64encode(open("{0}{1}".format(MEDIA_ROOT,
                                                              'library/2018/10/11/MEMBRETE_PROENERGY_SA.JPG'),
                                              "rb").read()).decode('utf-8')
            else:
                image = base64.b64encode(
                    open("{0}{1}".format(STATIC_URL, 'img/default/company.png'), "rb").read()).decode('utf-8')
            type_image = Image.open(self.icon.path)
            type_image = type_image.format.lower()
            return "data:image/{};base64,{}".format(type_image, image)
        except Exception as e:
            raise

    def get_icon(self):
        if self.icon:
            return "{0}{1}".format(MEDIA_URL, self.icon)
        return "{0}{1}".format(STATIC_URL, 'img/default/company.png')

    class Meta:
        verbose_name = 'Compañia'
        verbose_name_plural = 'Compañias'
        ordering = ['-name']


class TypeExpense(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo de Gasto'
        verbose_name_plural = 'Tipos de Gastos'
        ordering = ['id']


class Expenses(models.Model):
    type = models.ForeignKey(TypeExpense, verbose_name='Tipo de Gasto', on_delete=models.PROTECT)
    comp = models.ForeignKey(Company, null=True, blank=True, on_delete=models.PROTECT)
    details = models.CharField(max_length=500, verbose_name='Detalles', null=True, blank=True, default='Sin detalles')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
    cost = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor')

    def __str__(self):
        return self.details

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def cost_format(self):
        return format(self.cost, '.2f')

    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ['id']


class Tools(models.Model):
    comp = models.ForeignKey(Company, null=True, blank=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
    code = models.CharField(max_length=20, unique=True, verbose_name='Serie')
    cost = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor')
    guarantee = models.IntegerField(default=0, verbose_name='Garantía (Años)')
    dep = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

    def date_joined_format(self):
        return self.date_joined.strftime('%Y-%m-%d')

    def cost_format(self):
        return format(self.cost, '.2f')

    def dep_format(self):
        return format(self.dep, '.2f')

    class Meta:
        verbose_name = 'Herramienta'
        verbose_name_plural = 'Herramientas'
        ordering = ['id']
