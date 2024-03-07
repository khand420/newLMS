# import pymysql
import psycopg2
from django.core.mail import send_mail
from apps.leads.models import Leads, DuplicateLeads
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from apps.generalsettings.models import TellyCommSettings
from apps.authentication.models import UserDetails



def ivr_receiver(request):

    try:

        req_data = json.loads(request.body.decode('utf-8'))

        caller = req_data.get('caller_number', '')
        ivr_virtual_number = req_data.get('vn', '')
        call_status = req_data.get('call_status', '')

        userdata = TellyCommSettings.objects.filter(provider = "My-Telly", phones = ivr_virtual_number)
        if userdata.exists():
            source_id = userdata[0].source_id.id
            client_id = userdata[0].client_id
            # print(source_id, '----------------')
        else:
            print(f"No records found for phones={ivr_virtual_number}")
        name = userdetail.objects.filter(uniqueid = client_id, department = 'client').values('user__username')
        # print(name, '++++++ ')

        # lead_source_id = 32

        # if ivr_virtual_number == '9672631927':
        #     source_id = 33

        # Generate a lead_id (you can customize this logic)
        lead_id = timezone.now().strftime('%Y%m%d%H%M%S')

        ivf_lead = Leads.objects.filter(phone__contains=caller, client_id = client_id).first()

        if not ivf_lead:
            lead = Leads(
                salutation='mr',
                name=f'IVRLead_{lead_id}',
                phone=caller,
                email=f'ivrlead{lead_id}@{name}.com',
                product_id=None,
                centre_name=1,
                lead_status_id=1,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                created_by='api',
                lead_source_id=source_id,
                primary_lead_source_id=source_id,
                client_id=client_id,
                ivr_virtual_number=ivr_virtual_number,
                ivr_data=json.dumps(req_data),
                ivr_operator='mytelly',
            )
            lead.save()

            # Send an email notification
            email_to = f'info@{name}.com'
            subject = f'{name} IVR Lead'
            message = f'Hello {name},\nYou have received a new IVR lead. Check here: http://{name}.icg-crm.in/'
            send_mail(subject, message, 'info@icgcrm.in', [email_to], fail_silently=False)

            return HttpResponse('1')

        if ivf_lead:
            lead = DuplicateLeads(
                salutation='mr',
                name=f'IVRLead_{lead_id}',
                phone=caller,
                email=f'ivrlead{lead_id}@{name}.com',
                product_id=None,
                centre_name=1,
                lead_status_id=1,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                created_by='api',
                lead_source_id=source_id,
                primary_lead_source_id=source_id,
                client_id=client_id,
                ivr_virtual_number=ivr_virtual_number,
                ivr_data=json.dumps(req_data),
                ivr_operator='mytelly',
            )
            lead.save()

            # Send an email notification
            email_to = f'info@{name}.com'
            subject = f'{name} IVR Lead'
            message = f'Hello {name},\nYou have received a Duplicate IVR lead. Check here: http://{name}.icg-crm.in/'
            send_mail(subject, message, 'info@icgcrm.in', [email_to], fail_silently=False)

            return HttpResponse('1')

        return HttpResponse('0')

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return HttpResponse('0')






# @csrf_exempt
# def ivr_receiver(request):
#     try:
#         db_settings = {
#             'dbname': 'master_crm',
#             'user': 'postgres',
#             'password': '123',
#             'host': '127.0.0.1',
#             'port': '',
#         }

#         connection = psycopg2.connect(**db_settings)

#         # Decode the JSON data from the request
#         req_data = json.loads(request.body.decode('utf-8'))

#         data = TellyCommSettings.objects.all().first()
#         # phone = data.phones
#         source_id = data.source_id.id
#         client_id = data.client_id

#         caller = req_data['caller_number']
#         ivr_virtual_number = req_data['vn']
#         call_status = req_data['call_status']

#         # lead_source_id = 32

#         if ivr_virtual_number == '9672631927':
#             source_id = 33

#         lead_id = str(timezone.now().strftime('%Y%m%d%H%M%S'))

#         # Check if the caller number exists in the leads table
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "SELECT * FROM leads WHERE phone LIKE %s", ('%' + caller + '%',))
#             ivf_lead = cursor.fetchall()

#             if not ivf_lead:
#                 # Insert a new lead into the leads table
#                 sql = """
#                 INSERT INTO leads (salutation, name, phone, email, product_id, centre_name, lead_status_id, created_at, updated_at, created_by, lead_source_id, client_id, primary_lead_source_id, ivr_virtual_number, ivr_data, ivr_operator)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 """
#                 cursor.execute(
#                     sql,
#                     ('mr', 'IVRLead_' + lead_id, caller, 'ivrlead' + lead_id + '@drnagendra.com', None, 1, 1, timezone.now(),
#                      timezone.now(), 'api', source_id, client_id, ivr_virtual_number, json.dumps(req_data), 'mytelly')
#                 )
#                 connection.commit()

#                 # Send an email notification (You can use Django's Email API for this)
#                 email_to = 'info@drnagendra.com'
#                 subject = 'Drnagendra IVR Lead'
#                 message = f'Hello drnagendra,<br/> You have received a new IVR lead. <a href="http://drnagendra.icg-crm.in/">Click here to check</a>'
#                 send_mail(subject, message, 'info@icgcrm.in', [email_to])

#                 return JsonResponse({'status': 1})  # Success

#         return JsonResponse({'status': 0})  # Failure

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return JsonResponse({'status': 0})  # Failure


# # Function to send email (You can replace this with Django's Email API)
# def send_mail(subject, message, from_email, recipient_list):
#     from django.core.mail import EmailMessage
#     email = EmailMessage(subject, message, from_email, recipient_list)
#     email.content_subtype = 'html'
#     email.send()


# # {"{\"DTMF\":\"\",\"dealer_id\":515930,\"call_date\":\"2023-07-26\",\"call_time\":\"18:08:29\",\"connected_to\":\"\",\"call_status\":\"NotConnected\",\"call_duration\":0,\"redial_interval\":\"25\",\"call_id\":49739793,\"call_start_time\":1690375109,\"call_pick_time\":0,\"hangup_time\":1690375115,\"local_recording_path\":null,\"call_wait_time\":0,\"caller_number\":9667088845,\"vn\":9672520236,\"agent_name\":\"\",\"dcp_req_id\":null,\"dcp_req_time\":\"\",\"agent_status\":null,\"lega\":\"Disconnected_On_dialling\",\"legb\":\"Disconnected_On_dialling\",\"agent_attended_time\":\"\",\"agent_end_time\":\"\",\"attempted\":\"09667088845-Agent_2,09958688445-Agent_1\",\"agent_location\":\"DELHI_AND_NCR\",\"customer_location\":\"\"}": ""}
# ssh syrecosmetics@216.48.176.156
