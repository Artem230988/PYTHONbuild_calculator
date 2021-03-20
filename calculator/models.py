from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Customers(models.Model):
    """Заказчики."""
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=255
    )
    second_name = models.CharField(
        verbose_name='Отчество',
        max_length=255,
        blank=True
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=20
    )
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=255,
        blank=True
    )
    adress = models.CharField(
        verbose_name='Адрес',
        max_length=1000,
        blank=True
    )
    manager = models.ForeignKey(
        User,
        verbose_name='Менеджер',
        on_delete=models.PROTECT,
        related_name='customers',
    )

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        name = f'{self.last_name} {self.first_name}'
        return name


class Calculation(models.Model):
    """Расчет."""
    manager = models.ForeignKey(
        User,
        verbose_name='Менеджер',
        on_delete=models.PROTECT,
        related_name='calculation',
    )
    customer = models.ForeignKey(
        Customers,
        verbose_name='Заказчик',
        on_delete=models.CASCADE,
        related_name='calculation',
    )
    adress_object_construction = models.CharField(
        'Адрес строительства',
        max_length=1000,
        blank=True
    )
    title = models.CharField(
        'Название',
        max_length=255
    )
    created_date = models.DateField(
        'Дата создания',
        auto_now_add=True
    )
    state_calculation = models.ForeignKey(
        'CalculationState',
        verbose_name='Статус расчета',
        on_delete=models.PROTECT,
        related_name='calculation',
    )

    class Meta:
        verbose_name = 'Расчет'
        verbose_name_plural = 'Расчеты'

    def __str__(self):
        return self.title


class CalculationState(models.Model):
    """Статус расчета."""
    title = models.CharField(
        'Название статуса',
        max_length=255
    )

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.title


class Result(models.Model):
    """Результат."""
    calculation = models.ForeignKey(
        Calculation,
        verbose_name='Расчет',
        on_delete=models.CASCADE,
        related_name='results',
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Часть здания',
        default='qwerty'
    )
    floor = models.IntegerField(
        verbose_name='Этаж',
        blank=True,
        null=True
    )
    specific_material = models.ForeignKey(
        'SpecificMaterial',
        verbose_name='Материал',
        on_delete=models.PROTECT,
        related_name='results',
    )
    amount = models.DecimalField(
        verbose_name='Количество',
        decimal_places=2,
        max_digits=10
    )
    price = models.ForeignKey(
        'PriceList',
        verbose_name='Прайс лист',
        on_delete=models.PROTECT,
        related_name='results',
    )

    @property
    def full_price(self):
        full_price = self.price.selling_price * self.amount
        return full_price

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

    def __str__(self):
        return self.name


