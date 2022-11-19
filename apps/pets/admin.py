
from django.contrib import admin

from .models import Pet, Passport, Certificate
from core_helpers.utils import CachingPaginator


admin.site.register(Passport)
admin.site.register(Certificate)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = (
            'name',
            'color',
            'breed',
            'age',
            'sex',
            'owner',
            'vaccination_certificate',
            'passport'
    )
    list_per_page = 50
    list_display_links = ('name', )
    list_select_related = ['owner', 'vaccination_certificate', 'passport']

    show_full_result_count = False
    paginator = CachingPaginator
