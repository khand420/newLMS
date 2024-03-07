from django.shortcuts import get_object_or_404
from .models import Stage
from generalsettings.models import generalsettings
from .models import Leads, Sources, Stage, LeadType, StageQuestions, LeadScores, LeadAssignedUser, LeadTransferUser, LeadAttachments, LeadComments, LeadStatusLOG, DeletedLead, DuplicateLeads
from product.models import Product
from calls.models import Calls
from timeslot.models import timeslot
import datetime



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