from decimal import Decimal
from math import ceil

from django.shortcuts import get_object_or_404

from calculator.models import *


def calculate_frame(frame):
    # Общие данные
    square_external_walls = (
            frame.perimeter_of_external_walls *
            frame.height_of_one_floor *
            frame.number_of_floors
    )
    square_internal_walls = (
            frame.internal_wall_length *
            frame.height_of_one_floor *
            frame.number_of_floors
    )

    external_walls = 'Внешние стены'
    count_planks_external_walls = ceil(frame.perimeter_of_external_walls /
                                       frame.step_of_racks + 1)
    count_planks_floor = ceil(frame.perimeter_of_external_walls * 2 / 3)
    openings_all = frame.openings.all()
    count_planks_openings_external = 0
    square_openings = 0
    for opening in openings_all:
        if opening.type != 'Дверные проемы внутренние':
            count_planks_openings_external += (
                    (opening.wigth + opening.height) * 2 *
                    opening.count)
            square_openings += opening.wigth * opening.height * opening.count
    total_planks_external = (
            count_planks_external_walls + count_planks_floor +
            ceil(count_planks_openings_external / 3))
    wigth_plank_external_walls = frame.external_wall_thickness / 1000
    volume_plank_external_walls = (total_planks_external *
                                   wigth_plank_external_walls *
                                   3 * Decimal('0.05'))
    square_osb_external = square_external_walls * 2 * Decimal('1.15')
    square_steam_waterproofing_external = square_external_walls * Decimal(
        '1.15')
    square_windscreen_external = square_steam_waterproofing_external
    square_insulation_external_walls = (square_external_walls *
                                        Decimal('1.1') - square_openings)
    thickness_insulation_external = frame.external_wall_thickness / 1000
    volume_insulation_external = (square_insulation_external_walls *
                                  thickness_insulation_external)

    internal_walls = 'Внутренние стены'
    count_planks_internal_walls = ceil(frame.internal_wall_length /
                                       frame.step_of_racks)
    count_planks_openings_internal = 0
    for opening in openings_all:
        if opening.type == 'Дверные проемы внутренние':
            count_planks_openings_internal += (
                    (opening.wigth + opening.height) * 2 *
                    opening.count)
    total_planks_internal = (count_planks_internal_walls +
                             ceil(count_planks_openings_internal / 3))
    wigth_plank_internal_walls = frame.internal_wall_thickness / 1000
    volume_plank_internal_walls = (total_planks_internal *
                                   wigth_plank_internal_walls *
                                   3 * Decimal('0.05'))
    square_osb_internal = square_internal_walls * 2 * Decimal('1.15')

    base_area = 'Перекрытия'
    count_planks_base_area = ceil(frame.base_area * Decimal('0.7'))
    wigth_plank_base_area = frame.overlap_thickness / 1000
    volume_plank_base_area = (count_planks_base_area *
                              wigth_plank_base_area * 6 * Decimal('0.05'))
    square_osb_base_area = frame.base_area * 2 * 2 * Decimal('1.15')
    square_steam_waterproofing_base_area = frame.base_area * Decimal('1.15')
    square_windscreen_base_area = square_steam_waterproofing_base_area
    square_insulation_base_area = frame.base_area * Decimal('1.1') * 2
    thickness_insulation_base_area = frame.overlap_thickness / 1000
    volume_insulation_base_area = (square_insulation_base_area *
                                   thickness_insulation_base_area)

    # material = get_object_or_404(
    #     Materials,
    #     materials_type__materials_parameters__lenght=3000,
    #     materials_type__materials_parameters__wedth=int(frame.external_wall_thickness),)
    # price_list = get_object_or_404(PriceList, material=material)
    # result_external_walls = Results.objects.create(
    #     name=external_walls,
    #     calculation=frame.calculations,
    #     material=material,
    #     amount=volume_plank_external_walls,
    #     price=price_list
    # )
    # result_external_walls.save()

    print('\n', volume_plank_external_walls, '\n',
          square_osb_external, '\n',
          square_windscreen_external, '\n',
          volume_insulation_external, '\n',
          volume_plank_internal_walls, '\n',
          square_osb_internal, '\n',
          volume_plank_base_area, '\n',
          square_osb_base_area, '\n',
          square_windscreen_base_area, '\n',
          volume_insulation_base_area, '\n', )
