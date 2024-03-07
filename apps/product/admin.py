from django.contrib import admin
from .models import Product

# Register your models here.
#admin.site.register(Product)
@admin.register(Product)

class ProductIndex(admin.ModelAdmin):
    list_display = ('name','status')