# Generated by Django 2.1.1 on 2018-10-08 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_auto_20181008_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesmedidores',
            name='numeracion',
            field=models.PositiveIntegerField(default=0, verbose_name='numeracion'),
        ),
        migrations.AlterField(
            model_name='salessellos',
            name='numeracion',
            field=models.PositiveIntegerField(default=0, verbose_name='numeracion'),
        ),
    ]
