import uuid

from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. "
        "Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        'Номер телефона',
        validators=[phone_regex],
        max_length=17, blank=True
    )
    info = models.CharField(
        'Информация о себе',
        max_length=256,
        blank=True,
        null=True
    )
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name

