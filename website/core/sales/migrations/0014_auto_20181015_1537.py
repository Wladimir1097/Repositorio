# Generated by Django 2.1.1 on 2018-10-15 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0013_auto_20181015_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorymedidor',
            name='prod',
        ),
        migrations.AlterField(
            model_name='inventorymedidor',
            name='cli',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sales.Client'),
        ),
        migrations.AlterField(
            model_name='inventorymedidor',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='inventorymedidor',
            name='medtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sales.MedidorType'),
        ),
    ]