from django.views.generic import TemplateView
from web_project import TemplateLayout


from django.contrib import messages
from django.shortcuts import reverse
from django.utils.dateparse import parse_date
from django.db.models import Count, F, Value, Max
from django.contrib.auth.forms import AuthenticationForm
# from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from apps.authentication.models import Industry
from apps.authentication.models import UserDetails

from apps.calls.models import SMScount
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.leads.models import Leads, Stage, Sources, LeadStatusLOG, LeadAssignedUser, LeadTransferUser
from datetime import datetime, timedelta
from apps.generalsettings.models import generalsettings

from django.db import models

from django.views.decorators.http import require_http_methods
from django.db.models import Count, Func, F, IntegerField
from django.db.models.functions import ExtractWeek
from django.db.models import Prefetch
from apps.calls.models import Calls

from django.shortcuts import HttpResponse
from django.db.models import Count
from django.utils.timezone import make_aware  # Import make_aware
import json
from datetime import date

from apps.leads.ivr import ivr_user




@login_required
def index(request):

    udetail = UserDetails.objects.get(user_id=request.user.id)
    clientid = udetail.uniqueid
    user_department = udetail.department
    print(user_department, 'department-----')

    if user_department == 'telecaller':
        return telecaller_dashboard(request)
    else:
        return dashboard(request)


# def telecaller_dashboard(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     clientid = udetail.uniqueid
#     user_department = udetail.department

#     return render(request, 'telecaller.html', {'user_department':user_department})




