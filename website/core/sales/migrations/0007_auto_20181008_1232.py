# Generated by Django 2.1.1 on 2018-10-08 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_auto_20181008_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesmedidores',
            name='estado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='salesmedidores',
            name='numeracion',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='numeracion'),
        ),
        migrations.AlterField(
            model_name='salessellos',
            name='estado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='salessellos',
            name='numeracion',
            field=models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='numeracion'),
        ),
    ]
