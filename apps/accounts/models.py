from django.db import models

from pets.models import Pet
from core_helpers.models import BaseModel, USER


class Account(BaseModel):
    """ Dashboard для главной страницы"""
    owner = models.OneToOneField(
        USER,
        verbose_name='Пользователь',
        related_name='account_owner',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    pet = models.OneToOneField(
        Pet,
        verbose_name='Питомец',
        related_name='account_pet',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    # tender_history = models.OneToOneField(
    #     'Tender',
    #     verbose_name='История услуг',
    #     related_name='account_tender_history',
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True
    # )
    # order_history = models.OneToOneField(
    #     'Order',
    #     verbose_name='История заказов',
    #     related_name='account_tender_history',
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True
    # )
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.owner.name