@login_required
def telecaller_dashboard(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    udetail = UserDetails.objects.get(user_id=request.user.id)
    clientid = udetail.uniqueid
    user_department = udetail.department


    user_data = request.user
    # user_department = user_data.department_id
    # user_ivr_number = user_data.ivr_virtual_number
    telecaller_id = user_data.id

    ivr_users = []
    if user_department == 'telecaller':
        ivr_users.append({'name': user_data.username, 'user_id': user_data.id})
    else:
        # ivrcontrol = IvrController()
        ivr_users = ivr_user()

    # qualified_id = ""
     # appointment scheduled , patient-registration,next-review, interested, converted
    # main_stages = Stage.objects.filter(slug__in=["appointment-scheduled", "interested", "patient-registration", "procedure", "call-back", "next-review", "converted"]).all()
    # converted_leads_stages = ["appointment-scheduled", "patient-registration", "next-review", "interested", "converted"]
    # converted_leads_stages_id = []

    # for stage in main_stages:
    #     if stage.slug == "appointment-scheduled":
    #         appointment_id = stage.id
    #     elif stage.slug == "interested":
    #        interested_id = stage.id
    #     elif stage.slug == "patient-registration":
    #         patient_id = stage.id
    #     elif stage.slug == "next-review":
    #         next_review_id = stage.id
    #     elif stage.slug == "converted":
    #         converted_id = stage.id

    #     if stage.slug in converted_leads_stages:
    #         converted_leads_stages_id.append(stage.id)

    # total_appointments = Leads.objects.filter(lead_status_id=appointment_id).count()
    # total_interested = Leads.objects.filter(lead_status_id=interested_id).count()
    # total_next_review = Leads.objects.filter(lead_status_id=next_review_id).count()
    # total_patient = Leads.objects.filter(lead_status_id=patient_id).count()
    # total_converted = Leads.objects.filter(lead_status_id=converted_id).count()


    # all_settings = generalsettings.objects.all()
    # settings_dict = {}
    # for setting in all_settings:
    #     settings_dict[setting.key] = setting.value

    # parked_lead_notification_days = settings_dict.get("parked_lead_notification_days", 0)
    # avg_lead_cost = settings_dict.get("avg_lead_cost", 0)
    # appointment_revenue = settings_dict.get("appointment_revenue", 0)
    # investigation_revenue = settings_dict.get("investigation_revenue", 0)
    # procedure_revenue = settings_dict.get("procedure_revenue", 0)
    # qualified_leads_to_leads = settings_dict.get("qualified_leads_to_leads", 0)
    # appointment_to_qualified_conversion = settings_dict.get("appointment_to_qualified_conversion", 0)
    # investigation_to_appointment_conversion = settings_dict.get("investigation_to_appointment_conversion", 0)
    # procedure_to_investigation_conversion = settings_dict.get("procedure_to_investigation_conversion", 0)
    # procedure_to_qualified_conversion = settings_dict.get("procedure_to_qualified_conversion", 0)
    # procedure_to_appointment_conversion = settings_dict.get("procedure_to_appointment_conversion", 0)
    # qualified_lead_future_value = settings_dict.get("qualified_lead_future_value", 0)
    # appointment_lead_real_value = settings_dict.get("appointment_lead_real_value", 0)
    # appointment_lead_future_value = settings_dict.get("appointment_lead_future_value", 0)
    # investigation_lead_real_value = settings_dict.get("investigation_lead_real_value", 0)
    # investigation_lead_future_value = settings_dict.get("investigation_lead_future_value", 0)
    # procedure_lead_real_value = settings_dict.get("procedure_lead_real_value", 0)
    # procedure_lead_future_value = settings_dict.get("procedure_lead_future_value", 0)

    source_arr = []
    status_array = []

    home_leads = Leads.objects.all()

    related_sources_data = Sources.objects.filter(assign_user= user_data)

    # print(related_sources_data, '----------')
    # related_sources_data = Sources.objects.filter(user_id=user_data.id)
    related_sources = [source.lead_source_id for source in related_sources_data]
    # print(related_sources, '----------')

    if related_sources:
        for value in related_sources:
            related_status_data = Stage.objects.filter(user_id=user_data.id, lead_source_id=value)

            if related_status_data:
                for stage in related_status_data:
                    new_leads = Leads.objects.filter(lead_status_id=stage.lead_status_id, lead_source_id=value)
                    status_array.extend([lead.id for lead in new_leads])
            else:
                source_data = Leads.objects.filter(lead_source_id=value)
                source_arr.extend([lead.id for lead in source_data])

    if status_array:
        status_array = list(set(status_array))
    if source_arr:
        source_arr = list(set(source_arr))

    telecaller_assigned_leads = LeadAssignedUser.objects.filter(user_id=telecaller_id)
    assign_leads_arr = [lead.lead_id for lead in telecaller_assigned_leads]

    telecaller_transfer_leads = LeadTransferUser.objects.filter(user_id=telecaller_id)
    transfer_leads_arr = [lead.lead_id for lead in telecaller_transfer_leads]

    telecaller_leads_arr = list(set(source_arr + assign_leads_arr + transfer_leads_arr + status_array))

    home_leads = home_leads.filter(id__in=telecaller_leads_arr)

    telecaller_leads_record = home_leads.all()
    total_leads = home_leads.count()

    # status_data = Stage.objects.get(slug="converted")
    # total_converted_leads = Leads.objects.filter(lead_status_id=status_data.id).count()

    # avg_lead_cost = generalsettings.objects.get(key="avg_lead_cost").value

    # qualified_lead_real_value = 0
    # total_interested_real_value = total_interested * qualified_lead_real_value
    # total_interested_future_value = total_interested * qualified_lead_future_value
    # total_appointment_real_value = total_appointments * appointment_lead_real_value
    # total_appointment_future_value = total_appointments * appointment_lead_future_value
    # total_next_review_real_value = total_next_review * investigation_lead_real_value
    # total_next_review_future_value = total_next_review * investigation_lead_future_value
    # total_procedure_real_value = total_procedures * procedure_lead_real_value
    # total_procedure_future_value = total_procedures * procedure_lead_future_value

    # future_value = (
    #     total_qualified_future_value + total_appointment_future_value + total_investigation_future_value + total_procedure_future_value
    # )
    # real_value = total_qualified_real_value + total_appointment_real_value + total_investigation_real_value + total_procedure_real_value

    lead_status_data = Leads.objects.values("lead_status_id", "lead_status_id__name").annotate(total=models.Count("id")).filter(
        lead_status_id__status="active",
        lead_status_id__isnull=False
    ).order_by("lead_status_id")

    lead_type_data = Leads.objects.values("lead_type_id", "lead_type_id__name").annotate(total=models.Count("id")).filter(
        lead_type_id__isnull=False
    ).order_by("lead_type_id")

    # monthly_data = Leads.objects.extra(select={"month_name": "CONCAT(MONTHNAME(created_at), '.', YEAR(created_at))"}).values("month_name").annotate(total=models.Count("id")).order_by("month_name")

    weekly_data = Leads.objects.extra(
        select={"week": "WEEKOFYEAR(created_at)", "dateRange": "CONCAT(STR_TO_DATE(CONCAT(YEARWEEK(created_at),' Monday'), '%X%V %W'), ' to ', DATE_ADD(STR_TO_DATE(CONCAT(YEARWEEK(created_at),' Monday'), '%X%V %W'), INTERVAL 6 DAY))"}
    ).values("week", "dateRange").annotate(total=models.Count("id")).order_by("week")

    # converted_leads = []
    # for stage_id in converted_leads_stages_id:
    #     converted_leads.extend(
    #         LeadStatusLOG.objects.select_related("lead")
    #         .filter(lead__lead_status_id=stage_id)
    #         .values("lead_id", "lead__created_at", "created_at")
    #     )

    # total_converted_leads_data = [lead["lead_id"] for lead in converted_leads]

    # total_converted_leads = len(set(total_converted_leads_data))

    # total = 0
    # for lead in converted_leads:
    #     to = datetime.strptime(lead["lead__created_at"], "%Y-%m-%d %H:%M:%S")
    #     from_ = datetime.strptime(lead["created_at"], "%Y-%m-%d %H:%M:%S")
    #     total += (from_ - to).days

    # avg_conversion_time = round(total / total_converted_leads) if total_converted_leads > 0 else ""


    # Code to retrieve callbacks and pending callbacks
    callbacksarr = (
        Leads.objects
        .select_related('calls')
        .filter(
            calls__date__gte=datetime.now(),
            calls__date__lte=(datetime.combine(datetime.now(), datetime.min.time()) + timedelta(days=1)),
            calls__status=1,
            id__in=telecaller_leads_record
        )
        .values('id', 'name', 'calls__date')
        .annotate(total=Count('id'))
        .order_by('calls__date')
    )

    pendingcallback = (
        Leads.objects
        .select_related('calls')
        .filter(
            calls__date__lte=datetime.now(),
            calls__status=1,
            id__in=telecaller_leads_record
        )
        .values('id', 'name', 'calls__date', 'phone', 'created_at', 'updated_at')
        .annotate(total=Count('id'))
        .order_by('-calls__date')
    )
    print(pendingcallback, '---------------------')

    today_date = date.today()
    todays_total_pending_callbacks =  pendingcallback.filter(calls__date__date=today_date)

    # total_pending_callbacks = pendingcallback.aggregate(Sum('total'))['total__sum'] or 0
    sms_count = SMScount.objects.count()
    # sms_count = Calls.objects.count()

    tele_callbacks_count = (
        Leads.objects.select_related("calls")
        .filter(
            calls__date__gte=datetime.combine(datetime.now(), datetime.min.time()),
            calls__date__lte=(datetime.combine(datetime.now(), datetime.min.time()) + timedelta(days=1)),
            calls__status=1,
            id__in=telecaller_leads_record
        )
        .values("id", "name", "calls__date")
        .annotate(total=models.Count("id"))
        .order_by("calls__date")
    )


    today_start = datetime.combine(datetime.now(), datetime.min.time())
    today_end = today_start + timedelta(days=1)

    # Modify the queryset to count callbacks for today
    callbacks_count_today = (
        Leads.objects
        .filter(
            calls__date__gte=today_start,
            calls__date__lt=today_end,
            calls__status=1,
            id__in=telecaller_leads_record
        )
        .count()
    )


    context.update({
        "tele_callbacks_count": tele_callbacks_count,
        "smscount": sms_count,
        "todaysCall":callbacks_count_today,
        "ivruser": ivr_users,
        "totalLeads": total_leads,
        "callbacksarr": callbacksarr,
        "pendingcallback": pendingcallback,
        # "totalConvertedLeads": total_converted_leads,
        "leadStatusData": lead_status_data,
        "leadTypeData": lead_type_data,
        # "monthlyData": monthly_data,
        "weeklyData": weekly_data,
        # "avgConversionTime": avg_conversion_time,
        # "realValue": real_value,
        # "futureValue": future_value,
        'user_department':user_department
    })

    return render(request, "telecaller.html", context)
    # return render(request, 'telecaller.html', {})





def dashboard(request):
    udetail = UserDetails.objects.get(user_id=request.user.id)
    clientid = udetail.uniqueid
    user_department = udetail.department

    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)


    user_data = request.user
    # user_department = user_data.department_id
    # user_ivr_number = user_data.ivr_virtual_number
    telecaller_id = user_data.id

    # telecallers = UserDetails.objects.filter(uniqueid=clientid, department='telecaller').values('user_id', 'user__username')
    ivr_users_response = None
    ivr_users_data = []
    if user_department == 'telecaller':
        ivr_users_data.append({'name': user_data.username, 'user_id': user_data.id})
    else:
        # ivrcontrol = IvrController()
        # ivr_users = ivr_user(request)
        ivr_users_response = ivr_user(request)

    if ivr_users_response != None:
        if ivr_users_response.status_code == 200:
            ivr_users_data = ivr_users_response.content
            ivr_users_data = json.loads(ivr_users_data.decode('utf-8')).get('user_arr', [])
        # ivr_users_data = ivr_users_response.json().get('user_arr', [])

        # print(ivr_users_data)

    # print(ivr_users_data, 'ivr_users-------')



    start_date = end_date = ""
    if 'daterange' in request.POST and request.POST['daterange']:
        start_date = timezone.datetime.strptime(request.POST['daterange']['startDate'], '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        end_date = timezone.datetime.strptime(request.POST['daterange']['endDate'], '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        end_date += timezone.timedelta(days=1)

    home_leads = Leads.objects.values_list('id', flat=True)
    if start_date and end_date:
        home_leads = home_leads.filter(created_at__gte=start_date, created_at__lt=end_date)

    total_leads = home_leads.count()

            # Website Leads
    website_total = Leads.objects.filter(lead_source_id=17)
    if start_date and end_date:
        website_total = website_total.filter(created_at__gte=start_date, created_at__lt=end_date)
    website_total = website_total.count()
    # Total Converted Leads
    # statusData = Stage.objects.get(slug="converted")
    # total_converted_leads = Leads.objects.filter(lead_status_id=statusData.id).count()
    total_converted_leads = Leads.objects.filter().count()

            # Qualified Leads
    qualified_stages = Stage.objects.filter(stage_status='Qualified')
    qualified_stages_id = qualified_stages.values_list('id', flat=True)
    qualified_leads = Leads.objects.filter(lead_status_id__in=qualified_stages_id)
    if start_date and end_date:
        qualified_leads = qualified_leads.filter(created_at__gte=start_date, created_at__lt=end_date)
    total_qualified = qualified_leads.count()


            # Disqualified Leads
    disqualified_stages = Stage.objects.filter(stage_status='Disqualified')
    disqualified_stages_id = disqualified_stages.values_list('id', flat=True)
    total_disqualified = Leads.objects.filter(lead_status_id__in=disqualified_stages_id)
    if start_date and end_date:
        total_disqualified = total_disqualified.filter(created_at__gte=start_date, created_at__lt=end_date)
    total_disqualified = total_disqualified.count()

      # Not Knows Leads
    notknows_stages = Stage.objects.filter(stage_status='Not Knows')
    notknows_stages_id = notknows_stages.values_list('id', flat=True)
    total_notknows_leads = Leads.objects.filter(lead_status_id__in=notknows_stages_id)
    if start_date and end_date:
        total_notknows_leads = total_notknows_leads.filter(created_at__gte=start_date, created_at__lt=end_date)
    total_notknows_leads = total_notknows_leads.count()




    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    monthlyData = Leads.objects.filter(created_at__range=[start_date, end_date]) \
        .annotate(month_total=Count('id')) \
        .values('created_at__month', 'month_total') \
        .order_by('-created_at__year', '-created_at__month')
    monthlyData_json = json.dumps(list(monthlyData))

    # print('monthlyData------------', monthlyData_json)

    # Fetch weekly data for the current year
    current_year = datetime.now().year
    weekly_data = Leads.objects.filter(created_at__year=current_year) \
        .annotate(week=Count('created_at')) \
        .values('week') \
        .annotate(total=Count('id')) \
        .values('week', 'total')

    # Fetch data for lead status and lead type
    leadStatusData = Leads.objects.filter(lead_status_id__isnull=False) \
        .values('lead_status_id', 'lead_status_id__name') \
        .annotate(total=Count('id')) \
        .values('lead_status_id', 'lead_status_id__name', 'total')

    leadTypeData = Leads.objects.filter(lead_type_id__isnull=False) \
        .values('lead_type_id', 'lead_type_id__name') \
        .annotate(total=Count('id')) \
        .values('lead_type_id', 'lead_type_id__name', 'total')
    leadTypeData_json = json.dumps(list(leadTypeData))


    # print('leadTypeData--------------', leadTypeData)



    # current_datetime = datetime.now()
    current_datetime = timezone.now()
    next_day_datetime = current_datetime + timedelta(days=1)

    # callbacks_arr = Leads.objects.annotate(
    #     latest_call_date=Max('calls__date')
    # ).filter(
    #     calls__date__gte=current_datetime,
    #     calls__date__lt=next_day_datetime,
    #     calls__status=1
    # ).filter(
    #     calls__date=F('latest_call_date')
    # ).select_related('calls').order_by('calls__date').distinct()

    callbacks_arr = Leads.objects.prefetch_related('calls').filter(
        calls__date__gte=datetime.now(),
        calls__date__lte= next_day_datetime,
        calls__status=1
    ).order_by('calls__date').distinct()
    # print("callbacks_arr----------", callbacks_arr)


    tele_callbacks_count = Leads.objects.annotate(
        latest_call_date=Max('calls__date')
    ).filter(
        calls__date__gte=datetime.combine(current_datetime.date(), datetime.min.time()),
        calls__date__lt=datetime.combine(next_day_datetime.date(), datetime.min.time()) + timedelta(days=1),
        calls__status=1
    ).filter(
        calls__date=F('latest_call_date')
    ).count()



    pending_callback = Leads.objects.filter(
        calls__date__lte=current_datetime,
        calls__status=1
    ).prefetch_related('calls').order_by('-calls__date').distinct()

    # Print the queryset
    # print("pending_callback=========", pending_callback)



    sms_count = SMScount.objects.count()

    scheduled_leads = Leads.objects.filter(
        lead_status_id=2,
        calls__date__isnull=False
    ).annotate(
        latest_call_date=Max('calls__date')
    ).filter(
        calls__date__gte=current_datetime,
        calls__date__lt=next_day_datetime
    ).filter(
        calls__date=F('latest_call_date')
    ).select_related('calls').order_by('-calls__date').distinct()

    scheduled_leads_count = Leads.objects.filter(
        lead_status_id=2,
        calls__date__gte=datetime.combine(current_datetime.date(), datetime.min.time()),
        calls__date__lt=datetime.combine(next_day_datetime.date(), datetime.min.time()) + timedelta(days=1)
    ).annotate(
        latest_call_date=Max('calls__date')
    ).filter(
        calls__date=F('latest_call_date')
    ).count()


    # Today Leads
    newleadsarr = Leads.objects.filter(
        created_at__gte=datetime.now().replace(hour=0, minute=0, second=0),
        created_at__lte=datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=1)
    ).order_by('created_at')

    # Today Updated Leads
    updateleadsarr = Leads.objects.filter(
        updated_at__gte=datetime.now().replace(hour=0, minute=0, second=0),
        updated_at__lte=datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=1)
    ).order_by('updated_at')

    # Today Lead Logs
    logleadsarr = LeadStatusLOG.objects.filter(
        created_at__gte=datetime.now().replace(hour=0, minute=0, second=0),
        created_at__lte=datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=1)
    ).order_by('created_at')

    # Session handling
    # if 'callbackcount' not in request.session or not request.session["callbackcount"]:
    #     request.session["callbackcount"] = tele_callbacks_count
    # request.session["appointmentcount"] = scheduled_leads_count

    context.update({
        'smscount': sms_count,
            'totalLeads': total_leads,
            'totalConvertedLeads': total_converted_leads,
            # 'avgConversionTime': avg_conversion_time,
            'total_qualified': total_qualified,
            'total_disqualified': total_disqualified,
            # 'disqualified_html': disqualified_html,
            'total_notknows': total_notknows_leads,
            # 'notknows_html': notknows_html,

        'ivruser': ivr_users_data,
        'callbacksarr': callbacks_arr,
        'monthlyData': monthlyData_json,
        'weeklyData': weekly_data,
        'leadTypeData': leadTypeData_json,
        'leadStatusData':leadStatusData,

        'newleadsarr':newleadsarr,
        'updateleadsarr':updateleadsarr,
        'logleadsarr':logleadsarr,

        'pendingcallback': pending_callback,
        'tele_callbacks_count': tele_callbacks_count,
        'schedulded_leads': scheduled_leads,
        'schedulded_leads_count': scheduled_leads_count,
    })

    # dashboard_count_data = dashboardCount(request)
    # context.update(dashboard_count_data)

    return render(request, 'homepage.html', context)




