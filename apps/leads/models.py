from django.db import models
from .utils import Salutation
from .utils import Createdby
from .utils import Potencialenum
from .utils import Status, StageStatus
import uuid, datetime
from apps.product.models import Product
from apps.location.models import Location
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone


from apps.template.models import Template

from django.conf import settings

# Create your models here.
def generate_token():
  code = str(uuid.uuid4())[:10].replace('-', '').lower()
  return code



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, null= True, unique= True)
    description = models.CharField(max_length=255,null=True, blank=True,unique=False)
    status = models.CharField(max_length=255,choices=Status.choices(),default=Status.active,unique=False)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
      return self.name


class Sources(models.Model):
    status = models.CharField(max_length=255,choices=Status.choices(), default=Status.active,unique=False)
    token = models.CharField(max_length=15,blank=True, null= True, unique= False)
    name = models.CharField(max_length=255, null= True, unique= True)
    description = models.CharField(max_length=70,blank=False, null= True, unique= False)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    conversion_days = models.CharField(max_length= 255, null= True, blank= False, unique= False)
    client_id = models.CharField(max_length=255, null= True, unique= False)
    # assign_user = models.CharField(max_length=255, null=True, blank=True,unique=False)

    # assign_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='assigned_sources')
    assign_user = models.ManyToManyField(User, related_name='assigned_sources')

    def __str__(self):
      return self.name

    # def save(self, *args, **kwargs):
    #   if self.id:
    #     self.updated_at = datetime.datetime.now()
    #   else:
    #     self.token = generate_token()
    #     self.updated_at = datetime.datetime.now()
    #     self.created_at = datetime.datetime.now()
    #   super(Sources, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = timezone.now()
        else:
            self.token = generate_token()
            self.updated_at = timezone.now()
            self.created_at = timezone.now()

        super().save(*args, **kwargs)

    def assign_users(self, user_ids):
        self.assign_user.set(user_ids)



class Stage(models.Model):
    status = models.CharField(max_length=255,choices=Status.choices(), default=Status.active,unique=False)
    name = models.CharField(max_length=255, null= True, unique= True)
    description = models.TextField(blank=False, null= True, unique= False)
    slug = models.SlugField(max_length=250,blank=True, null=True)
    primary_slug = models.SlugField(max_length=250,blank=True, null=True)
    categeory_id  = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_potential = models.CharField(max_length=255,choices=Potencialenum.choices(), default=Potencialenum.no, null=True,unique=False)
    stage_status = models.CharField(max_length=255,choices=StageStatus.choices(), null=True,unique=False)

    # user = models.ManyToManyField(User, related_name='assigned_stage')
    # type = models.CharField(max_length=255, choices=Type.choices(), null=True, unique=False)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    client_id = models.CharField(max_length=255, null= True, unique= False)

    is_main = models.CharField(max_length=255,choices=Potencialenum.choices(), blank=True, null=True, unique=False)
    sms_template_id  = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, related_name='stage_sms_templates')
    email_template_id   = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, related_name='stage_email_templates' )
    # whatsapp_template_id  = models.ForeignKey(template, on_delete=models.SET_NULL, null=True)
    whatsapp_template_id = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, related_name='stage_whatsapp_templates')

    is_recurring = models.CharField(max_length=255,choices=Potencialenum.choices(), blank=True, null=True, unique=False)
    recurring_sms_template_id  = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, related_name='recurringStage_sms_templates')
    recurring_email_template_id  = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, related_name='recurringStage_email_templates')
    recurring_whatsapp_template_id  = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, related_name='recurringStage_whatsapp_templates')

    is_pre_stage = models.CharField(max_length=255,choices=Potencialenum.choices(),blank=True, null=True, unique=False)
    pre_sms_template_id  = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, related_name='prestage_sms_templates')
    pre_email_template_id   = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, related_name='prestage_email_templates')
    pre_whatsapp_template_id  = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, related_name='prestage_whatsapp_templates')

    is_thankyou_stage = models.CharField(max_length=255,choices=Potencialenum.choices(), blank=True, null=True, unique=False)
    thankyou_sms_template_id  = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, related_name='stage_thankyou_sms_templates')
    thankyou_email_template_id  = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, related_name='stage_thankyou_email_templates')
    # thankyou_whatsapp_template_id  = models.ForeignKey(template, on_delete=models.SET_NULL, null=True)
    # thankyou_whatsapp_template_id  = models.ForeignKey(template, on_delete=models.SET_NULL, null=True)
    thankyou_whatsapp_template_id = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, related_name='stage_thankyou_whatsapp_templates')





    def __str__(self):
      return self.name

    def save(self, *args, **kwargs):
      if self.id:
        self.slug = slugify(self.name)
        self.updated_at = datetime.datetime.now()
      else:
        self.slug = slugify(self.name)
        self.primary_slug =  self.slug
        self.updated_at = datetime.datetime.now()
        self.created_at = datetime.datetime.now()
      super(Stage, self).save(*args, **kwargs)

    def assign_users(self, user_ids):
      self.client.set(user_ids)




