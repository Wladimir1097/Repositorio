# Generated by Django 2.1.1 on 2018-09-11 03:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('hour', models.TimeField(default=datetime.datetime.now)),
                ('localhost', models.TextField()),
                ('hostname', models.TextField(default='DESKTOP-8I2OMDM')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Acceso del usuario',
                'verbose_name_plural': 'Accesos de los usuarios',
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(default=datetime.datetime.now)),
                ('hour', models.TimeField(default=datetime.datetime.now)),
                ('localhost', models.CharField(blank=True, max_length=100, null=True)),
                ('hostname', models.TextField(blank=True, default='DESKTOP-8I2OMDM', null=True)),
                ('archive', models.FileField(upload_to='backup/%Y/%m/%d')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Respaldos de BD',
                'verbose_name_plural': 'Respaldo de BD',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='GroupModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groups', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.Group')),
            ],
            options={
                'verbose_name': 'Grupo Módulo',
                'verbose_name_plural': 'Grupos Módulos',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100, unique=True, verbose_name='Url')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Descripción')),
                ('icon', models.CharField(blank=True, max_length=100, null=True, verbose_name='Icono')),
                ('image', models.ImageField(blank=True, null=True, upload_to='module/%Y/%m/%d', verbose_name='Imagen')),
                ('is_vertical', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_visible', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Módulo',
                'verbose_name_plural': 'Módulos',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='ModuleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('icon', models.CharField(max_length=100, unique=True, verbose_name='Icono')),
                ('is_active', models.BooleanField(default=True, verbose_name='¿Esta activo?')),
            ],
            options={
                'verbose_name': 'Tipo de Módulo',
                'verbose_name_plural': 'Tipos de Módulos',
                'ordering': ['-name'],
            },
        ),
        migrations.AddField(
            model_name='module',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='security.ModuleType', verbose_name='Tipo de Módulo'),
        ),
        migrations.AddField(
            model_name='groupmodule',
            name='modules',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='security.Module'),
        ),
    ]