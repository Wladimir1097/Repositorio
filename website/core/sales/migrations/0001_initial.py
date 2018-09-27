# Generated by Django 2.1.1 on 2018-09-11 03:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingress', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('ruc', models.CharField(blank=True, max_length=13, null=True, unique=True, verbose_name='Ruc')),
                ('phone', models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Teléfono')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Dirección')),
                ('email', models.CharField(blank=True, max_length=500, null=True, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='DevolutionSales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('cant', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Devolución',
                'verbose_name_plural': 'Devoluciones',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('date_delivery', models.DateField(default=datetime.datetime.now)),
                ('type', models.IntegerField(choices=[(1, 'Venta'), (2, 'Pedido')], default=1)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cli', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.Client')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'db_table': 'sales',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SalesProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('is_dispatched', models.BooleanField(default=True)),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ingress.Product')),
                ('sales', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.Sales')),
            ],
            options={
                'verbose_name': 'Detalle de Producto',
                'verbose_name_plural': 'Detalle de Productos',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SalesServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('sales', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.Sales')),
            ],
            options={
                'verbose_name': 'Detalle de la Venta',
                'verbose_name_plural': 'Detalle de las Ventas',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
                'ordering': ['-name'],
            },
        ),
        migrations.AddField(
            model_name='salesservices',
            name='serv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.Services'),
        ),
        migrations.AddField(
            model_name='devolutionsales',
            name='det',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.SalesProducts'),
        ),
    ]
