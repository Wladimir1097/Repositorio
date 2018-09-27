# -*- codign: utf-8 -*-
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):

        email = self.normalize_email(email)

        if not email:
            raise ValueError("Este Campo es obligatorio")
        if not username:
            raise ValueError("Este campo es obligatorio")

        user = self.model(username=username,email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_user(self, username, email, password = None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username,email, password, **extra_fields)

    def create_superuser(self, username, email, password = None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser = True')
        return self._create_user(username,email, password, **extra_fields)
