# Generated by Django 2.1.1 on 2018-09-11 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_auto_20180911_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal',
            name='email',
            field=models.CharField(default=2, max_length=50, unique=True),
            preserve_default=False,
        ),
    ]