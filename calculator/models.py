from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Customers(models.Model):
    """Заказчики"""
    last_name = models.CharField("Фамилия", max_length=255)
    first_name = models.CharField("Имя", max_length=255)
    second_name = models.CharField("Отчество", max_length=255, blank=True)
    phone = models.CharField('Телефон', max_length=10)
    email = models.EmailField('E-mail', max_length=255, blank=True)
    adress = models.CharField('Адрес', max_length=1000, blank=True)
    manager = models.ForeignKey(User, verbose_name='Менеджер', on_delete=models.PROTECT, related_name='customers')

#
# class Calculation(models.Model):
#     """Расчет"""
#     manager_id = models.ForeignKey('profiles.User', verbose_name='Менеджер', on_delete=models.PROTECT)
#     customer_id = models.ForeignKey(Customers, verbose_name='Заказчик', on_delete=models.PROTECT)
#     adress_object_construction = models.CharField('Адрес строительства', max_length=1000, blank=True)
#     title = models.CharField('Название', max_length=255)
#     created_date = models.DateField('Дата создания', auto_now_add=True)
#     result_id = models.ForeignKey('Results', verbose_name='Результаты', on_delete=models.PROTECT)
#     сalculation_state_id = models.ForeignKey('CalculationState', verbose_name='Статус расчета', on_delete=models.PROTECT)
#
#
# class CalculationState(models.Model):
#     """Статус расчета"""
#     title = models.CharField('Название статуса', max_length=255)
#
#
# class Results(models.Model):
#     """Результаты"""
#     material_id = models.ForeignKey('Materials', verbose_name='Материал', on_delete=models.PROTECT)
#     amount = models.PositiveIntegerField('Количество')
    # price
    # measurement_unit
    # full_price


























