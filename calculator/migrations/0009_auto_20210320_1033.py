# Generated by Django 3.1.7 on 2021-03-20 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0008_structuralelementfoundation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='structuralelementframe',
            name='OSB_for_base_area',
            field=models.CharField(help_text='Название материала', max_length=50, verbose_name='ОСБ для потолка и пола'),
        ),
        migrations.AlterField(
            model_name='structuralelementframe',
            name='OSB_for_external_walls',
            field=models.CharField(help_text='Название материала', max_length=50, verbose_name='ОСБ для наружных стен'),
        ),
        migrations.AlterField(
            model_name='structuralelementframe',
            name='OSB_for_interior_walls',
            field=models.CharField(help_text='Название материала', max_length=50, verbose_name='ОСБ для внутренних стен'),
        ),
        migrations.AlterField(
            model_name='structuralelementframe',
            name='insulation_base_area',
            field=models.CharField(help_text='Название материала', max_length=50, verbose_name='Утеплитель'),
        ),
        migrations.AlterField(
            model_name='structuralelementframe',
            name='insulation_external_walls',
            field=models.CharField(help_text='Название материала', max_length=50, verbose_name='Утеплитель'),
        ),
        migrations.AlterField(
            model_name='structuralelementframe',
            name='steam_waterproofing_base_area',
            field=models.CharField(help_text='Название материала', max_length=50, verbose_name='Парогидроизоляция'),
        ),
        migrations.AlterField(
            model_name='structuralelementframe',
            name='steam_waterproofing_external_walls',
            field=models.CharField(help_text='Название материала', max_length=50, verbose_name='Парогидроизоляция'),
        ),
        migrations.AlterField(
            model_name='structuralelementframe',
            name='windscreen_base_area',
            field=models.CharField(help_text='Название материала', max_length=50, verbose_name='Ветрозащита'),
        ),
        migrations.AlterField(
            model_name='structuralelementframe',
            name='windscreen_external_walls',
            field=models.CharField(help_text='Название материала', max_length=50, verbose_name='Ветрозащита'),
        ),
    ]