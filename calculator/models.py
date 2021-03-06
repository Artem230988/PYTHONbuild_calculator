from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Customers(models.Model):
    """Заказчики."""
    last_name = models.CharField(
        "Фамилия",
        max_length=255
    )
    first_name = models.CharField(
        "Имя",
        max_length=255
    )
    second_name = models.CharField(
        "Отчество",
        max_length=255,
        blank=True
    )
    phone = models.CharField(
        'Телефон',
        max_length=10
    )
    email = models.EmailField(
        'E-mail',
        max_length=255,
        blank=True
    )
    adress = models.CharField(
        'Адрес',
        max_length=1000,
        blank=True
    )
    manager = models.ForeignKey(
        User,
        verbose_name='Менеджер',
        on_delete=models.PROTECT,
        related_name='customers'
    )

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'


class Calculation(models.Model):
    """Расчет."""
    manager = models.ForeignKey(
        User,
        verbose_name='Менеджер',
        on_delete=models.PROTECT
    )
    customer = models.ForeignKey(Customers, verbose_name='Заказчик',
                                    on_delete=models.PROTECT)
    adress_object_construction = models.CharField('Адрес строительства',
                                                  max_length=1000, blank=True)
    title = models.CharField('Название', max_length=255)
    created_date = models.DateField('Дата создания', auto_now_add=True)
    result_id = models.ForeignKey('Results', verbose_name='Результаты',
                                  on_delete=models.PROTECT)
    state_calculation = models.ForeignKey('CalculationState',
                                             verbose_name='Статус расчета',
                                             on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Расчет'
        verbose_name_plural = 'Расчеты'


class CalculationState(models.Model):
    """Статус расчета."""
    title = models.CharField('Название статуса', max_length=255)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Results(models.Model):
    """Результаты."""
    material = models.ForeignKey('Materials',
                                    verbose_name='Материал',
                                    on_delete=models.PROTECT)
    amount = models.PositiveIntegerField('Количество')
    price = models.ForeignKey('PriceList',
                              verbose_name='Прайс лист',
                              on_delete=models.PROTECT)

    @property
    def full_price(self):
        full_price = self.price.price_sell * self.amount
        return full_price

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'


class Materials(models.Model):
    """Материалы."""
    name = models.CharField(max_length=50, verbose_name='Название')
    materials_type = models.ForeignKey('MaterialsType',
                                          verbose_name='Тип материала',
                                          on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class MaterialsType(models.Model):
    """Типы материалов."""
    name = models.CharField(max_length=50, verbose_name='Название')
    measurement_unit = models.CharField(max_length=20)
    materials_parameters = models.ForeignKey('MaterialsParameter',
                                                verbose_name='Параметры Материала',
                                                on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Тип материала'
        verbose_name_plural = 'Типы материалов'


class MaterialsParameter(models.Model):
    """Параметры материала."""
    lenght = models.DecimalField(verbose_name='Длина',
                                 decimal_places=2,
                                 max_digits=10)
    wedth = models.DecimalField(verbose_name='Ширина',
                                decimal_places=2,
                                max_digits=10)
    thickness = models.DecimalField(verbose_name='Толщина',
                                    decimal_places=2,
                                    max_digits=10)
    volume = models.DecimalField(verbose_name='Объем',
                                 decimal_places=2,
                                 max_digits=10)

    class Meta:
        verbose_name = 'Параметры материала'
        verbose_name_plural = 'Параметры материала'


class PriceList(models.Model):
    """Прайс лист."""
    material = models.ForeignKey('Materials',
                                    verbose_name='Материал',
                                    on_delete=models.PROTECT)
    data = models.DateField(verbose_name='Дата',
                            auto_now_add=True)
    purchase_price = models.DecimalField(verbose_name='Цена закупки',
                                         decimal_places=2,
                                         max_digits=10)
    selling_price = models.DecimalField(verbose_name='Цена продажи',
                                        decimal_places=2,
                                        max_digits=10)

    class Meta:
        verbose_name = 'Прайс лист'
        verbose_name_plural = 'Прайс листы'


class StructuralElementFrame(models.Model):
    """Конструктивный элемент каркас."""
    calculations = models.ForeignKey('Calculation',
                                     verbose_name='Расчет',
                                     on_delete=models.PROTECT)
    perimeter_of_external_walls = models.DecimalField(
        verbose_name='Периметр внешних стен',
        decimal_places=2,
        max_digits=10)
    base_area = models.DecimalField(verbose_name='Площадь основания',
                                    decimal_places=2,
                                    max_digits=10)
    external_wall_thickness = models.DecimalField(
        verbose_name='Толщина внешних стен',
        decimal_places=2,
        max_digits=10)
    internal_wall_length = models.DecimalField(
        verbose_name='Длина внутренних стен',
        decimal_places=2,
        max_digits=10)
    internal_wall_thickness = models.DecimalField(
        verbose_name='Толщина внутренних стен',
        decimal_places=2,
        max_digits=10)
    number_of_floors = models.IntegerField(verbose_name='Количество этажей')
    height_of_one_floor = models.DecimalField(
        verbose_name='Высота одного этажа',
        decimal_places=2,
        max_digits=10)
    overlap_thickness = models.DecimalField(verbose_name='Толщина перекрытия',
                                            decimal_places=2,
                                            max_digits=10)
    OSB = models.DecimalField(verbose_name='ОСБ',
                              decimal_places=2,
                              max_digits=10)
    steam_waterproofing = models.DecimalField(
        verbose_name='Парогидроизоляция',
        decimal_places=2,
        max_digits=10)
    windscreen = models.DecimalField(verbose_name='Ветрозащита',
                                     decimal_places=2,
                                     max_digits=10)
    insulation = models.DecimalField(verbose_name='Утеплитель',
                                     decimal_places=2,
                                     max_digits=10)
    OSB_for_interior_walls = models.DecimalField(
        verbose_name='ОСБ для внутренних стен',
        decimal_places=2,
        max_digits=10)
    OSB_for_sub_floor = models.DecimalField(
        verbose_name='ОСБ для чернового пола',
        decimal_places=2,
        max_digits=10)
    OSB_for_ceiling = models.DecimalField(verbose_name='ОСБ для потолка',
                                          decimal_places=2,
                                          max_digits=10)
    step_of_racks = models.DecimalField(verbose_name='Шаг стоек',
                                        decimal_places=2,
                                        max_digits=10)

    class Meta:
        verbose_name = 'Конструктивный элемент каркас.'
        verbose_name_plural = 'Конструктивный элемент каркас.'
