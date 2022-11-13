import uuid

from django.db import models

from apps.users.models import User
from core_helpers.models import BaseModel


class Passport(BaseModel):
    issuing_department = models.TextField('Отдел выдачи', max_length=2048)

    class Meta:
        verbose_name = 'Паспорт'
        verbose_name_plural = 'Паспорта'


class Certificate(BaseModel):

    TYPE = (
        'F', 'Full',
        'P', 'Partial'
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
    owner = models.ForeignKey(User, related_name='владелец питомца', on_delete=models.SET_NULL)
    vaccination_certificate = models.ForeignKey(Certificate, related_name='сертификат', on_delete=models.SET_NULL)
    passport = models.ForeignKey(Passport, related_name='паспорт', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'

    def __str__(self):
        return self.name
