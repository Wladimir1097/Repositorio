# -*- codign: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .managers import UserManager
from core.dashboard.choices import gender_choices
from django.core.mail import send_mail
from config.settings.base import MEDIA_URL, STATIC_URL
import unicodedata
import uuid
from core.company.models import Bodega


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='Username', max_length=20, unique=True)
    first_name = models.CharField(verbose_name="Nombres", max_length=255)
    last_name = models.CharField(verbose_name="Apellidos", max_length=255)
    dni = models.CharField(max_length=13, unique=True, verbose_name="Cédula o RUC")
    email = models.EmailField(verbose_name="Correo Electrónico", unique=True)
    phone = models.CharField(verbose_name="Teléfono Convencional", max_length=255, null=True, blank=True)
    mobile = models.CharField(verbose_name="Teléfono Celular", max_length=255, null=True, blank=True)
    gender = models.IntegerField(choices=gender_choices, verbose_name="Género", default=1)
    address = models.CharField(verbose_name="Dirección", max_length=255, null=True, blank=True)
    birthdate = models.DateField(verbose_name="Fecha de Nacimiento", blank=True, null=True)
    image = models.ImageField(upload_to='users/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_change_password = models.BooleanField(default=False)
    bodega = models.ForeignKey(Bodega, verbose_name='Bodega', blank=True, null=True, on_delete=models.PROTECT)

    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True, default=uuid.uuid4, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def generate_username(self):
        first_name = self.first_name.lower().strip().split(" ")
        last_name = self.last_name.lower().strip().split(" ")
        try:
            if len(first_name) > 1 and len(last_name) > 1:
                username = first_name[0][0] + last_name[0] + last_name[1][0]
                base = username
                cod = 1
                while User.objects.filter(username=username).exclude(id=self.id).exists():
                    username = "{}{}".format(base, cod)
                    cod = cod + 1
                return ''.join(c for c in unicodedata.normalize('NFD', username) if unicodedata.category(c) != 'Mn')
        except:
            return None

    def generate_token(self):
        return uuid.uuid4()

    def get_short_name(self):
        return self.first_name

    def get_age(self):
        from datetime import date
        return date.today().year - self.birthdate.year

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_birthdate(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def get_address(self):
        return self.address

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_image(self):
        if self.image:
            return "{0}{1}".format(MEDIA_URL, self.image)
        return "{0}{1}".format(STATIC_URL, 'img/default/user.png')

    def age(self):
        from datetime import date
        diff = (date.today() - self.birthdate).days
        years = str(int(diff / 365))
        return years

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