def dashboardCount(request):
    # print("HELLLLLLLLLO g q")
    try:
        # start_date = end_date = ""
        # if 'daterange' in request.POST and request.POST['daterange']:
        #     start_date = timezone.datetime.strptime(request.POST['daterange']['startDate'], '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        #     end_date = timezone.datetime.strptime(request.POST['daterange']['endDate'], '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        #     end_date += timezone.timedelta(days=1)

        start_date = end_date = ""

        if 'daterange[startDate]' in request.POST and request.POST['daterange[startDate]']:
            start_date_str = request.POST['daterange[startDate]']
            end_date_str = request.POST['daterange[endDate]']

        print("Received start_date_str:", start_date_str)
        print("Received end_date_str:", end_date_str)

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
        else:
            start_date_str = request.POST.get('date')

            print("Received start_date_str:", start_date_str)

            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = start_date + timedelta(days=1)

        print("Parsed Start Date:", start_date)
        print("Parsed End Date:", end_date)



        user_data = request.user
        # user_department = user_data.department_id
        # user_ivr_number = user_data.ivr_virtual_number

        qualified_id = ""
        main_stages = Stage.objects.filter(slug__in=["appointment", "investigation", "patient-registration", "procedure", "call-back", "next-review"])

        converted_leads_stages = ["appointment", "patient-registration", "next-review"]
        converted_leads_stages_id = []

        # for stage in main_stages:
        #     if stage.slug == "appointment":
        #         appointment_id = stage.id
        #     elif stage.slug == "investigation":
        #         investigation_id = stage.id
        #     elif stage.slug == "patient-registration":
        #         qualified_id = stage.id
        #     elif stage.slug == "procedure":
        #         procedure_id = stage.id
        #     elif stage.slug == "call-back":
        #         callback_id = stage.id

        #     if stage.slug in converted_leads_stages:
        #         converted_leads_stages_id.append(stage.id)

        # total_appointments = Leads.objects.filter(lead_status_id=appointment_id).count()
        # total_investigations = Leads.objects.filter(lead_status_id=investigation_id).count()
        # total_procedures = Leads.objects.filter(lead_status_id=procedure_id).count()
        # total_qualifieds = Leads.objects.filter(lead_status_id=qualified_id).count()

        # all_settings = generalsettings.objects.all()
        # settings_dict = {}
        # for setting in all_settings:
        #     settings_dict[setting.key] = setting.value

        home_leads = Leads.objects.values_list('id', flat=True)
        if start_date and end_date:
            home_leads = home_leads.filter(created_at__gte=start_date, created_at__lt=end_date)
        # if user_department == 1:
            # Assuming LeadSourceUser is a separate model that connects users to lead sources.
            # related_sources_data = LeadSourceUser.objects.filter(user_id=user_data.id)
            # related_sources = related_sources_data.values_list('lead_source_id', flat=True)
            # if related_sources:
            #     home_leads = home_leads.filter(lead_source_id__in=related_sources)

            # if user_ivr_number:
                # home_leads = home_leads.filter(ivr_virtual_number=user_ivr_number)

        total_leads = home_leads.count()

        facebook_total = Leads.objects.filter(lead_source_id=28)
        if start_date and end_date:
            facebook_total = facebook_total.filter(created_at__gte=start_date, created_at__lt=end_date)
        facebook_total = facebook_total.count()


        # IVR Leads
        ivr_total = Leads.objects.filter(lead_source_id=32)
        if start_date and end_date:
            ivr_total = ivr_total.filter(created_at__gte=start_date, created_at__lt=end_date)
        ivr_total = ivr_total.count()

        # Landing Page Leads
        landing_total = Leads.objects.filter(lead_source_id=33)
        if start_date and end_date:
            landing_total = landing_total.filter(created_at__gte=start_date, created_at__lt=end_date)
        landing_total = landing_total.count()

        # Website Leads
        website_total = Leads.objects.filter(lead_source_id=17)
        if start_date and end_date:
            website_total = website_total.filter(created_at__gte=start_date, created_at__lt=end_date)
        website_total = website_total.count()

        total_html = "Facebook Leads: {}\n".format(facebook_total)
        total_html += "IVR Leads: {}\n".format(ivr_total)
        total_html += "Website Leads: {}\n".format(website_total)
        total_html += "Landing Page Leads: {}\n".format(landing_total)

        # Total Converted Leads
        # statusData = Stage.objects.get(slug="converted")
        # total_converted_leads = Leads.objects.filter(lead_status_id=statusData.id).count()
        total_converted_leads = Leads.objects.filter().count()


        # Other Converted Leads
        convertedLeads_stages_id = [1, 2, 3]  # Replace with your actual stage IDs
        facebook_converted = Leads.objects.filter(lead_source_id=28, lead_status_id__in=convertedLeads_stages_id)
        if start_date and end_date:
            facebook_converted = facebook_converted.filter(created_at__gte=start_date, created_at__lt=end_date)
        facebook_converted = facebook_converted.count()

        ivr_converted = Leads.objects.filter(lead_source_id=32, lead_status_id__in=convertedLeads_stages_id)
        if start_date and end_date:
            ivr_converted = ivr_converted.filter(created_at__gte=start_date, created_at__lt=end_date)
        ivr_converted = ivr_converted.count()

        landing_converted = Leads.objects.filter(lead_source_id=33, lead_status_id__in=convertedLeads_stages_id)
        if start_date and end_date:
            landing_converted = landing_converted.filter(created_at__gte=start_date, created_at__lt=end_date)
        landing_converted = landing_converted.count()

        website_converted = Leads.objects.filter(lead_source_id=17, lead_status_id__in=convertedLeads_stages_id)
        if start_date and end_date:
            website_converted = website_converted.filter(created_at__gte=start_date, created_at__lt=end_date)
        website_converted = website_converted.count()

        other_converted_html = "Facebook Leads: {}\n".format(facebook_converted)
        other_converted_html += "IVR Leads: {}\n".format(ivr_converted)
        other_converted_html += "Website Leads: {}\n".format(website_converted)
        other_converted_html += "Landing Page Leads: {}\n".format(landing_converted)

        # Average Conversion Time
        avg_conversion_time = ""  # Implement your logic here

        # Qualified Leads
        qualified_stages = Stage.objects.filter(stage_status='Qualified')
        qualified_stages_id = qualified_stages.values_list('id', flat=True)
        qualified_leads = Leads.objects.filter(lead_status_id__in=qualified_stages_id)
        if start_date and end_date:
            qualified_leads = qualified_leads.filter(created_at__gte=start_date, created_at__lt=end_date)
        total_qualified = qualified_leads.count()

        facebook_qualified = Leads.objects.filter(lead_source_id=28, lead_status_id__in=qualified_stages_id)
        if start_date and end_date:
            facebook_qualified = facebook_qualified.filter(created_at__gte=start_date, created_at__lt=end_date)
        facebook_qualified = facebook_qualified.count()

        ivr_qualified = Leads.objects.filter(lead_source_id=32, lead_status_id__in=qualified_stages_id)
        if start_date and end_date:
            ivr_qualified = ivr_qualified.filter(created_at__gte=start_date, created_at__lt=end_date)
        ivr_qualified = ivr_qualified.count()

        landing_qualified = Leads.objects.filter(lead_source_id=33, lead_status_id__in=qualified_stages_id)
        if start_date and end_date:
            landing_qualified = landing_qualified.filter(created_at__gte=start_date, created_at__lt=end_date)
        landing_qualified = landing_qualified.count()

        website_qualified = Leads.objects.filter(lead_source_id=17, lead_status_id__in=qualified_stages_id)
        if start_date and end_date:
            website_qualified = website_qualified.filter(created_at__gte=start_date, created_at__lt=end_date)
        website_qualified = website_qualified.count()

        qualified_html = "Facebook Leads: {}\n".format(facebook_qualified)
        qualified_html += "IVR Leads: {}\n".format(ivr_qualified)
        qualified_html += "Website Leads: {}\n".format(website_qualified)
        qualified_html += "Landing Page Leads: {}\n".format(landing_qualified)

        # Disqualified Leads
        disqualified_stages = Stage.objects.filter(stage_status='Disqualified')
        disqualified_stages_id = disqualified_stages.values_list('id', flat=True)
        total_disqualified = Leads.objects.filter(lead_status_id__in=disqualified_stages_id)
        if start_date and end_date:
            total_disqualified = total_disqualified.filter(created_at__gte=start_date, created_at__lt=end_date)
        total_disqualified = total_disqualified.count()

        facebook_disqualified = Leads.objects.filter(lead_source_id=28, lead_status_id__in=disqualified_stages_id)
        if start_date and end_date:
            facebook_disqualified = facebook_disqualified.filter(created_at__gte=start_date, created_at__lt=end_date)
        facebook_disqualified = facebook_disqualified.count()

        ivr_disqualified = Leads.objects.filter(lead_source_id=32, lead_status_id__in=disqualified_stages_id)
        if start_date and end_date:
            ivr_disqualified = ivr_disqualified.filter(created_at__gte=start_date, created_at__lt=end_date)
        ivr_disqualified = ivr_disqualified.count()

        landing_disqualified = Leads.objects.filter(lead_source_id=33, lead_status_id__in=disqualified_stages_id)
        if start_date and end_date:
            landing_disqualified = landing_disqualified.filter(created_at__gte=start_date, created_at__lt=end_date)
        landing_disqualified = landing_disqualified.count()

        website_disqualified = Leads.objects.filter(lead_source_id=17, lead_status_id__in=disqualified_stages_id)
        if start_date and end_date:
            website_disqualified = website_disqualified.filter(created_at__gte=start_date, created_at__lt=end_date)
        website_disqualified = website_disqualified.count()

        disqualified_html = "Facebook Leads: " + str(facebook_disqualified) + "\n"
        disqualified_html += "IVR Leads: " + str(ivr_disqualified) + "\n"
        disqualified_html += "Website Leads: " + str(website_disqualified) + "\n"
        disqualified_html += "Landing Page Leads: " + str(landing_disqualified) + "\n"

        # Not Knows Leads
        notknows_stages = Stage.objects.filter(stage_status='Not Knows')
        notknows_stages_id = notknows_stages.values_list('id', flat=True)
        total_notknows_leads = Leads.objects.filter(lead_status_id__in=notknows_stages_id)
        if start_date and end_date:
            total_notknows_leads = total_notknows_leads.filter(created_at__gte=start_date, created_at__lt=end_date)
        total_notknows_leads = total_notknows_leads.count()

        facebook_notknows = Leads.objects.filter(lead_source_id=28, lead_status_id__in=notknows_stages_id)
        if start_date and end_date:
            facebook_notknows = facebook_notknows.filter(created_at__gte=start_date, created_at__lt=end_date)
        facebook_notknows = facebook_notknows.count()

        ivr_notknows = Leads.objects.filter(lead_source_id=32, lead_status_id__in=notknows_stages_id)
        if start_date and end_date:
            ivr_notknows = ivr_notknows.filter(created_at__gte=start_date, created_at__lt=end_date)
        ivr_notknows = ivr_notknows.count()

        landing_notknows = Leads.objects.filter(lead_source_id=33, lead_status_id__in=notknows_stages_id)
        if start_date and end_date:
            landing_notknows = landing_notknows.filter(created_at__gte=start_date, created_at__lt=end_date)
        landing_notknows = landing_notknows.count()

        website_notknows = Leads.objects.filter(lead_source_id=17, lead_status_id__in=notknows_stages_id)
        if start_date and end_date:
            website_notknows = website_notknows.filter(created_at__gte=start_date, created_at__lt=end_date)
        website_notknows = website_notknows.count()

        notknows_html = "Facebook Leads: " + str(facebook_notknows) + "\n"
        notknows_html += "IVR Leads: " + str(ivr_notknows) + "\n"
        notknows_html += "Website Leads: " + str(website_notknows) + "\n"
        notknows_html += "Landing Page Leads: " + str(landing_notknows) + "\n"


        print("works", total_leads, total_converted_leads, total_disqualified, total_notknows_leads)
        # print()
        # Prepare the JSON response
        response_data = {
            'totalLeads': total_leads,
            'totalConvertedLeads': total_converted_leads,
            'avgConversionTime': avg_conversion_time,
            'total_qualified': total_qualified,
            'total_disqualified': total_disqualified,
            'disqualified_html': disqualified_html,
            'total_notknows': total_notknows_leads,
            'notknows_html': notknows_html,
            # Add other statistics here if needed
        }
        print(response_data)

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'error': str(e)})






