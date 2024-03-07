from django.db import models
from .utils import Type, Status



class Communication(models.Model): 
    status = models.CharField(max_length=255,choices=Status.choices(), default=Status.active,unique=False)
    title = models.CharField(max_length=70,blank=False, null= True, unique= False)
    value = models.CharField(max_length=70,blank=False, null= True, unique= False) 
    description = models.CharField(max_length=70,blank=False, null= True, unique= False)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False) 
    created_by = models.IntegerField(null=True, blank=True,unique=False)
    updated_by = models.IntegerField(null=True, blank=True,unique=False)
    client_id = models.CharField(max_length=255, null= True, unique= False)
    type = models.CharField(max_length=255, choices=Type.choices(), null=True, unique=False)


