from django.contrib import admin
from .models import Location

# Register your models here.
#admin.site.register(Product)
@admin.register(Location)

class LocationIndex(admin.ModelAdmin):
    list_display = ('name','status')
    exclude = ('created_by','updated_by')