RANGE_CHOICES = (
    ('0-25', '0-25'),
    ('26-50', '26-50'),
    ('51-75', '51-75'),
    ('76-100', '76-100'),


)


class LeadType(models.Model):
  status = models.CharField(max_length=255,choices=Status.choices(), default=Status.active,unique=False)
  name = models.CharField(max_length=255, null= True, unique= True)
  description = models.CharField(max_length=70,blank=False, null= True, unique= False)
  created_at = models.DateTimeField(auto_now_add= True, unique= False)
  updated_at = models.DateTimeField(auto_now_add= True, unique= False)
  client_id = models.CharField(max_length=255, null= True, unique= False)
  score_range = models.CharField(choices = RANGE_CHOICES, max_length=200)

  def __str__(self):
    return self.name



class StageQuestions(models.Model):
    text = models.CharField(max_length=70,blank=False, null= True, unique= False)
    score = models.IntegerField(null=True, blank=True,unique=False ,default= 0)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    lead_status_id = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True)
    # lead_status_id = models.ForeignKey(LeadStatus, on_delete=models.CASCADE, related_name='status_questions')
    # parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_questions')
    parent_id = models.ForeignKey('StageQuestions', on_delete=models.CASCADE, null=True, blank=True, related_name='child_questions')


    client_id = models.CharField(max_length=255, null= True, unique= False)


    # def __str__(self):
    #   return self.name




class Leads(models.Model):
  salutation = models.CharField(max_length=255,choices=Salutation.choices(), default=Salutation.mr,unique=False)
  name = models.CharField(max_length=255, null=True, blank=False,unique=False)
  phone = models.CharField(max_length=255, null=True, blank=False,unique=True)
  email = models.CharField(max_length=255, null=True, blank=False,unique=True)
  company = models.CharField(max_length=255, null=True, blank=True,unique=False)
  product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
  lead_source_id  = models.ForeignKey(Sources, on_delete=models.SET_NULL, null=True)
  primary_lead_source_id  = models.BigIntegerField(null=True, blank=True,unique=False)
  # lead_type_id = models.BigIntegerField(null=True, blank=True,unique=False)

  lead_type_id = models.ForeignKey(LeadType, on_delete=models.SET_NULL, null=True)

  lead_status_id = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True)
  ringing_date = models.DateTimeField(null=True, blank=True,unique=False)
  created_at = models.DateTimeField(auto_now_add=True,unique=False)
  updated_at = models.DateTimeField(auto_now_add=True,unique=False)
  created_by = models.CharField(max_length=255,choices=Createdby.choices(), default=Createdby.system,unique=False )
  is_potential = models.CharField(max_length=255,choices=Potencialenum.choices(), default=Potencialenum.no,null=True, blank=True)
  city = models.CharField(max_length=255, null=True, blank=True,unique=False)
  spouse_name = models.CharField(max_length=255, null=True, blank=True,unique=False)
  alternate_number = models.CharField(max_length=255, null=True, blank=True,unique=False)
  centre_name = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
  fbpage_id = models.CharField(max_length=255, null=True, blank=True,unique=False)
  fbform_id = models.CharField(max_length=255, null=True, blank=True,unique=False)
  ivr_virtual_number = models.TextField(null=True, blank=True,unique=False)
  is_transfer = models.IntegerField(null=True, blank=True,unique=False)
  transfer_to = models.IntegerField(null=True, blank=True,unique=False)
  other_data = models.TextField(null=True, blank=True,unique=False)
  lead_data = models.TextField(null=True, blank=True,unique=False)
  star_patient = models.CharField(max_length=255,choices=Potencialenum.choices(), default=Potencialenum.no,null=True, blank=True)
  last_mesage_time = models.DateTimeField(null=True, blank=True,unique=False)
  gcampaignid = models.BigIntegerField(null=True, blank=True,unique=False)
  gadgroupid = models.BigIntegerField(null=True, blank=True,unique=False)
  gkeyword = models.TextField(null=True, blank=True,unique=False)
  gdevice = models.TextField(null=True, blank=True,unique=False)
  gdata = models.TextField(null=True, blank=True,unique=False)
  communication_id = models.IntegerField(null=True, blank=True,unique=False)
  client_id = models.CharField(max_length=255, null= True, unique= False)


  # def __str__(self):
  #   return self.id
  def __str__(self):
    return f"Lead ID: {self.id}, Name: {self.name}"


  def formfield_for_dbfield(self, *args, **kwargs):
    formfield = super().formfield_for_dbfield(*args, **kwargs)
    formfield.widget.can_delete_related = False
    formfield.widget.can_change_related = False
    # formfield.widget.can_add_related = False  # can change this, too
    # formfield.widget.can_view_related = False  # can change this, too
    return formfield


