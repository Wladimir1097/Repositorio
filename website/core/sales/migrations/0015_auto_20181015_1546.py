# Generated by Django 2.1.1 on 2018-10-15 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0014_auto_20181015_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorymedidor',
            name='estado',
            field=models.BooleanField(default=False),
        ),
    ]
