# Generated by Django 3.1.7 on 2021-03-18 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0006_auto_20210316_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opening',
            name='frame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frame', to='calculator.structuralelementframe', verbose_name='каркас'),
        ),
    ]