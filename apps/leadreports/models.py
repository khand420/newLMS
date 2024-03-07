from django.db import models
# from .utils import Status
import uuid, datetime
from django.conf import settings
from django.contrib.auth.models import User

# # Create your models here.
# class Location(models.Model):
#     # status = models.CharField(max_length=255,choices=Status.choices(),default=Status.active,unique=False)
#     name = models.CharField(max_length=255, null= True, unique= True)
#     created_at = models.DateTimeField(auto_now_add= True, unique= False)
#     updated_at = models.DateTimeField(auto_now_add= True, unique= False)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     client_id = models.CharField(max_length=255, null= True, unique= False)

#     def __str__(self):
#         return self.name