# @require_http_methods(["POST"])
# def lead_status_graph(request):
#     try:
#         start_date = end_date = updated_start_date = updated_end_date = None

#         if 'daterange' in request.POST and request.POST['daterange']:
#             start_date = timezone.datetime.strptime(request.POST['daterange']['startDate'], "%Y-%m-%d")
#             end_date = timezone.datetime.strptime(request.POST['daterange']['endDate'], "%Y-%m-%d")
#         if 'updateddate' in request.POST and request.POST['updateddate']:
#             updated_start_date = timezone.datetime.strptime(request.POST['updateddate']['startDate'], "%Y-%m-%d")
#             updated_end_date = timezone.datetime.strptime(request.POST['updateddate']['endDate'], "%Y-%m-%d")

#         lead_status_data = Leads.objects.filter(lead_status_id__isnull=False, lead_status_id__status='active').annotate(status_name=F('lead_status_id__name')).values('lead_status_id', 'status_name').annotate(total=Count('id'))

#         if start_date and end_date:
#             lead_status_data = lead_status_data.filter(created_at__gte=start_date, created_at__lt=end_date + timezone.timedelta(days=1))
#         if updated_start_date and updated_end_date:
#             lead_status_data = lead_status_data.filter(updated_at__gte=updated_start_date, updated_at__lt=updated_end_date + timezone.timedelta(days=1))

#         final_array = []
#         s = 0
#         labels = [item['status_name'] for item in lead_status_data]
#         final_array = [item['total'] for item in lead_status_data]
#         statusSum = [s+final_array[i] for i in final_array ]
#         # for i in final_array[i]:
#         #     s+=i

#         # print("================================", final_array, labels)

#         return JsonResponse({'labels': labels, 'finalarray': final_array,'statusSum':s})

#     except Exception as e:
#         return JsonResponse({'error': str(e)})

# @csrf_exempt
# def lead_status_graph(request):
#     start_date = end_date = updated_startdate = updated_enddate = ""

