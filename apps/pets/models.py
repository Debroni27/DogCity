
from django.contrib.auth import get_user_model
from django.db import models

from core_helpers.models import BaseModel


User = get_user_model()


class Passport(BaseModel):
    issuing_department = models.TextField('Отдел выдачи', max_length=2048)

    class Meta:
        verbose_name = 'Паспорт'
        verbose_name_plural = 'Паспорта'


class Certificate(BaseModel):

    TYPE = (
        ('F', 'Full',),
        ('P', 'Partial')
    )

    name = models.CharField('Название', max_length=256, blank=True)
    type_of = models.CharField('Тип', max_length=1, choices=TYPE, default='F')
    licence = models.CharField('Лицензия', max_length=256)

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        return self.name


class Pet(BaseModel):

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    name = models.CharField('имя питомца', max_length=256, blank=True)
    color = models.CharField('окрас', max_length=256, blank=True)
    age = models.PositiveIntegerField('возраст')
    sex = models.CharField('пол питомца', max_length=1, choices=GENDER)
    owner = models.ForeignKey(
        User,
        related_name='pet_owner',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    vaccination_certificate = models.ForeignKey(
        Certificate,
        related_name='pet_certificate',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    passport = models.ForeignKey(
        Passport,
        related_name='pet_passport',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'

    def __str__(self):
        return self.name
