# Generated by Django 2.1.1 on 2018-09-16 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_auto_20180915_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesproducts',
            name='cant_ent',
            field=models.IntegerField(default=0),
        ),
    ]