from django.contrib import admin
from .models import generalsettings
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter


# Register your models here.
#admin.site.register(generalsettings)
@admin.register(generalsettings)

class GeneralsettingsIndex(admin.ModelAdmin):
    list_display = ('meta_key','meta_value')