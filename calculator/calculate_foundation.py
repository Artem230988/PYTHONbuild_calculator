import math

from django.shortcuts import get_object_or_404
from .models import *


def calculate_foundation(data, calculation_id):
    """Внесение в таблицы результаты данных по фундаменту"""
    perimeter_of_external_walls = data.perimeter_of_external_walls
    internal_wall_length = data.internal_wall_length
    concrete_pile = data.concrete_pile
    concrete = data.concrete

    results = Result.objects.filter(
        calculation=calculation_id,
    )
    for i in results:
        i.delete()

    """Результат для количества бетонных свай"""
    Result.objects.create(
        calculation=Calculation.objects.get(pk=calculation_id),
        name='Фундамент',
        specific_material=get_object_or_404(SpecificMaterial, name=concrete_pile),
        price=PriceList.objects.filter(specific_material=get_object_or_404(SpecificMaterial, name=concrete_pile))[0],
        amount=((perimeter_of_external_walls + internal_wall_length + 1) // 2)
    )

    """Результат для количества бетона"""
    Result.objects.create(
        calculation=Calculation.objects.get(pk=calculation_id),
        name='Фундамент',
        specific_material=get_object_or_404(SpecificMaterial, name=concrete),
        price=PriceList.objects.filter(specific_material=get_object_or_404(SpecificMaterial, name=concrete))[0],
        amount=((perimeter_of_external_walls + internal_wall_length) * 3 * 4 * 15 / 10000)
    )
    """Результат для количества арматуры 14 мм"""
    Result.objects.create(
        calculation=Calculation.objects.get(pk=calculation_id),
        name='Фундамент',
        specific_material=get_object_or_404(SpecificMaterial, name="Арматура 14 мм"),
        price=PriceList.objects.filter(specific_material=get_object_or_404(SpecificMaterial, name="Арматура 14 мм"))[0],
        amount=math.ceil((perimeter_of_external_walls + internal_wall_length) * 4 / 6)
    )
    """Результат для количества арматуры 8 мм"""
    Result.objects.create(
        calculation=Calculation.objects.get(pk=calculation_id),
        name='Фундамент',
        specific_material=get_object_or_404(SpecificMaterial, name="Арматура 8 мм"),
        price=PriceList.objects.filter(specific_material=get_object_or_404(SpecificMaterial, name="Арматура 8 мм"))[0],
        amount=math.ceil((perimeter_of_external_walls + internal_wall_length) * 10 / 18)
    )
    """Результат для доски 30*100*3000"""
    Result.objects.create(
        calculation=Calculation.objects.get(pk=calculation_id),
        name='Фундамент',
        specific_material=get_object_or_404(SpecificMaterial, name="Доска 30*100*3000"),
        price=PriceList.objects.filter(specific_material=get_object_or_404(SpecificMaterial, name="Доска 30*100*3000"))[0],
        amount=((perimeter_of_external_walls + internal_wall_length) * 3 / 100)
    )
    """Результат для Брус 50*50*3000"""
    Result.objects.create(
        calculation=Calculation.objects.get(pk=calculation_id),
        name='Фундамент',
        specific_material=get_object_or_404(SpecificMaterial, name="Брус 50*50*3000"),
        price=PriceList.objects.filter(specific_material=get_object_or_404(SpecificMaterial, name="Брус 50*50*3000"))[0],
        amount=((perimeter_of_external_walls + internal_wall_length) * 25 / 7000)
    )