# Generated by Django 2.1.1 on 2018-10-16 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0018_auto_20181016_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorymedidor',
            name='numeracion',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='inventorysello',
            name='numeracion',
            field=models.CharField(max_length=100),
        ),
    ]
