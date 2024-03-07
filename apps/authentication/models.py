
# Create your models here.
from django.db import models
from .utils import Status
import uuid, datetime

from django.conf import settings




# class DepartmentManager(models.Manager):
#     def telecaller(self):
#         return self.get_queryset().filter(name='telecaller')

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=255, null= True, unique= True)
    status = models.CharField(max_length=255,choices=Status.choices(),default=Status.active,unique=False)
    slug = models.SlugField(max_length=250,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    # objects = DepartmentManager()

    def __str__(self):
      return self.name



# Create your models here.
class Industry(models.Model):
    name = models.CharField(max_length=255, null= True, unique= True)
    description = models.CharField(max_length=255,null=True, blank=True,unique=False)
    status = models.CharField(max_length=255,choices=Status.choices(),default=Status.active,unique=False)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
      return self.name

    def save(self, *args, **kwargs):
     super(Industry, self).save(*args, **kwargs)




# Create your models here.
class UserDetails(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    department_id = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    uniqueid = models.CharField(max_length=255, null=True, blank=True,unique=False, default=uuid.uuid4)
    department = models.CharField(max_length=255, null=True, blank=True,unique=False)
    phone = models.CharField(max_length=255, null=True, blank=False,unique=False)
