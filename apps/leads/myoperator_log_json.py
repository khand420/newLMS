from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.core.mail import send_mail
import json
from datetime import datetime
from .models import Leads, DuplicateLeads
from template.models import template
from apps.calls.models import SMScount
import requests
from apps.generalsettings.models import TellyCommSettings
from apps.authentication.models import UserDetails



@csrf_exempt
def ivr_webhook(request):
    if request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode('utf-8'))
            myoperator_data = json.loads(req_data.get('myoperator', '{}'))

            caller = myoperator_data.get('_cr', '')

            call_type = myoperator_data.get('_ev', '')
            call_status = myoperator_data.get('_su', '')

            userdata = TellyCommSettings.objects.filter(provider = "My-Operator", phones = call_type)
            if userdata.exists():
                source_id = userdata[0].source_id.id
                client_id = userdata[0].client_id
                virtualNum = userdata[0].phones

                # print(source_id, '----------------')
            else:
                print(f"No records found for phones={call_type}")
            name = userdetail.objects.filter(uniqueid = client_id, department = 'client').values('user__username')



            lead_id = Leads.objects.filter(phone__contains=caller, client_id = client_id).first().id

            if call_type == '1':
                if '+' not in caller:
                    caller = '+91' + caller

                data = {
                    'salutation': {lead_id},
                    'product_id': {lead_id.lead_product_id},
                    'centre_name': {lead_id.centre_name},
                    'name': f'IVRLead_{lead_id}',
                    'phone': caller,
                    'email': f'ivrlead{lead_id}@{name}.com',
                    'lead_source_id': {source_id},
                    'lead_status_id': 1,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now(),
                    'created_by': 'api',
                    'ivr_virtual_number': virtualNum,
                    'ivr_data': json.dumps(req_data),
                    'ivr_operator': 'myoperator',
                    'client_id': client_id,
                }

                send_whatsapp = False

                if not lead_id.exists():
                    try:
                        Leads.objects.create(**data)
                    except IntegrityError:
                        DuplicateLeads.objects.create(**data)

                email_to = 'info@{name}.com'
                subject = '{name} IVR Lead'
                message = f'Hello {name},<br/>You have received a new IVR lead. <a href="https://{name}crm.in/">Click here to check</a>'
                send_email(email_to, subject, message)

                # if send_whatsapp:
                #     send_whatsapp_message(caller, call_status)

                # if call_status == 2:
                #     sms_template = template.objects.get(id=9)
                #     whatsapp_template = template.objects.get(id=26)
                # else:
                #     sms_template = template.objects.get(id=4)
                #     whatsapp_template = template.objects.get(id=15)

                # if sms_template.message:
                #     send_sms(caller, sms_template.message)

                # if whatsapp_template:
                #     send_whatsapp_msg(caller, whatsapp_template.name, general_data={})

                return HttpResponse('1')
            else:
                return HttpResponse('0')
        except Exception as e:
            return HttpResponse(str(e))
    else:
        return HttpResponse('Invalid Request Method')



def send_email(to, subject, message):
    from_email = 'info@{name}crm.in'
    headers = {
        'From': from_email,
        'Reply-To': from_email,
        'X-Mailer': 'Ichelon',
    }

    try:
        send_mail(subject, '', from_email, [to], html_message=message, fail_silently=False, headers=headers)
    except Exception as e:
        print(f'Error sending email: {str(e)}')



# def send_sms(mobile, message):
#     # Implement your SMS sending logic here
#     # Use a third-party SMS gateway or service

#     # Example code to send SMS using a gateway (replace with actual code)
#     sms_url = "https://example-sms-gateway.com/send"
#     sms_data = {
#         'mobile': mobile,
#         'message': message,
#         'api_key': 'your_api_key_here',  # Replace with your API key
#     }

#     try:
#         response = requests.post(sms_url, data=sms_data)
#         if response.status_code == 200:
#             sms_response = response.text
#             # Handle the SMS response as needed
#             return sms_response
#         else:
#             # Handle the error if the SMS request fails
#             return None
#     except Exception as e:
#         # Handle exceptions, e.g., network errors
#         return None

# def send_whatsapp_msg(mobile, template_name, general_data):
#     # Implement your WhatsApp message sending logic here
#     # Use a third-party WhatsApp API

#     # Example code to send WhatsApp message (replace with actual code)
#     whatsapp_api_url = "https://example-whatsapp-api.com/send_message"
#     whatsapp_data = {
#         'mobile': mobile,
#         'template_name': template_name,
#         'params': json.dumps(general_data),
#         'api_key': 'your_api_key_here',  # Replace with your API key
#     }

#     try:
#         response = requests.post(whatsapp_api_url, data=whatsapp_data)
#         if response.status_code == 200:
#             whatsapp_response = response.text
#             # Handle the WhatsApp response as needed
#             return whatsapp_response
#         else:
#             # Handle the error if the WhatsApp request fails
#             return None
#     except Exception as e:
#         # Handle exceptions, e.g., network errors
#         return None

# def send_whatsapp_message(mobile, call_status):
    # Implement logic to send WhatsApp message based on call_status
    # Use a third-party WhatsApp API

    # if call_status == 2:
    #     template_name = "template_name_2"
    #     general_data = {
    #         'param1': 'value1',
    #         'param2': 'value2',
    #         # Add more parameters as needed for your WhatsApp template
    #     }
    #     send_whatsapp_msg(mobile, template_name, general_data)
    # else:
    #     template_name = "template_name_1"
    #     general_data = {
    #         'param1': 'value1',
    #         'param2': 'value2',
    #         # Add more parameters as needed for your WhatsApp template
    #     }
    #     send_whatsapp_msg(mobile, template_name, general_data)
