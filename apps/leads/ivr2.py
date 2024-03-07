import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from datetime import timezone
from calls.models import Calls
from leads.models import Leads, Sources
from generalsettings.models import TellyCommSettings
import ast
from userdetail.models import userdetail



class IvrController:
    # paginatLimit = 10
    mydata = TellyCommSettings.objects.all().first()
    # print(mydata.outgoing_call_name, '-------------')
    ivr_token = mydata.ivr_token
    # ivr_token = "a83fd6025d590bd4cd9cfdec78638e52"
    
    def __invoke(self, request):
        url = "https://developers.myoperator.co/search"
        data = {
            "token": self.ivr_token,
            "page_size": 100,
            "search_key": "Sanjana",
        }
        response = requests.post(url, data=data)
        
        if response.status_code != 200:
            error_msg = 'api_error'
            return render(request, 'ivr_logs/index.html', {'error_msg': error_msg})
        
        ivr_log = response.json()
        return render(request, 'ivr_logs/index.html', {'ivr_log': ivr_log})
    
    def OpIvr_user(self):
        user_arr = []
        url = "https://developers.myoperator.co/user?token=" + self.ivr_token
        response = requests.get(url)
        
        if response.status_code != 200:
            error_msg = response.text
            return JsonResponse({'message': error_msg}, status=400)
        
        # mydata = TellyCommSettings.objects.filter(provider = "My-Operator")[0]
        ivr_user = response.json()
        status = ivr_user['status']
        if status == "success":
            userdata = ivr_user['data']
            for val in userdata:
                user_arr.append({'user_id': val['uuid'], 'name': val['name']})
        return JsonResponse(user_arr, safe=False)
    
    def OpIvrinitiate(self, request):
        udetail = userdetail.objects.get(user=request.user)
        clientid = udetail.uniqueid
        user_department = udetail.department
        # mydata = TellyCommSettings.objects.all()[0]
        mydata = TellyCommSettings.objects.filter(provider = "My-Operator", outgoing_call = "Yes").first()
        authToken = mydata.auth_token
        numbers = mydata.phones
        company_id = mydata.company_id
        public_ivr_id = mydata.public_ivr_id
        secret_token = mydata.secret_token


        user_id = request.POST['user_id']
        customer = request.POST['customer']
        leadid = request.POST.get('leadid', '')
        phonelen = len(customer)
        if phonelen == 12:
            customer = "+" + customer
        if "+91" not in customer:
            customer = "+91" + customer

        url = "https://obd-api.myoperator.co/obd-api-v1"
        data = {
            "company_id": company_id,
            # "company_id": "5f6995b1ad31b625",
            # "secret_token": "4f1a4f720ff3561862fc781468994d22950769693f1a3542be708a9b198d9c7b",
            "secret_token": secret_token,

            "type": "1",
            "user_id": user_id,
            "number": customer,
            "public_ivr_id": public_ivr_id,
            # "public_ivr_id": "5faa3aac63637764",
        }
        headers = {
            "x-api-key": "oomfKA3I2K6TCJYistHyb7sDf0l0F6c8AZro5DJh",
            "Content-Type": "application/json",
        }

        response = requests.post(url, data=json.dumps(data), headers=headers)
        response_data = response.json()
        
        if response_data['status'] == "success":
            if leadid:
                leadcall = Calls.objects.filter(lead_id=leadid, status=1, check_status=1)
                if leadcall.exists():
                    Calls.objects.filter(lead_id=leadid).update(status=0, check_status=0)
                else:
                    lead = Leads.objects.get(id=leadid)
                    call = Calls()
                    call.date = timezone.now()
                    call.lead_id = leadid
                    call.lead_status_id = lead.lead_status_id
                    call.status = 0
                    call.check_status = 0
                    call.today_call = 1
                    call.slot = response_data.get("slot", "")
                    call.telecallerid = user_id
                    call.client_id = clientid
                    call.save()
            return JsonResponse({'message': "Call Initiated Successfully"})
        else:
            return JsonResponse({'message': response_data['details']}, status=400)

    def telly_ivr_user(self):
        # userdata = [
        #     {'uuid': '9718795952', 'name': 'Pooja'},
        #     {'uuid': '8920713781', 'name': 'Pooja Dwarika'}
        # ]
        # user_arr = [{'user_id': val['uuid'], 'name': val['name']} for val in userdata]
        userdata = []
        mydata = TellyCommSettings.objects.filter(provider = "My-Telly",outgoing_call = "Yes").first()
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
        return JsonResponse(user_arr, safe=False)

     
    def telly_ivrinitiate(self, request):
        udetail = userdetail.objects.get(user=request.user)
        clientid = udetail.uniqueid
        user_department = udetail.department
        mydata = TellyCommSettings.objects.filter(provider = "My-Telly")[0]
        authToken = mydata.auth_token
        numbers = mydata.phones

        user_id = request.POST['user_id']
        customer = request.POST['customer']
        customer = customer.replace("+91", "")

        url = "http://api.mytelly.in/api/dcp/connect-dcp-call"
        data = {
            "agent_number": user_id,
            # "virtual_number": "7230019301",
            'virtual_number': numbers,
            "customer_number": customer,
        }
        headers = {
            'Authorization': f'Bearer {authToken}',
            # "Authorization": "Bearer fuI45mC2lRAynUuCYwFBu-Erw5e61hymdlkDhTUNfzgCoGc0w-YsiGM7o5BhElvZAGQ67AjTUIa7aC_9qgTY-JJC2rHPHtEn9s8krXOnXmC28cPxPj3d7mIxYHyFbIEg",
            "Content-Type": "application/json",
            "Cookie": "advanced-api=4n10psfj3ro323v5m8339golqu; _csrf-backend=bc032bf0cfae8a8e88859d9e3920a5daaaf9a405aeb34fd5dcc67f8403ff8d4aa%3A2%3A%7Bi%3A0%3Bs%3A13%3A%22_csrf-backend%22%3Bi%3A1%3Bs%3A32%3A%225rOh_1d8kRJfogWgiQQLfLHnCVhVOA_9%22%3B%7D",
        }

        response = requests.get(url, data=json.dumps(data), headers=headers)
        response_data = response.json()
        
        if response_data['status'] == 1:
            return JsonResponse({'message': "Call Initiated Successfully"})
        else:
            return JsonResponse({'message': json.dumps(response_data['message'])})
    
    def lead_call_log(self, request, phone):
        phone = phone.replace('+91', '')
        url = "https://developers.myoperator.co/search"
        data = {
            "token": self.ivr_token,
            "page_size": 100,
            "search_key": phone,
        }
        response = requests.post(url, data=data)
        
        if response.status_code != 200:
            error_msg = 'api_error'
            return render(request, 'leads/lead_call_logs.html', {'error_msg': error_msg})
        
        ivr_log = response.json()
        return render(request, 'leads/lead_call_logs.html', {'ivr_log': ivr_log})
