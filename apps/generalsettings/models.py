from django.db import models
import uuid, datetime
from django.conf import settings
from django.contrib.auth.models import User
import urllib.request
# from leads.models import Sources


# Create your models here.
class generalsettings(models.Model):
    meta_key = models.CharField(max_length=255, null= True, unique= True)
    meta_value = models.CharField(max_length=255,null=True, blank=True,unique=False)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    client_id = models.CharField(max_length=255, null= True, unique= False)


    
    def __str__(self):
      return self.name
    
# My_CHOICES = (
#     ('My Telly', 'My Telly'),
#     ('My Operator', 'My Operator'),  
# )

My_CHOICES = [
    ('My-Telly', 'My-Telly'),
    ('My-Operator', 'My-Operator'),
]
OutgoingCall_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]
 
class TellyCommSettings(models.Model):
    provider = models.CharField(choices = My_CHOICES, max_length=255,)
    phones = models.CharField(max_length=255, null= True, unique= True)
    source_id = models.ForeignKey('leads.Sources', on_delete=models.SET_NULL, null=True)
    # source_id = models.ForeignKey('Sources', on_delete=models.SET_NULL, null=True)
    client_id = models.CharField(max_length=255, null= True, unique= False)
    auth_token = models.CharField(max_length=255, null= True, unique=False)

    outgoing_call = models.CharField(choices=OutgoingCall_CHOICES, max_length=255) 
    outgoing_call_name = models.CharField(max_length=255, null=True, blank=True)
    outgoing_call_phone = models.CharField(max_length=255, null=True, blank=True)

    ivr_token = models.CharField(max_length=255, null= True, unique=False)
    company_id = models.CharField(max_length=255, null= True, unique=False)
    secret_token = models.CharField(max_length=255, null= True, unique=False)
    public_ivr_id = models.CharField(max_length=255, null= True, unique=False)

    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    
    # def __str__(self):
    #   return f"{self.phones} - {self.provider}"
    def __str__(self):
      return f"{self.phones} - {self.provider} - {self.source_id}" 
      # return self.phones, self.source_id, self.client_id


# class OutgoingCall(models.Model):
#     telly_comm_settings = models.ForeignKey(TellyCommSettings, on_delete=models.CASCADE, related_name='outgoing_calls')
#     name = models.CharField(max_length=255)
#     phone = models.CharField(max_length=255)