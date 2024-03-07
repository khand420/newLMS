

from apps.authentication.models import UserDetails
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from apps.calls.models import Calls
from apps.leads.models import Leads, Sources
# from datetime import timezone

# import pymysql
import psycopg2
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render
from apps.generalsettings.models import TellyCommSettings
import ast



@csrf_exempt
def ivr_logs(request):
    # paginatLimit = 10
    mydata = TellyCommSettings.objects.all().first()
    # print(mydata.outgoing_call_name, '-------------')
    ivr_token = mydata.ivr_token
    # ivr_token = "a83fd6025d590bd4cd9cfdec78638e52"

    if request.method == 'POST':
        print(request.method, '---')
        url = "https://developers.myoperator.co/search"
        data = {
            "token": ivr_token,
            "page_size": 100
        }

        try:
            response = requests.post(url, data=data)
            print(response)
            response.raise_for_status()
            ivr_log = response.json()
        except requests.exceptions.RequestException as e:
            error_msg = 'api_error'
            return JsonResponse({'error_msg': error_msg})

        return render(request, 'ivr_log.html', {'ivr_log': ivr_log})

        # return JsonResponse({'ivr_log': ivr_log})

    return JsonResponse({'error_msg': 'Invalid HTTP method'})


@csrf_exempt
def ivr_user(request):
    # mydata = TellyCommSettings.objects.all()[0]
    # print(mydata.outgoing_call_name, '-------------')

    # userdata = [
    #     {'uuid': '9667088845', 'name': 'Agent 2'},
    #     {'uuid': '9958688445', 'name': 'Agent 1'}
    # ]

    # user_arr = [{'user_id': val['uuid'], 'name': val['name']} for val in userdata]

    # print('user_arr', user_arr)


    userdata = []
    mydata = TellyCommSettings.objects.all().first()

    if mydata:
        names = mydata.outgoing_call_name
        uuids = mydata.outgoing_call_phone
        # print(name,uuid ,'-------------')

        names_list = ast.literal_eval(names)
        phone_list = ast.literal_eval(uuids)


        for name, uuid in zip(names_list, phone_list):
            user_info = {'name': name, 'uuid': uuid}
            userdata.append(user_info)

        # print(userdata)

        names_list = userdata[0]['name']
        uuids_list = userdata[0]['uuid']

        # Create a list of dictionaries in the desired format
        user_arr = [{'user_id': uuid, 'name': name} for name, uuid in zip(names_list, uuids_list)]
        print(user_arr)

        return JsonResponse({'user_arr': user_arr})


