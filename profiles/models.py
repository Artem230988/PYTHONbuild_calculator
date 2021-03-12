from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(
        verbose_name='Фотография',
        upload_to='photos/%Y/%m/%d/'
    )
    second_name = models.CharField(
        verbose_name='Отчество',
        max_length=50
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=20)
    current_employee = models.BooleanField(
        verbose_name='Действующий сотрудник',
        default=True
    )
