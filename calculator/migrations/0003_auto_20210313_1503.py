# Generated by Django 3.1.7 on 2021-03-13 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0002_auto_20210312_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculation',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calculation', to='calculator.customers', verbose_name='Заказчик'),
        ),
    ]
