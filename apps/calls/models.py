from django.db import models
from .utils import Status
import uuid, datetime
from django.conf import settings
from django.contrib.auth.models import User
import urllib.request
# from leads.models import Stage, Leads


# Create your models here.
class Calls(models.Model):
    lead_id = models.ForeignKey('leads.Leads', on_delete=models.CASCADE, related_name='calls')
    # leadid = models.ForeignKey('leads.Leads', on_delete=models.CASCADE, related_name='calls')
    date = models.DateTimeField(auto_now_add= False, unique= False)
    # lead_id = models.BigIntegerField(null=True, blank=True,unique=False)
    # lead_status_id = models.BigIntegerField(null=True, blank=True,unique=False)
    lead_status_id = models.ForeignKey('leads.Stage', on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    status = models.CharField(max_length=255,choices=Status.choices(),default=Status.inactive,unique=False)
    check_status = models.CharField(max_length=255,choices=Status.choices(),default=Status.active,unique=False)
    slot = models.CharField(max_length=255, null= True, unique= False)
    telecallerid = models.IntegerField(null=True, blank=True,unique=False)
    today_call = models.CharField(max_length=255,choices=Status.choices(),default=Status.inactive,unique=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    client_id = models.CharField(max_length=255, null= True, unique= False) 
    
    def __str__(self):
      return f"Call for {self.lead.name}"

# Create your models here.
class SMScount(models.Model):
    sms_sent = models.FloatField(null=True, blank=True,unique=False)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    client_id = models.CharField(max_length=255, null= True, unique= False) 
    


# Create your models here.
class Timeslots(models.Model):
    slot_time = models.CharField(max_length=255, null= True, unique= False)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    client_id = models.CharField(max_length=255, null= True, unique= False)

    
    def __str__(self):
      return self.name