#     if request.method == 'POST':
#         data = request.POST

#         if 'daterange' in data and 'startDate' in data['daterange'] and 'endDate' in data['daterange']:
#             start_date = datetime.strptime(data['daterange']['startDate'], '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
#             end_date = (datetime.strptime(data['daterange']['endDate'], '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')

#         if 'updateddate' in data and 'startDate' in data['updateddate'] and 'endDate' in data['updateddate']:
#             updated_startdate = datetime.strptime(data['updateddate']['startDate'], '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
#             updated_enddate = (datetime.strptime(data['updateddate']['endDate'], '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')

#         if updated_startdate and updated_enddate:
#             leaddata = LeadStatusLOG.objects.filter(created_at__gte=updated_startdate, created_at__lt=updated_enddate).values_list('lead_id', flat=True).distinct()

#             leadStatusData = Leads.objects.filter(id__in=leaddata, lead_status_id__isnull=False).values('lead_status_id__name').annotate(total=models.Count('id'))
#         else:
#             leadStatusData = Leads.objects.filter(lead_status_id__isnull=False)

#             if start_date and end_date:
#                 leadStatusData = leadStatusData.filter(created_at__gte=start_date, created_at__lt=end_date)

#     leadStatusData = leadStatusData.values('lead_status_id__name').annotate(total=models.Count('id'))


#     totalleads = sum([item['total'] for item in leadStatusData])
#     finalarray = [item['total'] for item in leadStatusData]
#     labels = [item['lead_status_id__name'] for item in leadStatusData]

#     response_data = {
#         'labels': labels,
#         'finalarray': finalarray,
#         'totalleads': totalleads,
#     }

#     return JsonResponse(response_data)