@login_required
@csrf_exempt
def ivrinitiate(request):
    udetail = userdetail.objects.get(user=request.user)
    clientid = udetail.uniqueid
    user_department = udetail.department
    mydata = TellyCommSettings.objects.all().first()
    authToken = mydata.auth_token
    numbers = mydata.phones
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        customer = request.POST.get('customer')
        customer = customer.replace("+91", "")
        leadid = request.POST.get('leadid', '')

        print(user_id, customer, leadid, '-----------')

        headers = {
            'Authorization': f'Bearer {authToken}',
            # 'Authorization': 'Bearer AsS57gQP_w-BZonZxbCqG3_i2rn7lmFZYlm_zypbMqCHMg6uABXgUgMUUwBq-qQczJg0HUuLUZo9O3y54UduwbpY9KGRn0z5wllUojcfofQSpkdO441OROYQOiedmLiC',
            'Content-Type': 'application/json',
            'Cookie': 'advanced-api=4n10psfj3ro323v5m8339golqu; _csrf-backend=bc032bf0cfae8a8e88859d9e3920a5daaaf9a405aeb34fd5dcc67f8403ff8d4aa%3A2%3A%7Bi%3A0%3Bs%3A13%3A%22_csrf-backend%22%3Bi%3A1%3Bs%3A32%3A%225rOh_1d8kRJfogWgiQQLfLHnCVhVOA_9%22%3B%7D',
        }

        payload = {
            'agent_number': user_id,
            'virtual_number': numbers,
            'customer_number': customer
        }

        try:
            response = requests.get('http://api.mytelly.in/api/dcp/connect-dcp-call', headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()
            print('ivrinitiate-',response_data )
            if response_data['status'] == 1:
                if leadid:
                    try:
                        leadcall = Calls.objects.filter(lead_id=leadid, status=1, check_status=1).get()
                        if leadcall:
                            leadcall.status = 0
                            leadcall.check_status = 0
                            leadcall.client_id = clientid
                            leadcall.save()
                            print('ivrinitiate working-', leadcall.id)
                        else:
                            lead = Leads.objects.get(id=leadid)
                            telecallerId = request.user.id

                            # if request.user.department_id != 1:
                            if user_department != 'telecaller':
                                # SourcesData = LeadSourceUser.objects.filter(lead_source_id=lead.lead_source_id).first()
                                SourcesData = Sources.objects.filter(leads__id=lead.lead_source_id).first()
                                # source_data = Sources.objects.filter(leads__id=source_id).first()
                                if SourcesData:
                                    # telecallerId = SourcesData.user_id
                                    telecallerId = SourcesData.assign_user.first().id

                            calls = Calls()
                            calls.date = timezone.now()
                            calls.lead_id = leadid
                            calls.lead_status_id = lead.lead_status_id
                            calls.status = 0
                            calls.client_id = clientid
                            calls.check_status = 0
                            calls.today_call = 1
                            calls.telecallerid = telecallerId
                            calls.save()

                    except Calls.DoesNotExist:
                        pass

                return JsonResponse({'message': 'Call Initiated Successfully'})
            else:
                return JsonResponse({'message': response_data['message']})
        except requests.exceptions.RequestException as e:
            return JsonResponse({'message': 'API Error'})

    return JsonResponse({'message': 'Invalid HTTP method'})





# @csrf_exempt
# def ivr_receiver(request):
#     try:
#         # PostgreSQL Database Configuration
#         db_settings = {
#             'dbname': 'master_crm',
#             'user': 'postgres',
#             'password': '123',
#             'host': '127.0.0.1',
#             'port': '',
#         }

#         # Connect to the PostgreSQL Database
#         connection = psycopg2.connect(**db_settings)

#         # Decode the JSON data from the request
#         req_data = json.loads(request.body.decode('utf-8'))

#         # Extract data from the JSON
#         caller = req_data['caller_number']
#         ivr_virtual_number = req_data['vn']
#         call_status = req_data['call_status']

#         lead_source_id = 32

#         if ivr_virtual_number == '9672631927':
#             lead_source_id = 33

#         lead_id = str(timezone.now().strftime('%Y%m%d%H%M%S'))

#         # Check if the caller number exists in the leads table
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM leads WHERE phone LIKE %s", ('%' + caller + '%',))
#             ivf_lead = cursor.fetchall()

#             if not ivf_lead:
#                 # Insert a new lead into the leads table
#                 sql = """
#                 INSERT INTO leads (salutation, name, phone, email, product_id, centre_name, lead_status_id, created_at, updated_at, created_by, lead_source_id, primary_lead_source_id, ivr_virtual_number, ivr_data, ivr_operator)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 """
#                 cursor.execute(
#                     sql,
#                     ('mr', 'IVRLead_' + lead_id, caller, 'ivrlead' + lead_id + '@drnagendra.com', None, 1, 1, timezone.now(), timezone.now(), 'api', lead_source_id, lead_source_id, ivr_virtual_number, json.dumps(req_data), 'mytelly')
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











#     $('.ivrresponse').empty();
#     $("#callivf").show();
#     $("#ivr_customer_number").val(phone);
#     $("#leadid").val(leadid);

#     $('#clicktocall').modal('show');
# }
# $("#callivf").on("click", function(){
#     $(this).hide();
#     $('#ivrload').show();
#     var customer = $('#ivr_customer_number').val();
#     var leadid = $('#leadid').val();
#     var ivruser = $('select#ivr_user_id option:selected').val();
#     //console.log(ivruser+'-------'+customer);

#     $.ajax({
# 		url: 'https://primeivfcrm.in/ivrinitiate',
# 		data: {'user_id': ivruser, 'customer':customer,'leadid':leadid},
# 		dataType: 'json',
# 		method:'post',
# 		success: function(data)
# 		{
#             $('.ivrresponse').empty().append(data.message);
#             $('#ivrload').hide();
# 		}
#     });
#     $("select#ivr_user_id option").prop("selected", false);



# def ivr_receiver(request):
#     try:
#         # MySQL Database Configuration
#         db_settings = {
#             'host': '127.0.0.1',
#             'user': 'root',
#             'password': '',
#             'db': 'ichelon',
#             'charset': 'utf8mb4',
#             'cursorclass': pymysql.cursors.DictCursor,
#         }

#         # Connect to the MySQL Database
#         connection = pymysql.connect(**db_settings)

#         # Decode the JSON data from the request
#         req_data = json.loads(request.body.decode('utf-8'))

#         # Extract data from the JSON
#         caller = req_data['caller_number']
#         ivr_virtual_number = req_data['vn']
#         call_status = req_data['call_status']

#         lead_source_id = 32

#         if ivr_virtual_number == '9672631927':
#             lead_source_id = 33

#         lead_id = timezone.now().strftime('%Y%m%d%H%M%S')

#         # Check if the caller number exists in the leads table
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM leads WHERE phone LIKE %s", ('%' + caller + '%',))
#             ivf_lead = cursor.fetchall()

#             if not ivf_lead:
#                 # Insert a new lead into the leads table
#                 sql = """
#                 INSERT INTO leads (salutation, name, phone, email, product_id, centre_name, lead_status_id, created_at, updated_at, created_by, lead_source_id, primary_lead_source_id, ivr_virtual_number, ivr_data, ivr_operator)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 """
#                 cursor.execute(
#                     sql,
#                     ('mr', 'IVRLead_' + lead_id, caller, 'ivrlead' + lead_id + '@drnagendra.com', None, 1, 1, timezone.now(), timezone.now(), 'api', lead_source_id, lead_source_id, ivr_virtual_number, json.dumps(req_data), 'mytelly')
#                 )
#                 connection.commit()

#                 # Send an email notification
#                 email_to = 'info@drnagendra.com'
#                 subject = 'Drnagendra IVR Lead'
#                 message = f'Hello drnagendra,\nYou have received a new IVR lead. Check here: http://drnagendra.icg-crm.in/'
#                 send_mail(subject, message, 'info@icgcrm.in', [email_to], fail_silently=False)

#                 return HttpResponse('1')  # Success

#         return HttpResponse('0')  # Failure

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return HttpResponse('0')  # Failure
