from django.db import models
from .utils import Type
from .utils import Smstype
from .utils import Whatsapptype
import uuid, datetime

class Template(models.Model):
  name = models.CharField(max_length=255, null=True, blank=False,unique=True)
  subject = models.CharField(max_length=255, null=True, blank=False,unique=False)
  type = models.CharField(max_length=255,choices=Type.choices(), null=True,unique=False)
  message = models.TextField(blank=False, null= True, unique= False)
  template_id = models.TextField(blank=False, null= True, unique= False)
  parameters = models.TextField(blank=False, null= True, unique= False)
  created_at = models.DateTimeField(auto_now_add=True,unique=False)
  updated_at = models.DateTimeField(auto_now_add=True,unique=False)
  smstype = models.CharField(max_length=255,choices=Smstype.choices(), default=Smstype.english,unique=False)
  whatsapptype = models.CharField(max_length=255,choices=Whatsapptype.choices(), default=Whatsapptype.text,unique=False)
  # whatsappmedia = models.TextField(blank=False, null= True, unique= False)
  whatsappmedia = models.ImageField(upload_to='media/whatsapp_media', blank=False, null=True)
  client_id = models.CharField(max_length=255, null= True, unique= False)
  created_by = models.CharField(max_length=255, null= True, unique= False)
  updated_by = models.CharField(max_length=255, null= True, unique= False)



  def __str__(self):
    return self.name
