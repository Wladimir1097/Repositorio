# Generated by Django 2.1.1 on 2018-10-08 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_auto_20181008_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesmedidores',
            name='cant',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='salessellos',
            name='cant',
            field=models.IntegerField(default=0),
        ),
    ]
