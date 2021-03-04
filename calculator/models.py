from django.db import models


class Customers(models.Model):
    """Заказчики"""
    last_name = models.CharField("Фамилия", max_length=255)
    first_name = models.CharField("Имя", max_length=255)
    second_name = models.CharField("Отчество", max_length=255, blank=True)
    phone = models.CharField('Телефон', max_length=10)
    email = models.EmailField('E-mail', max_length=255, blank=True)
    adress = models.CharField('Адрес', max_length=1000, blank=True)
    building_adress = models.CharField('Адрес строительства дома', max_length=1000, blank=True)


class Estimate(models.Model):
    """Смета"""
    manager_id = models.ForeignKey('profiles.User', verbose_name='Менеджер', on_delete=models.PROTECT)
    customer_id = models.ForeignKey(Customers, verbose_name='Заказчик', on_delete=models.PROTECT)
    title = models.CharField('Название', max_length=255)
    created_date = models.DateField('Дата создания', auto_now_add=True)
    box_calculation_id = models.ForeignKey('BoxСalculations', verbose_name='Расчет коробки', on_delete=models.PROTECT, blank=True)
    foundation_calculation_id = models.ForeignKey('FoundationСalculations', verbose_name='Расчет фундамента', on_delete=models.PROTECT, blank=True)
    roof_calculation_id = models.ForeignKey('RoofCalculations', verbose_name='Расчет крыши', on_delete=models.PROTECT, blank=True)
    estimate_state_id = models.ForeignKey('States', verbose_name='Cтатус сметы', on_delete=models.PROTECT)


class States(models.Model):
    """Статус сметы"""
    title = models.CharField('Название статуса', max_length=255)


class Materials(models.Model):
    """Материалы"""
    materials_type_id = models.ForeignKey('MaterialsType', verbose_name='Тип материала', on_delete=models.PROTECT)
    measurement_unit_id = models.ForeignKey('MeasurementUnits', verbose_name='Единицы измерения', on_delete=models.PROTECT)


class MeasurementUnits(models.Model):
    """Единица измерения"""
    measurement_units_name = models.CharField('Наименование единицы измерения', max_length=20)


class MaterialsType(models.Model):
    """Тип материала"""
    description = models.CharField('Описание', max_length=255)


class PriceLists(models.Model):
    """Прайс-лист"""
    material_id = models.ForeignKey(Materials, verbose_name='Материал', on_delete=models.PROTECT)
    date = models.DateField('Дата')
    purchase_price = models.DecimalField('Цена закупки', max_digits=11, decimal_places=2)
    selling_price = models.DecimalField('Цена продажи', max_digits=11, decimal_places=2)


class BoxСalculations(models.Model):
    """Расчет коробки"""
    price_list = models.ForeignKey(PriceLists, verbose_name='Прайс-лист', on_delete=models.CASCADE)


class FoundationСalculations(models.Model):
    """Расчет фундамента"""
    price_list = models.ForeignKey(PriceLists, verbose_name='Прайс-лист', on_delete=models.CASCADE)


class RoofCalculations(models.Model):
    """Расчет крыши"""
    price_list = models.ForeignKey(PriceLists, verbose_name='Прайс-лист', on_delete=models.CASCADE)




























