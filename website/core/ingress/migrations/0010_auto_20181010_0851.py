# Generated by Django 2.1.1 on 2018-10-10 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_bodega'),
        ('ingress', '0009_auto_20181005_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='bodega',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='company.Bodega', verbose_name='Bodega'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
    ]