class DuplicateLeads(models.Model):
  salutation = models.CharField(max_length=255,choices=Salutation.choices(), default=Salutation.mr,unique=False)
  name = models.CharField(max_length=255, null=True, blank=False,unique=False)
  phone = models.CharField(max_length=255, null=True, blank=False,unique=True)
  email = models.CharField(max_length=255, null=True, blank=False,unique=True)
  company = models.CharField(max_length=255, null=True, blank=True,unique=False)
  product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
  lead_source_id  = models.ForeignKey(Sources, on_delete=models.SET_NULL, null=True)
  primary_lead_source_id  = models.BigIntegerField(null=True, blank=True,unique=False)
  lead_type_id = models.BigIntegerField(null=True, blank=True,unique=False)
  lead_status_id = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True)
  ringing_date = models.DateTimeField(null=True, blank=True,unique=False)
  created_at = models.DateTimeField(auto_now_add=True,unique=False)
  updated_at = models.DateTimeField(auto_now_add=True,unique=False)
  created_by = models.CharField(max_length=255,choices=Createdby.choices(), default=Createdby.system,unique=False )
  is_potential = models.CharField(max_length=255,choices=Potencialenum.choices(), default=Potencialenum.no,null=True, blank=True)
  city = models.CharField(max_length=255, null=True, blank=True,unique=False)
  spouse_name = models.CharField(max_length=255, null=True, blank=True,unique=False)
  alternate_number = models.CharField(max_length=255, null=True, blank=True,unique=False)
  centre_name = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
  fbpage_id = models.CharField(max_length=255, null=True, blank=True,unique=False)
  fbform_id = models.CharField(max_length=255, null=True, blank=True,unique=False)
  ivr_virtual_number = models.TextField(null=True, blank=True,unique=False)
  is_transfer = models.IntegerField(null=True, blank=True,unique=False)
  transfer_to = models.IntegerField(null=True, blank=True,unique=False)
  other_data = models.TextField(null=True, blank=True,unique=False)
  lead_data = models.TextField(null=True, blank=True,unique=False)
  star_patient = models.CharField(max_length=255,choices=Potencialenum.choices(), default=Potencialenum.no,null=True, blank=True)
  last_mesage_time = models.DateTimeField(null=True, blank=True,unique=False)
  gcampaignid = models.BigIntegerField(null=True, blank=True,unique=False)
  gadgroupid = models.BigIntegerField(null=True, blank=True,unique=False)
  gkeyword = models.TextField(null=True, blank=True,unique=False)
  gdevice = models.TextField(null=True, blank=True,unique=False)
  gdata = models.TextField(null=True, blank=True,unique=False)
  communication_id = models.IntegerField(null=True, blank=True,unique=False)
  client_id = models.CharField(max_length=255, null= True, unique= False)


  def __str__(self):
    return self.name


  def formfield_for_dbfield(self, *args, **kwargs):
    formfield = super().formfield_for_dbfield(*args, **kwargs)
    formfield.widget.can_delete_related = False
    formfield.widget.can_change_related = False
    # formfield.widget.can_add_related = False  # can change this, too
    # formfield.widget.can_view_related = False  # can change this, too
    return formfield


class LeadScores(models.Model):
    question = models.CharField(max_length=70,blank=False, null= True, unique= False)
    answer = models.CharField(max_length=70,blank=False, null= True, unique= False)
    score = models.IntegerField(null=True, blank=True,unique=False ,default= 0)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    lead_id = models.ForeignKey(Leads, on_delete=models.SET_NULL, null=True)
    lead_status_id = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True)
    # lead_status_id = models.ForeignKey(LeadStatus, on_delete=models.CASCADE, related_name='status_questions')
    # parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_questions')
    # parent_id = models.ForeignKey('StageQuestions', on_delete=models.CASCADE, null=True, blank=True, related_name='child_questions')
    client_id = models.CharField(max_length=255, null= True, unique= False)


    # def __str__(self):
    #   return self.name



