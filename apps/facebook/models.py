from django.db import models
from leads.utils import Status
import uuid, datetime
from django.conf import settings


class CommunicationFB(models.Model):
    communication_id = models.BigIntegerField(null=True, blank=True,unique=False)
    communication_name = models.CharField(max_length=255, null= True, unique= False) 

    fbpage_id = models.CharField(max_length=255, null= True, unique= False) 
    fbpage_name = models.CharField(max_length=255, null= True, unique= False) 

    fbform_id = models.CharField(max_length=255, null= True, unique= False) 
    fbform_name = models.CharField(max_length=255, null= True, unique= False) 


    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    created_by = models.BigIntegerField(null=True, blank=True,unique=False)

    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_by = models.BigIntegerField(null=True, blank=True,unique=False)

    status = models.CharField(max_length=255,choices=Status.choices(),default=Status.inactive,unique=False)
    client_id = models.CharField(max_length=255, null= True, unique= False) 
    
    def __str__(self):
      return self.communication_name
  
  

class ProductFB(models.Model):
    product_id = models.BigIntegerField(null=True, blank=True,unique=False)
    product_name = models.CharField(max_length=255, null= True, unique= False) 

    fbpage_id = models.CharField(max_length=255, null= True, unique= False) 
    fbpage_name = models.CharField(max_length=255, null= True, unique= False) 

    fbform_id = models.CharField(max_length=255, null= True, unique= False) 
    fbform_name = models.CharField(max_length=255, null= True, unique= False) 


    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    created_by = models.BigIntegerField(null=True, blank=True,unique=False)

    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_by = models.BigIntegerField(null=True, blank=True,unique=False)

    status = models.CharField(max_length=255,choices=Status.choices(),default=Status.inactive,unique=False)
    client_id = models.CharField(max_length=255, null= True, unique= False) 
    
    def __str__(self):
      return self.product_name
    

class TelecallerFB(models.Model):
    telecaller_id = models.BigIntegerField(null=True, blank=True,unique=False)
    telecaller_name = models.CharField(max_length=255, null= True, unique= False) 

    fbpage_id = models.CharField(max_length=255, null= True, unique= False) 
    fbpage_name = models.CharField(max_length=255, null= True, unique= False) 

    fbform_id = models.CharField(max_length=255, null= True, unique= False) 
    fbform_name = models.CharField(max_length=255, null= True, unique= False) 


    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    created_by = models.BigIntegerField(null=True, blank=True,unique=False)

    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_by = models.BigIntegerField(null=True, blank=True,unique=False)

    status = models.CharField(max_length=255,choices=Status.choices(),default=Status.inactive,unique=False)
    client_id = models.CharField(max_length=255, null= True, unique= False) 
    
    def __str__(self):
      return self.telecaller_name
    

class SubscriptionsFB(models.Model):
    page_id = models.CharField(max_length=255, null= True, unique= False) 
    page_name = models.CharField(max_length=255, null= True, unique= False) 

    fbform_id = models.CharField(max_length=255, null= True, unique= False) 
    fbform_name = models.CharField(max_length=255, null= True, unique= False) 


    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    created_by = models.BigIntegerField(null=True, blank=True,unique=False)

    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_by = models.BigIntegerField(null=True, blank=True,unique=False)

    access_token = models.CharField(max_length=255, null= True, unique= False) 
    client_id = models.CharField(max_length=255, null= True, unique= False) 
    
    def __str__(self):
      return self.page_name
    