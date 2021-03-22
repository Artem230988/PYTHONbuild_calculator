from decimal import Decimal
from math import ceil

from django.shortcuts import get_object_or_404

from calculator.models import *

LENS_PLANKS_WALLS = Decimal('3')
LENS_PLANKS_BASE_AREA = Decimal('6')
THICKNESS_PLANKS = Decimal('0.05')
MM_IN_METER = Decimal('1000')
PROCENT_COVERING = Decimal('1.15')
PROCENT_INSULATION = Decimal('1.1')
STEP_PLANKS_BASE_AREA = Decimal('0.7')


def calculate_frame(frame):
    """Расчет материала для конструктивного элемента каркас."""
    # Коэффициент перекрытия, если первый этаж то 1, если иной то 2
    if frame.number_of_floors == 1:
        K_BASE_AREA = 2
    else:
        K_BASE_AREA = 1

    # Общие данные, периметр внешних и внутренних стен
    square_external_walls = (
            frame.perimeter_of_external_walls *
            frame.height_of_one_floor
    )
    square_internal_walls = (
            frame.internal_wall_length *
            frame.height_of_one_floor
    )

    external_walls = f'Внешние стены'
    # Количество досок на внешние стойки
    count_planks_external_walls = ceil(
        frame.perimeter_of_external_walls / frame.step_of_racks + 1
    )
    # Количество досок для основания
    count_planks_floor = ceil(
        frame.perimeter_of_external_walls * K_BASE_AREA / LENS_PLANKS_WALLS
    )
    # Подсчет количества досок для проемов и их площадь
    openings_all = Opening.objects.filter(frame=frame)
    count_planks_openings_external = 0
    square_openings = 0
    for opening in openings_all:
        if opening.type != 'Дверные проемы внутренние':
            count_planks_openings_external += (
                    (opening.wigth + opening.height) * 2 *
                    opening.count)
            square_openings += opening.wigth * opening.height * opening.count

    # Общее количество досок на внешние стены
    total_planks_external = (
            count_planks_external_walls + count_planks_floor +
            ceil(count_planks_openings_external / LENS_PLANKS_WALLS)
    )
    # Ширина доски на внешние стены
    width_plank_external_walls = frame.external_wall_thickness / MM_IN_METER
    # Объем досок на внешние стены
    volume_plank_external_walls = (
            total_planks_external *
            width_plank_external_walls *
            LENS_PLANKS_WALLS *
            THICKNESS_PLANKS
    )
    # площадь ОСБ на внешние стены
    square_osb_external = (
            square_external_walls * K_BASE_AREA * PROCENT_COVERING
    )
    # Площадь парогидроизоляции на внешние стены
    square_steam_waterproofing_external = (
            square_external_walls * PROCENT_COVERING
    )
    # Площадь ветрозащиты на внешние стены
    square_windscreen_external = square_steam_waterproofing_external
    # Площадь утеплителя на внешние стены
    square_insulation_external_walls = (
            square_external_walls * PROCENT_INSULATION - square_openings
    )
    # Толщина утеплителя
    thickness_insulation_external = (
            frame.external_wall_thickness / MM_IN_METER
    )
    # Объем утеплителя на внешние стены
    volume_insulation_external = (
            square_insulation_external_walls * thickness_insulation_external
    )

    internal_walls = f'Внутренние стены'
    # Количество досок на внутренние стойки
    count_planks_internal_walls = ceil(
        frame.internal_wall_length / frame.step_of_racks
    )
    # Подсчет количества досок для проемов
    count_planks_openings_internal = 0
    for opening in openings_all:
        if opening.type == 'Дверные проемы внутренние':
            count_planks_openings_internal += (
                    (opening.wigth + opening.height) * 2 *
                    opening.count)
    # Общее количество досок на внутренние стены
    total_planks_internal = (
            count_planks_internal_walls +
            ceil(count_planks_openings_internal / LENS_PLANKS_WALLS)
    )
    # Ширина доски на внутренние стойки
    wigth_plank_internal_walls = frame.internal_wall_thickness / MM_IN_METER
    # Объем досок на внутренние стойки
    volume_plank_internal_walls = (
            total_planks_internal *
            wigth_plank_internal_walls *
            LENS_PLANKS_WALLS *
            THICKNESS_PLANKS
    )
    # Площадь ОСБ на внутренние стены
    square_osb_internal = square_internal_walls * 2 * PROCENT_COVERING

    base_area = f'Перекрытия'
    # Кол-во балок перекрытий
    count_planks_base_area = ceil(
        frame.base_area * STEP_PLANKS_BASE_AREA
    )
    # Ширина доски на балки перекрытия
    wigth_plank_base_area = frame.overlap_thickness / MM_IN_METER
    # Объем досок на перекрытия
    volume_plank_base_area = (
            count_planks_base_area *
            wigth_plank_base_area *
            LENS_PLANKS_BASE_AREA *
            THICKNESS_PLANKS
    )
    # площадь ОСБ на перекрытия
    square_osb_base_area = (
            frame.base_area * K_BASE_AREA * 2 * PROCENT_COVERING
    )
    # Площадь парогидроизоляции на перекрытия
    square_steam_waterproofing_base_area = frame.base_area * PROCENT_COVERING
    # Площадь ветрозащиты на перекрытия
    square_windscreen_base_area = square_steam_waterproofing_base_area
    # Площадь утеплителя перекрытия на перекрытия
    square_insulation_base_area = (
            frame.base_area * PROCENT_INSULATION * K_BASE_AREA
    )
    # Толщина утеплителя на перекрытия
    thickness_insulation_base_area = frame.overlap_thickness / MM_IN_METER
    # Объем утеплителя на перекрытия
    volume_insulation_base_area = (
            square_insulation_base_area * thickness_insulation_base_area
    )

    results = Result.objects.filter(
        calculation=frame.calculations,
        floor=frame.number_of_floors
    )
    for i in results:
        i.delete()

    name_all = [
        external_walls,
        internal_walls,
        base_area
    ]
    # Сохранение результатов досок
    material_plank = get_object_or_404(
        Material,
        name='Доска'
    )
    thickness = [
        frame.external_wall_thickness,
        frame.internal_wall_thickness,
        frame.overlap_thickness
    ]
    volume_plank = [
        volume_plank_external_walls,
        volume_plank_internal_walls,
        volume_plank_base_area
    ]
    for i in range(len(thickness)):
        if name_all[i] != base_area:
            planks_mat = get_object_or_404(
                SpecificMaterial,
                material=material_plank,
                width=thickness[i],
                thickness=THICKNESS_PLANKS * MM_IN_METER,
                length=LENS_PLANKS_WALLS * MM_IN_METER
            )
        else:
            planks_mat = get_object_or_404(
                SpecificMaterial,
                material=material_plank,
                width=thickness[i],
                thickness=THICKNESS_PLANKS * MM_IN_METER,
                length=LENS_PLANKS_BASE_AREA * MM_IN_METER
            )
        price_list_planks = PriceList.objects.filter(
            specific_material=planks_mat
        )[0]
        result_planks = Result.objects.create(
            name=name_all[i],
            calculation=frame.calculations,
            specific_material=planks_mat,
            amount=volume_plank[i],
            price=price_list_planks,
            floor=frame.number_of_floors
        )
        result_planks.save()

    # Сохранение результатов ОСБ
    material_osb = get_object_or_404(
        Material,
        name='OSB'
    )
    osb = [
        frame.OSB_for_external_walls,
        frame.OSB_for_interior_walls,
        frame.OSB_for_base_area
    ]
    square_osb = [
        square_osb_external,
        square_osb_internal,
        square_osb_base_area
    ]
    for j in range(len(osb)):
        osb_mat = get_object_or_404(
            SpecificMaterial,
            material=material_osb,
            name=osb[j]
        )
        price_list_osb = PriceList.objects.filter(
            specific_material=osb_mat
        )[0]
        result_osb = Result.objects.create(
            name=name_all[j],
            calculation=frame.calculations,
            specific_material=osb_mat,
            amount=square_osb[j],
            price=price_list_osb,
            floor=frame.number_of_floors
        )
        result_osb.save()

    name_two = [
        external_walls,
        base_area
    ]
    # Сохранение результатов парогидроизоляции
    material_steam_waterproofing = get_object_or_404(
        Material,
        name='Парогидроизоляция'
    )
    steam_waterproofing = [
        frame.steam_waterproofing_external_walls,
        frame.steam_waterproofing_base_area
    ]
    square_steam_waterproofing = [
        square_steam_waterproofing_external,
        square_steam_waterproofing_base_area
    ]
    for w in range(len(steam_waterproofing)):
        steam_waterproofing_mat = get_object_or_404(
            SpecificMaterial,
            material=material_steam_waterproofing,
            name=steam_waterproofing[w]
        )
        price_list_steam_waterproofing_mat = PriceList.objects.filter(
            specific_material=steam_waterproofing_mat
        )[0]
        result_steam_waterproofing = Result.objects.create(
            name=name_two[w],
            calculation=frame.calculations,
            specific_material=steam_waterproofing_mat,
            amount=square_steam_waterproofing[w],
            price=price_list_steam_waterproofing_mat,
            floor=frame.number_of_floors
        )
        result_steam_waterproofing.save()

    # Сохранение результатов ветрозащиты
    material_windscreen = get_object_or_404(
        Material,
        name='Ветрозащита'
    )
    windscreen = [
        frame.windscreen_external_walls,
        frame.windscreen_base_area
    ]
    square_windscreen = [
        square_windscreen_external,
        square_windscreen_base_area
    ]
    for v in range(len(windscreen)):
        windscreen_mat = get_object_or_404(
            SpecificMaterial,
            material=material_windscreen,
            name=windscreen[v]
        )
        price_list_windscreen_mat = PriceList.objects.filter(
            specific_material=windscreen_mat
        )[0]
        result_windscreen = Result.objects.create(
            name=name_two[v],
            calculation=frame.calculations,
            specific_material=windscreen_mat,
            amount=square_windscreen[v],
            price=price_list_windscreen_mat,
            floor=frame.number_of_floors
        )
        result_windscreen.save()

    # Сохранение результатов утеплителя
    material_insulation = get_object_or_404(
        Material,
        name='Утеплитель'
    )
    insulation = [
        frame.insulation_external_walls,
        frame.insulation_base_area
    ]
    volume_insulation = [
        volume_insulation_external,
        volume_insulation_base_area
    ]
    for s in range(len(insulation)):
        insulation_mat = get_object_or_404(
            SpecificMaterial,
            material=material_insulation,
            name=insulation[s]
        )
        price_list_insulation_mat = PriceList.objects.filter(
            specific_material=insulation_mat
        )[0]
        result_insulation = Result.objects.create(
            name=name_two[s],
            calculation=frame.calculations,
            specific_material=insulation_mat,
            amount=volume_insulation[s],
            price=price_list_insulation_mat,
            floor=frame.number_of_floors
        )
        result_insulation.save()