@csrf_exempt
def lead_status_graph(request):
    start_date = end_date = updated_startdate = updated_enddate = ""

    if request.method == 'POST':

        data = request.POST
        # print(data, '-----')

        if 'daterange[startDate]' in data and 'daterange[endDate]' in data:
            start_date = datetime.strptime(data['daterange[startDate]'], '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
            end_date = (datetime.strptime(data['daterange[endDate]'], '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')

        if 'updateddate[startDate]' in data and 'updateddate[endDate]' in data:
            updated_startdate = datetime.strptime(data['updateddate[startDate]'], '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
            updated_enddate = (datetime.strptime(data['updateddate[endDate]'], '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')

        # if 'daterange' in data and 'startDate' in data['daterange'] and 'endDate' in data['daterange']:
        #     start_date = datetime.strptime(data['daterange']['startDate'], '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
        #     end_date = (datetime.strptime(data['daterange']['endDate'], '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')

        # if 'updateddate' in data and 'startDate' in data['updateddate'] and 'endDate' in data['updateddate']:
        #     updated_startdate = datetime.strptime(data['updateddate']['startDate'], '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
        #     updated_enddate = (datetime.strptime(data['updateddate']['endDate'], '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')

    # print('####',start_date, end_date)
    # print('------',updated_startdate,updated_enddate)

    # Initialize leadStatusData outside of the if conditions
    leadStatusData = None

    if updated_startdate and updated_enddate:
        leaddata = LeadStatusLOG.objects.filter(created_at__gte=updated_startdate, created_at__lt=updated_enddate).values_list('lead_id', flat=True).distinct()

        leadStatusData = Leads.objects.filter(id__in=leaddata, lead_status_id__isnull=False).values('lead_status_id__name').annotate(total=models.Count('id'))
    else:
        leadStatusData = Leads.objects.filter(lead_status_id__isnull=False)

        if start_date and end_date:
            leadStatusData = leadStatusData.filter(created_at__gte=start_date, created_at__lt=end_date)

        leadStatusData = leadStatusData.values('lead_status_id__name').annotate(total=models.Count('id'))

    totalleads = sum([item['total'] for item in leadStatusData])
    finalarray = [item['total'] for item in leadStatusData]
    labels = [item['lead_status_id__name'] for item in leadStatusData]

    response_data = {
        'labels': labels,
        'finalarray': finalarray,
        'totalleads': totalleads,
    }

    return JsonResponse(response_data)



# def weekly_leads(request):
#     year = datetime.now().year
#     start_date = datetime(year, datetime.now().month, 1)
#     end_date = start_date + timedelta(days=31)
#     end_date = end_date.replace(day=1) - timedelta(days=1)

#     if request.method == 'POST' and 'startDate' in request.POST and 'endDate' in request.POST:
#         start_date = make_aware(datetime.strptime(request.POST['startDate'], '%Y-%m-%d'))
#         end_date = make_aware(datetime.strptime(request.POST['endDate'], '%Y-%m-%d')) + timedelta(days=1)
#         year = end_date.year

#     sweek = start_date.strftime("%U")
#     monthfirstweek = get_start_and_end_date(sweek, year)
#     start_date = monthfirstweek['start_date']

#     month = start_date.month

#     if month == 12:
#         # year = year + 1
#         pass

#     eweek = end_date.strftime("%U")
#     monthlastweek = get_start_and_end_date(eweek, year)
#     end_date = monthlastweek['end_date']

#     weekly_data = Leads.objects \
#         .filter(created_at__gte=start_date, created_at__lt=end_date) \
#         .annotate(week_of_year=Count('created_at')) \
#         .values('week_of_year') \
#         .annotate(total=Count('id')) \
#         .values('week_of_year', 'total')

#     total_leads = sum(week['total'] for week in weekly_data)
#     final_array = [week['total'] for week in weekly_data]
#     labels = [f"Week {week['week_of_year']} to Week {week['week_of_year'] + 1}" for week in weekly_data]

#     response_data = {
#         'labels': labels,
#         'finalarray': final_array,
#         'totalleads': total_leads,
#     }

#     return HttpResponse(json.dumps(response_data), content_type='application/json')

# def get_start_and_end_date(week_number, year):
#     d = datetime.strptime(f'{year}-W{int(week_number) - 1}-1', "%Y-W%U-%w")
#     start_date = make_aware(d.replace(hour=0, minute=0, second=0, microsecond=0))
#     end_date = make_aware((d + timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=999999))
#     return {'start_date': start_date, 'end_date': end_date}



# @csrf_exempt
# def weekly_leads(request):
#     # today = datetime.now()
#     # year = today.year
#     # start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#     # end_date = start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)
#     # end_date += timedelta(days=1)

#     # if request.method == 'POST' and 'daterange' in request.POST:
#     #     start_date = datetime.strptime(request.POST['daterange']['startDate'], '%Y-%m-%d')
#     #     end_date = datetime.strptime(request.POST['daterange']['endDate'], '%Y-%m-%d') + timedelta(days=1)
#     #     year = end_date.year

#     # if request.method == 'POST' and 'daterange' in request.POST:
#     #     daterange = json.loads(request.POST['daterange'])
#     #     start_date = datetime.strptime(daterange['startDate'], '%Y-%m-%d')
#     #     end_date = datetime.strptime(daterange['endDate'], '%Y-%m-%d') + timedelta(days=1)
#     #     year = end_date.year

#     try:
#         selected_date = request.POST.get('daterange', None)

#         if selected_date:
#             selected_date = json.loads(selected_date)
#             start_date = datetime.strptime(selected_date['startDate'], '%Y-%m-%d')
#             end_date = datetime.strptime(selected_date['endDate'], '%Y-%m-%d') + timedelta(days=1)
#         else:
#             # Default to the current month's first and last weeks
#             today = datetime.now()
#             year = today.year
#             start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#             end_date = start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)
#             end_date += timedelta(days=1)


#     except (json.JSONDecodeError, KeyError, ValueError):
#         return HttpResponseBadRequest("Invalid or missing date range data")

#     print("--------",start_date, end_date,)

#     sweek = start_date.strftime('%U')
#     monthfirstweek = get_start_and_end_date(sweek, year)
#     start_date = monthfirstweek['start_date']

#     month = start_date.month

#     if month == 12:
#         # year = start_date.year + 1
#         pass

#     eweek = end_date.strftime('%U')
#     monthlastweek = get_start_and_end_date(eweek, year)
#     end_date = monthlastweek['end_date']

#     weekly_data = Leads.objects.annotate(week=ExtractWeek('created_at')).filter(
#         created_at__gte=start_date,
#         created_at__lt=end_date
#     ).values('week').annotate(total=Count('id')).order_by('week')

#     total_leads = sum(item['total'] for item in weekly_data)
#     labels = [f"{item['start_date'].strftime('%d %b')} to {item['end_date'].strftime('%d %b')}" for item in [get_start_and_end_date(week['week'], year) for week in weekly_data]]

#     final_array = [item['total'] for item in weekly_data]

#     return JsonResponse({
#         'labels': labels,
#         'finalarray': final_array,
#         'totalleads': total_leads
#     })


# def get_start_and_end_date(week, year):
#     start_date = datetime.strptime(f"{year}-{week}-1", "%G-%V-%u")
#     end_date = start_date + timedelta(days=6)
#     return {
#         'start_date': start_date.replace(hour=0, minute=0, second=0),
#         'end_date': end_date.replace(hour=0, minute=0, second=0)
#     }



@csrf_exempt
def weekly_leads(request):
    try:
        selected_date = request.POST.get('daterange', None)

        if selected_date:
            selected_date = json.loads(selected_date)
            start_date = datetime.strptime(selected_date['startDate'], '%Y-%m-%d')
            end_date = datetime.strptime(selected_date['endDate'], '%Y-%m-%d') + timedelta(days=1)
        else:
            # Default to the current month's first and last weeks
            today = datetime.now()
            year = today.year
            start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)
            end_date += timedelta(days=1)

    except (json.JSONDecodeError, KeyError, ValueError):
        return HttpResponseBadRequest("Invalid or missing date range data")

    sweek = start_date.strftime('%U')
    monthfirstweek = get_start_and_end_date(sweek, start_date.year)
    start_date = monthfirstweek['start_date']

    month = start_date.month

    if month == 12:
        pass

    eweek = end_date.strftime('%U')
    monthlastweek = get_start_and_end_date(eweek, start_date.year)
    end_date = monthlastweek['end_date']

    weekly_data = Leads.objects.annotate(week=ExtractWeek('created_at')).filter(
        created_at__gte=start_date,
        created_at__lt=end_date
    ).values('week').annotate(total=Count('id')).order_by('week')

    total_leads = sum(item['total'] for item in weekly_data)

    # Corrected usage of get_start_and_end_date within list comprehension
    labels = [f"{get_start_and_end_date(week['week'], start_date.year)['start_date'].strftime('%d %b')} to {get_start_and_end_date(week['week'], start_date.year)['end_date'].strftime('%d %b')}" for week in weekly_data]

    final_array = [item['total'] for item in weekly_data]

    return JsonResponse({
        'labels': labels,
        'finalarray': final_array,
        'totalleads': total_leads
    })

def get_start_and_end_date(week, year):
    start_date = datetime.strptime(f"{year}-{week}-1", "%G-%V-%u")
    end_date = start_date + timedelta(days=6)
    return {
        'start_date': start_date.replace(hour=0, minute=0, second=0),
        'end_date': end_date.replace(hour=0, minute=0, second=0)
    }




# def lead_source_graph(request):
#     start_date = end_date = ""

#     if request.method == 'POST':
#         data = request.POST

#         if 'daterange' in data and 'startDate' in data['daterange'] and 'endDate' in data['daterange']:
#             start_date = datetime.strptime(data['daterange']['startDate'], '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
#             end_date = datetime.strptime(data['daterange']['endDate'], '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
#             end_date = (datetime.strptime(end_date, '%Y-%m-%d 00:00:00') + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')

#     stage_array = ['34', '35', '36', '37', '38']  #--------------
#     # include in part[..]
#     stage_array = ['Immediate', 'HOT', 'Warm', 'COLD', 'Baat nahi ho payi hai']

#     lead_source_data = Leads.objects.annotate(
#         source_name=Value("source_name", output_field=models.CharField()),
#         status_name=Value("status_name", output_field=models.CharField())
#     ).filter(
#         lead_status_id__in=stage_array,
#         lead_source__status='active',
#         lead_source_id__isnull=False
#     ).values(
#         'lead_source_id',
#         'lead_source__name',
#         'lead_status__name'
#     )

#     if start_date and end_date:
#         lead_source_data = lead_source_data.filter(
#             created_at__gte=start_date,
#             created_at__lt=end_date
#         )

#     lead_source_data = lead_source_data.values(
#         'lead_source_id',
#         'lead_source__name',
#         'lead_status__name'
#     ).annotate(
#         total=Count('id')
#     )

#     raw_data = {}
#     labels2 = []
#     for entry in lead_source_data:
#         source_name = entry['lead_source__name']
#         status_name = entry['lead_status__name']
#         if source_name not in raw_data:
#             raw_data[source_name] = {}
#         if status_name not in raw_data[source_name]:
#             raw_data[source_name][status_name] = 0
#         raw_data[source_name][status_name] += entry['total']

#     final_second_data = {}
#     second_sum_array = []

#     for source_name, status_data in raw_data.items():
#         final_second_data[source_name] = status_data
#         second_sum_array.append(sum(status_data.values()))

#     second_sum_array_total = sum(second_sum_array)

#     labels2 = list(final_second_data.keys())
#     object2 = final_second_data

#     response_data = {
#         'finalSecondData': final_second_data,
#         'sumarray': second_sum_array_total,
#         'secondSumArray': second_sum_array,
#         'labels2': labels2,
#         'object2': object2
#     }

#     return JsonResponse(response_data)


def lead_source_graph(request):
    start_date = end_date = ""

    if request.method == 'POST':
        data = request.POST

        if 'daterange' in data and 'startDate' in data['daterange'] and 'endDate' in data['daterange']:
            start_date = datetime.strptime(data['daterange']['startDate'], '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
            end_date = datetime.strptime(data['daterange']['endDate'], '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
            end_date = (datetime.strptime(end_date, '%Y-%m-%d 00:00:00') + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')

    stage_array = ['255', '254', '36', '37', '38']  #--------------
    # include in part[..]
    # stage_array = ['Immediate', 'HOT', 'Warm', 'COLD', 'Baat nahi ho payi hai']

    lead_source_data = Leads.objects.annotate(
        source_name=Value("source_name", output_field=models.CharField()),
        status_name=Value("status_name", output_field=models.CharField())
    ).filter(
        lead_status_id__in=stage_array,
        lead_source_id__status='active',
        lead_source_id__id__isnull=False  # Use the correct related field syntax
    ).values(
        'lead_source_id',
        'lead_source_id__name',
        'lead_status_id__name'
    )

    if start_date and end_date:
        lead_source_data = lead_source_data.filter(
            created_at__gte=start_date,
            created_at__lt=end_date
        )

    lead_source_data = lead_source_data.values(
        'lead_source_id',
        'lead_source_id__name',
        'lead_status_id__name'
    ).annotate(
        total=Count('id')
    )

    raw_data = {}
    labels2 = []
    for entry in lead_source_data:
        source_name = entry['lead_source_id__name']  # Use the correct related field syntax
        status_name = entry['lead_status_id__name']
        if source_name not in raw_data:
            raw_data[source_name] = {}
        if status_name not in raw_data[source_name]:
            raw_data[source_name][status_name] = 0
        raw_data[source_name][status_name] += entry['total']

    final_second_data = {}
    second_sum_array = []

    for source_name, status_data in raw_data.items():
        final_second_data[source_name] = status_data
        second_sum_array.append(sum(status_data.values()))

    second_sum_array_total = sum(second_sum_array)

    labels2 = list(final_second_data.keys())
    object2 = final_second_data

    response_data = {
        'finalSecondData': final_second_data,
        'sumarray': second_sum_array_total,
        'secondSumArray': second_sum_array,
        'labels2': labels2,
        'object2': object2
    }

    return JsonResponse(response_data)













# from django.shortcuts import render
# from django.http import JsonResponse
# from django.db.models import Q, F
# from .models import Lead, LeadAssignedUser, LeadTransferUser, LeadSourceUser

# def update_lead_filter(request):
#     start_date = end_date = ""

#     if 'daterange' in request.POST and request.POST['daterange']:
#         start_date = request.POST['daterange']['startDate']
#         end_date = request.POST['daterange']['endDate']
#     else:
#         start_date = request.POST['date']
#         end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

#     user_data = request.user
#     user_department = user_data.department_id

#     home_leads = Lead.objects.all()

#     if user_department == 1:
#         related_sources_data = LeadSourceUser.objects.filter(user=user_data)
#         related_sources = related_sources_data.values_list('lead_source_id', flat=True)
#         home_leads = home_leads.filter(lead_source_id__in=related_sources)

#         telecaller_assigned_leads = LeadAssignedUser.objects.filter(user=user_data)
#         telecaller_transfer_leads = LeadTransferUser.objects.filter(user=user_data)

#         telecaller_leads = telecaller_assigned_leads.values_list('lead_id', flat=True) \
#                         .union(telecaller_transfer_leads.values_list('lead_id', flat=True))
#         telecaller_leads = list(telecaller_leads)
#         home_leads = home_leads.filter(Q(id__in=telecaller_leads) | Q(id__in=telecaller_leads))

#     lead_records = home_leads.values_list('id', flat=True)
#     lead_records = list(set(lead_records))

#     update_leads_arr = Lead.objects.filter(
#         Q(updated_at__gte=start_date) &
#         Q(updated_at__lt=end_date) &
#         Q(id__in=lead_records)
#     ).annotate(
#         leadstatus=F('lead_status__name'),
#         leadsource=F('lead_source__name')
#     ).order_by('updated_at')

#     count = update_leads_arr.count()

#     context = {
#         'update_leads_arr': update_leads_arr,
#         'count': count,
#     }

#     if request.is_ajax():
#         return JsonResponse(context)
#     else:
#         return render(request, 'update_lead_template.html', context)


# filters part
from django.db.models import Q

@login_required
def callback_filter(request):
    # userid = request.user
    # start_date = end_date = ""

    # if 'daterange' in request.POST and request.POST['daterange']:
    #     start_date = datetime.strptime(request.POST['daterange']['startDate'], '%Y-%m-%d')
    #     end_date = datetime.strptime(request.POST['daterange']['endDate'], '%Y-%m-%d') + timedelta(days=1)
    # else:
    #     start_date = datetime.strptime(request.POST['date'], '%Y-%m-%d')
    #     end_date = datetime.strptime(request.POST['date'], '%Y-%m-%d') + timedelta(days=1)

    udetail = UserDetails.objects.get(user=request.user)
    user_department = udetail.department

    start_date = end_date = ""
    start_date_str = end_date_str = ""

    if 'daterange[startDate]' in request.POST and request.POST['daterange[startDate]']:
        start_date_str = request.POST['daterange[startDate]']
        end_date_str = request.POST['daterange[endDate]']

    print("Received start_date_str:", start_date_str)
    print("Received end_date_str:", end_date_str)

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
    else:
        # start_date_str = request.POST.get('date')
        start_date_str = request.POST.get('date', '')

        print("Received start_date_str:", start_date_str)

        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = start_date + timedelta(days=1)

    print("Parsed Start Date:", start_date)
    print("Parsed End Date:", end_date)

    user_data = request.user

    if user_department == 'telecaller':
        home_leads = Leads.objects.all()

        # related_sources_data = LeadSourceUser.objects.filter(user=user_data)
        related_sources_data = Sources.objects.filter(assign_user= user_data)
        # if related_sources_data.exists():
        #     related_sources = related_sources_data.values_list("lead_source_id", flat=True)
        #     home_leads = home_leads.filter(lead_source_id__in=related_sources)

        if related_sources_data.exists():
            related_sources = related_sources_data.values_list('lead_source_id', flat=True)
            home_leads = home_leads.filter(lead_source_id__in=related_sources)

        telecaller_assigned_leads = LeadAssignedUser.objects.filter(user_id=user_data.id)
        assign_leads_arr = telecaller_assigned_leads.values_list('lead_id', flat=True)

        telecaller_transfer_leads = LeadTransferUser.objects.filter(user_id=user_data.id)
        transfer_leads_arr = telecaller_transfer_leads.values_list('lead_id', flat=True)

        telecaller_leads_arr = list(set(assign_leads_arr) | set(transfer_leads_arr))
        home_leads = home_leads.filter(id__in=telecaller_leads_arr)

        telecaller_leads_record = home_leads.all()
        lead_record = telecaller_leads_record.values_list('id', flat=True)

        lead_record = list(set(lead_record))

        callbacks_arr = Leads.objects.filter(
            Q(calls__date__gte=start_date) &
            Q(calls__date__lte=end_date) &
            Q(calls__status=1) &
            Q(id__in=lead_record)
        ).prefetch_related('calls').order_by('calls__date').distinct()

    else:
        lead_record = Leads.objects.filter(
        Q(calls__date__gte=start_date_str) &
        Q(calls__date__lte=end_date_str) &
        Q(calls__status=1)
    ).values_list('id', flat=True).distinct()
        # callbacks_arr = Leads.objects.filter(
        #     Q(calls__date__gte=start_date) &
        #     Q(calls__date__lte=end_date) &
        #     Q(calls__status=1)
        # ).select_related('calls').order_by('calls__date').distinct()

        # callbacks_arr = Leads.objects.filter(
        #     Q(calls__date__gte=start_date_str) &
        #     Q(calls__date__lte=end_date_str) &
        #     Q(calls__status=1) &
        #     Q(id__in=lead_record)
        # ).select_related('calls').order_by('calls__date').distinct()
    callbacks_arr = Leads.objects.filter(
    Q(calls__date__gte=start_date_str) &
    Q(calls__date__lte=end_date_str) &
    Q(calls__status=1) &
    Q(id__in=lead_record)
).select_related('calls').order_by('calls__date').distinct()


        # callbacks_arr = Leads.objects.filter(
        #     Q(calls__date__gte=start_date) &
        #     Q(calls__date__lt=end_date) &
        #     Q(calls__status=1)
        # ).prefetch_related('calls').order_by('-calls__date').distinct()


    html = ""
    count = 0

    if callbacks_arr.exists():
        count = callbacks_arr.count()
        for callbacks in callbacks_arr:
            html += f"""
                <tr>
                    <td>{callbacks.id}</td>
                    <td><a href="{reverse('lead_update', args=[callbacks.id])}" target="_blank">{callbacks.name}</a></td>
                    <td>{callbacks.phone}</td>
                    <td>{callbacks.calls.date}</td>
                    <td>{callbacks.updated_at}</td>
                </tr>
            """
    else:
        html = "<tr><td colspan='5'>No Calls</td></tr>"

    return JsonResponse({'html': html, 'count': count})


@login_required
def prev_callback_filter(request):
    udetail = UserDetails.objects.get(user=request.user)
    user_department = udetail.department
    userid = request.user

    start_date = end_date = ""
    start_date_str = end_date_str = ""

    if 'daterange[startDate]' in request.POST and request.POST['daterange[startDate]']:
        start_date_str = request.POST['daterange[startDate]']
        end_date_str = request.POST['daterange[endDate]']

    print("Received start_date_str:", start_date_str)
    print("Received end_date_str:", end_date_str)

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
    else:
        # start_date_str = request.POST.get('date')
        start_date_str = request.POST.get('date', '')

        print("Received start_date_str:", start_date_str)

        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = start_date + timedelta(days=1)

    print("Parsed Start Date:", start_date)
    print("Parsed End Date:", end_date)


    user_data = request.user

    if user_department == 'telecaller':
        home_leads = Leads.objects.all()
        # related_sources_data = LeadSourceUser.objects.filter(user=user_data)
        related_sources_data = Sources.objects.filter(assign_user= user_data)


        if related_sources_data.exists():
            related_sources = related_sources_data.values_list('lead_source_id', flat=True)
            home_leads = home_leads.filter(lead_source_id__in=related_sources)

        telecaller_assigned_leads = LeadAssignedUser.objects.filter(user=user_data)
        assign_leads_arr = telecaller_assigned_leads.values_list('lead_id', flat=True)

        telecaller_transfer_leads = LeadTransferUser.objects.filter(user=user_data)
        transfer_leads_arr = telecaller_transfer_leads.values_list('lead_id', flat=True)

        telecaller_leads_arr = list(set(assign_leads_arr) | set(transfer_leads_arr))
        home_leads = home_leads.filter(id__in=telecaller_leads_arr)

        telecaller_leads_record = home_leads.all()
        lead_record = telecaller_leads_record.values_list('id', flat=True)

        lead_record = list(set(lead_record))

        # pending_callback = Leads.objects.filter(
        #     Q(calls__date__gte=start_date) &
        #     Q(calls__date__lt=end_date) &
        #     Q(calls__status=1) &
        #     Q(id__in=lead_record)
        # ).select_related('calls').order_by('-calls__date').distinct()
        pending_callback = Leads.objects.filter(
            Q(calls__date__gte=start_date) &
            Q(calls__date__lt=end_date) &
            Q(calls__status=1)
        ).prefetch_related('calls').order_by('-calls__date').distinct()
    else:
        pending_callback = Leads.objects.filter(
            Q(calls__date__gte=start_date) &
            Q(calls__date__lt=end_date) &
            Q(calls__status=1)
        ).prefetch_related('calls').order_by('-calls__date').distinct()

        # print(pending_callback)

        # pending_callback = Leads.objects.filter(
        #     Q(calls__date__gte=start_date) &
        #     Q(calls__date__lt=end_date) &
        #     Q(calls__status=1)
        # ).select_related('calls').order_by('-calls__date').distinct()

    html = ""
    count = 0

    # if pending_callback.exists():
    #     count = pending_callback.count()
    #     for callback in pending_callback:
    #         html += f"""
    #             <tr>
    #                 <td>{callback.id}</td>
    #                 <td><a href="{callback.get_absolute_url()}" target="_blank">{callback.name}</a></td>
    #                 <td>{callback.phone}</td>
    #                 <td>{callback.calls.date}</td>
    #                 <td>{callback.updated_at}</td>
    #             </tr>
    #         """
    # else:
    #     html = "<tr><td colspan='5'>No Calls</td></tr>"

    # return JsonResponse({'html': html, 'count': count})

    if pending_callback.exists():
        count = pending_callback.count()
        for callback in pending_callback:
            html += f"""
                <tr>
                    <td>{callback.id}</td>
                    <td><a href="{reverse('lead_update', args=[callback.id])}" target="_blank">{callback.name}</a></td>
                    <td>{callback.phone}</td>
                    <td>{callback.created_at}</td>
                    <td>{callback.updated_at}</td>
                </tr>
            """
    else:
        html = "<tr><td colspan='5'>No Calls</td></tr>"

    return JsonResponse({'html': html, 'count': count})


@login_required
def update_lead_filter(request):
    start_date = end_date = ""
    udetail = UserDetails.objects.get(user=request.user)
    user_department = udetail.department
    userid = request.user

    # if 'daterange' in request.POST and request.POST['daterange']:
    #     start_date = request.POST['daterange']['startDate']
    #     end_date = request.POST['daterange']['endDate']
    # else:
    #     start_date = request.POST['date']
    #     end_date = (start_date + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')

    # if 'daterange' in request.POST and request.POST['daterange']:
    #     selected_date = json.loads(request.POST['daterange'])
    #     start_date = datetime.strptime(selected_date['startDate'], '%Y-%m-%d')
    #     end_date = datetime.strptime(selected_date['endDate'], '%Y-%m-%d') + timedelta(days=1)
    # else:
    #     start_date = datetime.strptime(request.POST['date'], '%Y-%m-%d')
    #     end_date = start_date + timedelta(days=1)

    # start_date = None
    # end_date = None

    if 'daterange[startDate]' in request.POST and request.POST['daterange[startDate]']:
        start_date_str = request.POST['daterange[startDate]']
        end_date_str = request.POST['daterange[endDate]']

    print("Received start_date_str:", start_date_str)
    print("Received end_date_str:", end_date_str)

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
    else:
        start_date_str = request.POST.get('date')

        print("Received start_date_str:", start_date_str)

        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = start_date + timedelta(days=1)

    print("Parsed Start Date:", start_date)
    print("Parsed End Date:", end_date)

    # if 'daterange' in request.POST and request.POST['daterange']:
    #     selected_date = json.loads(request.POST['daterange'])
    #     start_date = datetime.strptime(selected_date['startDate'], '%Y-%m-%d')
    #     end_date = datetime.strptime(selected_date['endDate'], '%Y-%m-%d') + timedelta(days=1)
    # elif 'date' in request.POST:
    #     start_date = datetime.strptime(request.POST['date'], '%Y-%m-%d')
    #     end_date = start_date + timedelta(days=1)

    # if 'daterange' in request.POST and request.POST['daterange']:
    #     selected_date = json.loads(request.POST['daterange'])
    #     if 'startDate' in selected_date and 'endDate' in selected_date:
    #         start_date_str = selected_date['startDate']
    #         end_date_str = selected_date['endDate']

    #         try:
    #             start_date = parse_date(start_date_str)
    #             end_date = parse_date(end_date_str) + timedelta(days=1)
    #         except ValidationError:
    #             pass

    # elif 'date' in request.POST:
    #     date_str = request.POST['date']
    #     try:
    #         start_date = parse_date(date_str)
    #         end_date = start_date + timedelta(days=1)
    #     except ValidationError:
    #         pass

    # print("Parsed start_date:", start_date)
    # print("Parsed end_date:", end_date)


    user_data = request.user
    # user_department = user_data.department

    if user_department == 'telecaller':
        home_leads = Leads.objects.all()
        # related_sources_data = LeadSourceUser.objects.filter(user=user_data)
        related_sources_data = Sources.objects.filter(assign_user= user_data)


        if related_sources_data:
            related_sources = related_sources_data.values_list('lead_source_id', flat=True)
            home_leads = home_leads.filter(lead_source_id__in=related_sources)

        telecaller_assigned_leads = LeadAssignedUser.objects.filter(user=user_data)
        assign_leads_arr = telecaller_assigned_leads.values_list('lead_id', flat=True)

        telecaller_transfer_leads = LeadTransferUser.objects.filter(user=user_data)
        transfer_leads_arr = telecaller_transfer_leads.values_list('lead_id', flat=True)

        telecaller_leads_arr = list(set(assign_leads_arr) | set(transfer_leads_arr))
        home_leads = home_leads.filter(id__in=telecaller_leads_arr)

        telecaller_leads_record = home_leads.all()
        lead_record = telecaller_leads_record.values_list('id', flat=True)

        lead_record = list(set(lead_record))

        # update_leads_arr = Leads.objects.filter(
        #     Q(updated_at__date__gte=start_date) &
        #     Q(updated_at__date__lt=end_date) &
        #     Q(id__in=lead_record)
        # ).select_related('lead_status', 'lead_source').order_by('updated_at')
        update_leads_arr = Leads.objects.filter(
            Q(updated_at__date__gte=start_date) &
            Q(updated_at__date__lt=end_date)
        ).select_related('lead_status_id', 'lead_source_id').order_by('updated_at')

    else:
        update_leads_arr = Leads.objects.filter(
            Q(updated_at__date__gte=start_date) &
            Q(updated_at__date__lt=end_date)
        ).select_related('lead_status_id', 'lead_source_id').order_by('updated_at')


    html = ""
    count = 0

    if update_leads_arr.exists():
        count = update_leads_arr.count()
        for update_lead in update_leads_arr:
            html += f"""
                <tr>
                    <td>{update_lead.id}</td>
                    <td><a href="{reverse('lead_update', args=[update_lead.id])}" target="_blank">{update_lead.name}</a></td>
                    <td>{update_lead.phone}</td>
                    <td>{update_lead.lead_status_id}</td>
                    <td>{update_lead.lead_source_id}</td>
                    <td>{update_lead.created_at}</td>
                    <td>{update_lead.updated_at}</td>
                </tr>
            """
    else:
        html = "<tr><td colspan='6'>No Updated Lead Found</td></tr>"

    return JsonResponse({'html': html, 'count': count})


@login_required
def lead_log_filter(request):
    start_date = end_date = ""
    udetail = UserDetails.objects.get(user=request.user)
    user_department = udetail.department



    # if 'daterange' in request.POST and request.POST['daterange']:
    #     start_date = datetime.strptime(request.POST['daterange']['startDate'], '%Y-%m-%d')
    #     end_date = datetime.strptime(request.POST['daterange']['endDate'], '%Y-%m-%d')
    #     end_date += timedelta(days=1)
    # else:
    #     start_date = datetime.strptime(request.POST['date'], '%Y-%m-%d')
    #     end_date = start_date + timedelta(days=1)

    if 'daterange[startDate]' in request.POST and request.POST['daterange[startDate]']:
        start_date_str = request.POST['daterange[startDate]']
        end_date_str = request.POST['daterange[endDate]']

    print("Received start_date_str:", start_date_str)
    print("Received end_date_str:", end_date_str)

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
    else:
        start_date_str = request.POST.get('date')

        print("Received start_date_str:", start_date_str)

        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = start_date + timedelta(days=1)

    print("Parsed Start Date:", start_date)
    print("Parsed End Date:", end_date)

    user_data = request.user

    if user_department == 'telecaller':
        home_leads = Leads.objects.all()
        # related_sources_data = LeadSourceUser.objects.filter(user=user_data)
        related_sources_data = Sources.objects.filter(assign_user= user_data)


        if related_sources_data.exists():
            related_sources = related_sources_data.values_list('lead_source_id', flat=True)
            home_leads = home_leads.filter(lead_source_id__in=related_sources)

        telecaller_assigned_leads = LeadAssignedUser.objects.filter(user=user_data)
        assign_leads_arr = telecaller_assigned_leads.values_list('lead_id', flat=True)

        telecaller_transfer_leads = LeadTransferUser.objects.filter(user=user_data)
        transfer_leads_arr = telecaller_transfer_leads.values_list('lead_id', flat=True)

        telecaller_leads_arr = list(set(assign_leads_arr) | set(transfer_leads_arr))
        home_leads = home_leads.filter(id__in=telecaller_leads_arr)

        telecaller_leads_record = home_leads.all()
        lead_record = telecaller_leads_record.values_list('id', flat=True)

        lead_record = list(set(lead_record))

        # log_leads_arr = LeadStatusLOG.objects.filter(
        #     created_at__date__gte=start_date,
        #     created_at__date__lt=end_date,
        #     lead_id__in=lead_record
        # ).select_related('user').order_by('created_at')
        log_leads_arr = LeadStatusLOG.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lt=end_date
        ).order_by('created_at')

        user_ids = log_leads_arr.values_list('user_id', flat=True)
        users = User.objects.filter(id__in=user_ids)
    else:
        # log_leads_arr = LeadStatusLOG.objects.filter(
        #     created_at__date__gte=start_date,
        #     created_at__date__lt=end_date
        # ).select_related('user').order_by('created_at')
        log_leads_arr = LeadStatusLOG.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lt=end_date
        ).order_by('created_at')

    user_ids = log_leads_arr.values_list('user_id', flat=True)
    users = User.objects.filter(id__in=user_ids)

    html = ""
    count = 0

    if log_leads_arr.exists():
        count = log_leads_arr.count()
        for log_lead in log_leads_arr:
            change_type = "Field Change" if log_lead.field_change == 1 else "Status Change"
            html += f"""
                <tr>
                    <td>{log_lead.lead_id}</td>
                    <td>{change_type}</td>
                    <td>{log_lead.created_at}</td>
                    <td>{log_lead.user_id}</td>
                </tr>
            """
    else:
        html = "<tr><td colspan='4'>No Log Found</td></tr>"

    return JsonResponse({'html': html, 'count': count})









class DashboardsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context
