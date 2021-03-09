from django.contrib import admin
from .models import *


class CustomersAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'second_name', 'phone', 'manager',)
    search_fields = ('last_name', 'first_name',)
    list_filter = ('manager',)
    empty_value_display = '-пусто-'


class CalculationAdmin(admin.ModelAdmin):
    list_display = ('manager', 'customer', 'adress_object_construction',
                    'title', 'created_date', 'state_calculation',)
    search_fields = ('adress_object_construction', 'title')
    list_filter = ('manager', 'state_calculation')
    date_hierarchy = 'created_date'
    empty_value_display = '-пусто-'


class CalculationStateAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ResultsAdmin(admin.ModelAdmin):
    list_display = ('specific_material', 'amount', 'price', 'full_price',)
    list_filter = ('specific_material', )
    empty_value_display = '-пусто-'


class MaterialsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class MeasurementUnitAdmin(admin.ModelAdmin):
    list_display = ('measurement_unit',)


class SpecificMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-пусто-'


class PriceListAdmin(admin.ModelAdmin):
    list_display = ('specific_material', 'data', 'purchase_price', 'selling_price')
    date_hierarchy = 'data'
    empty_value_display = '-пусто-'


class OpeningsAdmin(admin.ModelAdmin):
    list_display = ('type', 'wigth', 'height', 'count')
    empty_value_display = '-пусто-'


class FrameOpeningsAdmin(admin.ModelAdmin):
    list_display = ('structural_element_frame', 'openings',)
    empty_value_display = '-пусто-'


admin.site.register(Customers, CustomersAdmin)
admin.site.register(Calculation, CalculationAdmin)
admin.site.register(CalculationState, CalculationStateAdmin)
admin.site.register(Results, ResultsAdmin)
admin.site.register(Materials, MaterialsAdmin)
admin.site.register(MeasurementUnit, MeasurementUnitAdmin)
admin.site.register(SpecificMaterial, SpecificMaterialAdmin)
admin.site.register(PriceList, PriceListAdmin)
admin.site.register(StructuralElementFrame)
admin.site.register(Openings, OpeningsAdmin)
admin.site.register(FrameOpenings, FrameOpeningsAdmin)
