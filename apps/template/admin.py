from django.contrib import admin
from .models import Template

# Register your models here.
#admin.site.register(Product)
@admin.register(Template)

class TemplateIndex(admin.ModelAdmin):
    list_display = ('name','type')
