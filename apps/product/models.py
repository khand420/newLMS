from django.db import models
from .utils import Status
from django.conf import settings
# Create your models here.
class Product(models.Model):
    status = models.CharField(max_length=255,choices=Status.choices(),default=Status.active,unique=False)
    name = models.CharField(max_length=255, null= True, unique= False)
    description = models.CharField(max_length=255,null=True, blank=True,unique=False)
    product_code = models.CharField(max_length=70,blank=False, null= True, unique= False)
    price = models.DecimalField(max_digits = 15,decimal_places = 2, null= True, unique= False)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)

    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    conversion_days = models.CharField(max_length=255, null= True, unique= False)
    # conversion_days = models.CharField(max_length= 255, null= True, blank= False, unique= False)

    client = models.CharField(max_length=255, null= True, unique= False)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

  
    def __str__(self):
      return self.name