# Generated by Django 2.1.1 on 2018-10-10 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_bodega'),
        ('sales', '0009_medidoresdetalle_sellosdetalle'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='bodega',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='company.Bodega', verbose_name='Bodega'),
        ),
    ]
