
# from leads.models import Sources  # Move the import here

from apps.product.models import Product
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from apps.generalsettings.models import generalsettings
from apps.calls.models import Calls
from apps.calls.models import Timeslots
import datetime
from apps.authentication.models import UserDetails

# from .models import Leads, Stage, LeadType, LeadTransferUser, LeadStatusLOG, Sources
from enum import IntEnum
from enum import Enum





class Salutation(Enum):
  mr = 'mr'
  mrs = 'mrs'
  ms = 'ms'

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]


class Createdby(Enum):
  api = 'api'
  system = 'system'

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]

class Potencialenum(Enum):
  yes = 'yes'
  no = 'no'

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]

class Status(Enum):
  active = 'active'
  inactive = 'inactive'

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]


class StageStatus(Enum):
  Not_Knows  = 'Not Knows'
  Qualified = 'Qualified'
  Disqualified = 'Disqualified'

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]





# from .models import Stage, Product, LeadType, Sources, LeadTransferUser, User, LeadSourceUser




def get_status_by_id(id):
    return Stage.objects.get(id=id)

def get_product_by_id(id):
    return Product.objects.get(id=id)

def get_type_by_id(id):
    return LeadType.objects.get(id=id)

def get_source_by_id(id):
    return Sources.objects.get(id=id)

def get_lead_by_id(id):
    return Leads.objects.get(id=id)

def get_transferred_user(lead_id):
    transferred = ""
    transferred_by = LeadTransferUser.objects.filter(lead_id=lead_id, transferred=1).values('transferred_by').first()
    if transferred_by:
        transfer_by = transferred_by['transferred_by']
        transfer_data = User.objects.filter(id=transfer_by).values('name').first()
        if transfer_data:
            transferred_by = transfer_data['name']
    return transferred_by

def get_transferredto_user(lead_id):
    transferred_to = ""
    transferredto = LeadTransferUser.objects.filter(lead_id=lead_id, transferred=1).values('user_id').first()
    if transferredto:
        transfer_to = transferredto['user_id']
        transfer_data = User.objects.filter(id=transfer_to).values('name').first()
        if transfer_data:
            transferred_to = transfer_data['name']
    return transferred_to



# def get_source_user(source_id):
#     users = Sources.objects.filter(assign_user = , lead_source_id=source_id).values('user_id')
#     # users = userdetail.objects.filter(uniqueid=clientid, department='telecaller').values('user_id')
#     source_users = []
#     for user in users:
#         user_data = User.objects.filter(id=user['user_id']).values('name').first()
#         if user_data:
#             source_users.append(user_data['name'])
#     if source_users:
#         return ', '.join(source_users)
#     else:
#         return "No user assigned"



def get_source_user(source_id):
    users = Sources.objects.filter(lead_source_id=source_id).values('assign_user__id')
    source_users = []
    for user in users:
        user_data = User.objects.filter(id=user['assign_user__id']).values('username').first()
        if user_data:
            source_users.append(user_data['username'])
    if source_users:
        return ', '.join(source_users)
    else:
        return "No user assigned"




def get_parked_leads():
    data = generalsettings.objects.filter(key="parked_lead_notification_days").first()
    days = int(data.value)
    leads = Leads.objects.all()

    suggested_leads = {}
    for lead in leads:
        logs = LeadStatusLOG.objects.filter(lead=lead).order_by('-created_at')
        if logs.exists():
            converted_status = Stage.objects.filter(slug="converted").first()
            parked_status = Stage.objects.filter(slug="parked").first()
            latest_log = logs.first()

            if latest_log.lead_status_id != converted_status.id and latest_log.lead_status_id != parked_status.id:
                fdate = latest_log.created_at.date()
                tdate = datetime.now().date()
                diff_in_days = (tdate - fdate).days

                if diff_in_days >= days:
                    suggested_leads[lead.id] = lead.name

    return suggested_leads




def get_status_id(slug):
    status = get_object_or_404(Stage, slug=slug)
    return status.id



def get_date_time(lead_id, status_id):
    call_data = Calls.objects.filter(lead_id=lead_id, lead_status_id=status_id).order_by('-id').first()
    if call_data:
        return call_data
    return False