# class LeadAssignedUser(models.Model):
#     assigned = models.IntegerField(null=True, blank=True,unique=False ,default= 0)
#     created_at = models.DateTimeField(auto_now_add= True, unique= False)
#     updated_at = models.DateTimeField(auto_now_add= True, unique= False)
#     lead_id = models.IntegerField(null=True, blank=True,unique=False)
#     # user_id = models.ForeignKey(department='telecaller', on_delete=models.SET_NULL, null=True)
#     # user_id = models.ManyToManyField(User, related_name='assigned_sources')
#     user_id = models.IntegerField(null=True, blank=True,unique=False)
#     client_id = models.CharField(max_length=255, null= True, unique= False)


class LeadAssignedUser(models.Model):
    assigned = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    lead_id = models.IntegerField(null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    client_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"LeadAssignedUser {self.id}"


class LeadTransferUser(models.Model):
    transferred = models.IntegerField(null=True, blank=True,unique=False ,default= 0)
    # transferred_by = models.IntegerField(null=True, blank=True,unique=False)
    # transferred_by = models.ForeignKey(User, null=True, blank=True, unique=False, on_delete=models.SET_NULL)
    transferred_by = models.ForeignKey(User, null=True, blank=True, unique=False, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    lead_id = models.IntegerField(null=True, blank=True,unique=False)
    user_id = models.IntegerField(null=True, blank=True,unique=False)
    client_id = models.CharField(max_length=255, null= True, unique= False)

class LeadAttachments(models.Model):
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    file = models.ImageField(upload_to='media/lead_media', blank=False, null=True)
    lead_id = models.ForeignKey(Leads, on_delete=models.SET_NULL, null=True)
    client_id = models.CharField(max_length=255, null= True, unique= False)

class LeadComments(models.Model):
    created_at = models.DateTimeField(auto_now_add= True, unique= False)
    updated_at = models.DateTimeField(auto_now_add= True, unique= False)
    comment = models.CharField(max_length=255, null= True, unique= False)
    lead_id = models.ForeignKey(Leads, on_delete=models.SET_NULL, null=True)
    is_deleted = models.CharField(max_length=255,choices=Potencialenum.choices(), default=Potencialenum.no,null=True, blank=True)
    client_id = models.CharField(max_length=255, null= True, unique= False)






class LeadStatusLOG(models.Model):
  lead_id = models.ForeignKey(Leads, on_delete=models.SET_NULL, null=True)
  lead_status_id = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True)
  created_at = models.DateTimeField(auto_now_add=True,unique=False)
  updated_at = models.DateTimeField(auto_now_add=True,unique=False)
  user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  salutation = models.CharField(max_length=255,choices=Salutation.choices(), default=Salutation.mr,unique=False)
  name = models.CharField(max_length=255, null=True, blank=True,unique=False)
  phone = models.CharField(max_length=255, null=True, blank=True,unique=False)
  email = models.CharField(max_length=255, null=True, blank=True,unique=False)

  # company = models.CharField(max_length=255, null=True, blank=True,unique=False)
  # product_id = models.ForeignKey(Product.Product, on_delete=models.SET_NULL, null=True)
  # lead_source_id  = models.ForeignKey(Sources, on_delete=models.SET_NULL, null=True)

  product_id = models.BigIntegerField(null=True, blank=True,unique=False)
  lead_source_id = models.BigIntegerField(null=True, blank=True,unique=False)


  city = models.CharField(max_length=255, null=True, blank=True,unique=False)
  alternate_number = models.CharField(max_length=255, null=True, blank=True,unique=False)
  comment = models.CharField(max_length=255, null=True, blank=True,unique=False)
  centre_name = models.CharField(max_length=255, null=True, blank=True,unique=False)


  # primary_lead_source_id  = models.BigIntegerField(null=True, blank=True,unique=False)
  # lead_type_id = models.BigIntegerField(null=True, blank=True,unique=False)
  # ringing_date = models.DateTimeField(null=True, blank=True,unique=False)
  # created_by = models.CharField(max_length=255,choices=Createdby.choices(), default=Createdby.system,unique=False )
  # is_potential = models.CharField(max_length=255,choices=Potencialenum.choices(), default=Potencialenum.no,null=True, blank=True)
  spouse_name = models.CharField(max_length=255, null=True, blank=True,unique=False)
  # centre_name = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
  # fbpage_id = models.CharField(max_length=255, null=True, blank=True,unique=False)
  # fbform_id = models.CharField(max_length=255, null=True, blank=True,unique=False)
  # ivr_virtual_number = models.TextField(null=True, blank=True,unique=False)
  # is_transfer = models.IntegerField(null=True, blank=True,unique=False)
  # transfer_to = models.IntegerField(null=True, blank=True,unique=False)
  # other_data = models.TextField(null=True, blank=True,unique=False)
  # lead_data = models.TextField(null=True, blank=True,unique=False)
  # star_patient = models.CharField(max_length=255,choices=Potencialenum.choices(), default=Potencialenum.no,null=True, blank=True)
  # last_mesage_time = models.DateTimeField(null=True, blank=True,unique=False)
  # gcampaignid = models.BigIntegerField(null=True, blank=True,unique=False)
  # gadgroupid = models.BigIntegerField(null=True, blank=True,unique=False)
  # gkeyword = models.TextField(null=True, blank=True,unique=False)
  # gdevice = models.TextField(null=True, blank=True,unique=False)
  # gdata = models.TextField(null=True, blank=True,unique=False)
  # field_change = models.BooleanField(default=False)
  field_change = models.IntegerField(null=True, blank=True, default=0)
  communication_id = models.IntegerField(null=True, blank=True,unique=False)
  client_id = models.CharField(max_length=255, null= True, unique= False)
  deleted_at = models.DateTimeField(auto_now_add=True,unique=False)
  deleted_by = models.IntegerField(null=True, blank=True,unique=False)




class DeletedLead(models.Model):
  salutation = models.CharField(max_length=255,choices=Salutation.choices(), default=Salutation.mr,unique=False)
  name = models.CharField(max_length=255, null=True, blank=False,unique=False)
  phone = models.CharField(max_length=255, null=True, blank=False,unique=True)
  email = models.CharField(max_length=255, null=True, blank=False,unique=True)
  company = models.CharField(max_length=255, null=True, blank=True,unique=False)
  product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
  lead_source_id  = models.ForeignKey(Sources, on_delete=models.SET_NULL, null=True)
  primary_lead_source_id  = models.BigIntegerField(null=True, blank=True,unique=False)
  lead_type_id = models.BigIntegerField(null=True, blank=True,unique=False)
  lead_status_id = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True)
  ringing_date = models.DateTimeField(null=True, blank=True,unique=False)
  created_at = models.DateTimeField(auto_now_add=True,unique=False)
  updated_at = models.DateTimeField(auto_now_add=True,unique=False)
  created_by = models.CharField(max_length=255,choices=Createdby.choices(), default=Createdby.system,unique=False )
  is_potential = models.CharField(max_length=255,choices=Potencialenum.choices(), default=Potencialenum.no,null=True, blank=True)
  city = models.CharField(max_length=255, null=True, blank=True,unique=False)
  spouse_name = models.CharField(max_length=255, null=True, blank=True,unique=False)
  alternate_number = models.CharField(max_length=255, null=True, blank=True,unique=False)
  centre_name = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
  fbpage_id = models.CharField(max_length=255, null=True, blank=True,unique=False)
  fbform_id = models.CharField(max_length=255, null=True, blank=True,unique=False)
  ivr_virtual_number = models.TextField(null=True, blank=True,unique=False)
  is_transfer = models.IntegerField(null=True, blank=True,unique=False)
  transfer_to = models.IntegerField(null=True, blank=True,unique=False)
  other_data = models.TextField(null=True, blank=True,unique=False)
  lead_data = models.TextField(null=True, blank=True,unique=False)
  star_patient = models.CharField(max_length=255,choices=Potencialenum.choices(), default=Potencialenum.no,null=True, blank=True)
  last_mesage_time = models.DateTimeField(null=True, blank=True,unique=False)
  gcampaignid = models.BigIntegerField(null=True, blank=True,unique=False)
  gadgroupid = models.BigIntegerField(null=True, blank=True,unique=False)
  gkeyword = models.TextField(null=True, blank=True,unique=False)
  gdevice = models.TextField(null=True, blank=True,unique=False)
  gdata = models.TextField(null=True, blank=True,unique=False)
  communication_id = models.IntegerField(null=True, blank=True,unique=False)
  client_id = models.CharField(max_length=255, null= True, unique= False)
  deleted_at = models.DateTimeField(auto_now_add=True,unique=False)
  deleted_by = models.IntegerField(null=True, blank=True,unique=False)

  def __str__(self):
      return f"Lead {self.pk} - {self.created_at}"
