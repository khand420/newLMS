
# Register your models here.
from django.contrib import admin
from .models import UserDetails, Department, Industry

# Register your models here.
admin.site.register(UserDetails)
admin.site.register(Department)
admin.site.register(Industry)



# class ProductIndex(admin.ModelAdmin):
#     list_display = ('name','status')