class Material(models.Model):
    """Материал."""
    name = models.CharField(
        max_length=50,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return self.name


class SpecificMaterial(models.Model):
    """Характеристики материала."""
    name = models.CharField(
        max_length=50,
        verbose_name='Название материала'
    )
    material = models.ForeignKey(
        Material,
        verbose_name='Материал',
        on_delete=models.PROTECT,
        related_name='specific_materials'
    )
    measurement_unit = models.ForeignKey(
        'MeasurementUnit',
        verbose_name='Единица измерения',
        on_delete=models.PROTECT,
        related_name='specific_materials',
    )
    length = models.DecimalField(
        verbose_name='Длина',
        help_text='мм, если применимо к материалу',
        decimal_places=2,
        max_digits=10,
        blank=True, null=True
    )
    width = models.DecimalField(
        verbose_name='Ширина',
        help_text='мм, если применимо к материалу',
        decimal_places=2,
        max_digits=10,
        blank=True, null=True
    )
    thickness = models.DecimalField(
        verbose_name='Толщина',
        help_text='мм, если применимо к материалу',
        decimal_places=2,
        max_digits=10,
        blank=True, null=True
    )
    volume = models.DecimalField(
        verbose_name='Объем',
        help_text='м3, если применимо к материалу',
        decimal_places=2,
        max_digits=10,
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Характеристики материала'
        verbose_name_plural = 'Характеристики материала'

    def __str__(self):
        return self.name


class MeasurementUnit(models.Model):
    """Единицы измерений."""
    measurement_unit = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерений'

    def __str__(self):
        return self.measurement_unit


class PriceList(models.Model):
    """Прайс лист."""
    specific_material = models.ForeignKey(
        'SpecificMaterial',
        verbose_name='Материал',
        on_delete=models.PROTECT,
        related_name='price_list',
    )
    data = models.DateField(
        verbose_name='Дата',
        auto_now_add=True
    )
    purchase_price = models.DecimalField(
        verbose_name='Цена закупки',
        decimal_places=2,
        max_digits=10
    )
    selling_price = models.DecimalField(
        verbose_name='Цена продажи',
        decimal_places=2,
        max_digits=10
    )

    class Meta:
        verbose_name = 'Прайс лист'
        verbose_name_plural = 'Прайс листы'
        ordering = ['-data']

    def __str__(self):
        return self.specific_material.name


class StructuralElementFrame(models.Model):
    """Конструктивный элемент каркас."""
    calculations = models.ForeignKey(
        'Calculation',
        verbose_name='Расчет',
        on_delete=models.CASCADE,
        related_name='structural_element_frame',
    )
    number_of_floors = models.IntegerField(
        verbose_name='Количество этажей'
    )
    perimeter_of_external_walls = models.DecimalField(
        verbose_name='Периметр внешних стен',
        help_text='ед. измерения - метры (м)',
        decimal_places=2,
        max_digits=10
    )
    base_area = models.DecimalField(
        verbose_name='Площадь основания',
        help_text='ед. измерения - метры кубические (м2)',
        decimal_places=2,
        max_digits=10
    )
    external_wall_thickness = models.DecimalField(
        verbose_name='Толщина внешних стен',
        help_text='ед. измерения - миллиметры (мм)',
        decimal_places=2,
        max_digits=10
    )
    internal_wall_length = models.DecimalField(
        verbose_name='Длина внутренних стен',
        help_text='ед. измерения - метры (м)',
        decimal_places=2,
        max_digits=10
    )
    internal_wall_thickness = models.DecimalField(
        verbose_name='Толщина внутренних стен',
        help_text='ед. измерения - миллиметры (мм)',
        decimal_places=2,
        max_digits=10
    )
    height_of_one_floor = models.DecimalField(
        verbose_name='Высота одного этажа',
        help_text='ед. измерения - метры (м)',
        decimal_places=2,
        max_digits=10
    )
    overlap_thickness = models.DecimalField(
        verbose_name='Толщина перекрытия',
        help_text='ед. измерения - миллиметры (мм)',
        decimal_places=2,
        max_digits=10
    )
    steam_waterproofing_external_walls = models.CharField(
        verbose_name='Парогидроизоляция',
        help_text='Название материала',
        max_length=50,
    )
    steam_waterproofing_base_area = models.CharField(
        verbose_name='Парогидроизоляция',
        help_text='Название материала',
        max_length=50,
    )
    windscreen_external_walls = models.CharField(
        verbose_name='Ветрозащита',
        help_text='Название материала',
        max_length=50,
    )
    windscreen_base_area = models.CharField(
        verbose_name='Ветрозащита',
        help_text='Название материала',
        max_length=50,
    )
    insulation_external_walls = models.CharField(
        verbose_name='Утеплитель',
        help_text='Название материала',
        max_length=50,
    )
    insulation_base_area = models.CharField(
        verbose_name='Утеплитель',
        help_text='Название материала',
        max_length=50,
    )
    OSB_for_interior_walls = models.CharField(
        verbose_name='ОСБ для внутренних стен',
        help_text='Название материала',
        max_length=50,
    )
    OSB_for_external_walls = models.CharField(
        verbose_name='ОСБ для наружных стен',
        help_text='Название материала',
        max_length=50,
    )
    OSB_for_base_area = models.CharField(
        verbose_name='ОСБ для потолка и пола',
        help_text='Название материала',
        max_length=50,
    )
    step_of_racks = models.DecimalField(
        verbose_name='Шаг стоек',
        help_text='ед. измерения - метры (м)',
        decimal_places=2,
        max_digits=10
    )

    class Meta:
        verbose_name = 'Конструктивный элемент каркас'
        verbose_name_plural = 'Конструктивный элемент каркас'


class FrameOpening(models.Model):
    """Связь каркаса и проемов"""
    frame = models.ForeignKey(
        StructuralElementFrame,
        verbose_name='каркас',
        on_delete=models.CASCADE,
    )
    opening = models.ForeignKey(
        'Opening',
        verbose_name='проем',
        on_delete=models.CASCADE,
    )


class Opening(models.Model):
    """Проем."""
    frame = models.ForeignKey(
        StructuralElementFrame,
        verbose_name='каркас',
        on_delete=models.CASCADE,
        related_name='openings',
    )
    type = models.CharField(
        max_length=50,
        help_text=('Дверные проемы внутренние, Дверные проемы внешние '
                   'или Оконные проемы'),
        verbose_name='Тип проема'
    )
    wigth = models.DecimalField(
        verbose_name='Ширина',
        help_text='ед. измерения - метры (м)',
        decimal_places=2,
        max_digits=10
    )
    height = models.DecimalField(
        verbose_name='Высота',
        help_text='ед. измерения - метры (м)',
        decimal_places=2,
        max_digits=10
    )
    count = models.IntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Проем'
        verbose_name_plural = 'Проемы'

    def __str__(self):
        return f'{self.type} Ш{self.height}*В{self.height} кол-во {self.count}'


class StructuralElementFoundation(models.Model):
    """Конструктивный элемент фундамент."""
    calculation = models.ForeignKey(
        'Calculation',
        verbose_name='Расчет',
        on_delete=models.CASCADE,
        related_name='structural_element_foundation',
    )
    perimeter_of_external_walls = models.DecimalField(
        verbose_name='Периметр внешних стен',
        decimal_places=2,
        max_digits=10
    )
    internal_wall_length = models.DecimalField(
        verbose_name='Длина внутренних стен',
        decimal_places=2,
        max_digits=10
    )
    concrete_pile = models.CharField(
        verbose_name='Бетонная свая',
        max_length=100
    )
    concrete = models.CharField(
        verbose_name='Бетон',
        max_length=100
    )

    class Meta:
        verbose_name = 'Конструктивный элемент фундамент'
        verbose_name_plural = 'Конструктивный элемент фундамент'
