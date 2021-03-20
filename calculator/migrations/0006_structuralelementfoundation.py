# Generated by Django 3.1.7 on 2021-03-18 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0005_auto_20210316_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='StructuralElementFoundation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perimeter_of_external_walls', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Периметр внешних стен')),
                ('internal_wall_length', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Длина внутренних стен')),
                ('concrete_pile', models.CharField(max_length=100, verbose_name='Бетонная свая')),
                ('concrete', models.CharField(max_length=100, verbose_name='Бетон')),
                ('calculations', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='structural_element_foundation', to='calculator.calculation', verbose_name='Расчет')),
            ],
            options={
                'verbose_name': 'Конструктивный элемент фундамент',
                'verbose_name_plural': 'Конструктивный элемент фундамент',
            },
        ),
    ]
