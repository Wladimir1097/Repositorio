# Generated by Django 2.1.1 on 2018-10-15 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0015_auto_20181015_1546'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gestionmedidor',
            old_name='cantmsell',
            new_name='cantsell',
        ),
    ]
