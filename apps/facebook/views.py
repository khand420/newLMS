
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from communication.models import Communication
from product.models import Product

from .models import CommunicationFB, SubscriptionsFB, ProductFB, TelecallerFB
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from userdetail.models import userdetail

import json
import requests
from django.http import JsonResponse


@login_required
def facebookSubscriptions_add(request):
    return render(request, 'subscriptionFB/add.html')


@login_required
def facebookSubscriptions(request):

    # subscriptions = SubscriptionsFB.objects.order_by('-id').values('page_id', 'page_name').distinct()
    # paginatLimit = 10
    # page = request.GET.get('page')
    # paginator = Paginator(subscriptions, paginatLimit)
    # subscriptions = paginator.get_page(page)
    try:
        udetail = userdetail.objects.get(user_id=request.user.id)
        # clientid = udetail.uniqueid
        subscriptions = SubscriptionsFB.objects.filter(client_id=udetail.uniqueid).all().order_by('-id').values('page_id', 'page_name').distinct()


        paginator = Paginator(subscriptions, 5)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except SubscriptionsFB.DoesNotExist:
        page_obj:None  
    return render(request, 'subscriptionFB/index.html', {'subscriptions': subscriptions, 'page_obj':page_obj})


# App ID: 140745182240809
# App Secret: 14235b543231819b24b2adb7c28eb8b1


@login_required
def fb_save_subscription(request):
    print('---fb_save_subscription-----',request.method == 'POST')
    if request.method == 'POST':
        page_access_token = request.POST.get('page_access_token')
        page_id = request.POST.get('page_id')
        page_name = request.POST.get('page_name')

        if page_access_token and page_id and page_name:
            # app_id = "140745182240809"
            # app_id = "347199637039934"
            # app_secret = "c6ab498008829e813b0d5a3d47d9367c"
            app_id = "904530936725782" 
            app_secret = "ec87fa0f8adf8337e4fa7f1c9b09343b"

            graph_url = f"https://graph.facebook.com/oauth/access_token?client_id={app_id}&client_secret={app_secret}&grant_type=fb_exchange_token&fb_exchange_token={page_access_token}"

            response = requests.get(graph_url)
            data = response.json()
            print(data)
            long_token = data["access_token"]

            graph_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={long_token}"
            response = requests.get(graph_url)
            data = response.json()
            final_token = data["access_token"]

            access_token = final_token

            SubscriptionsFB.objects.filter(page_id=page_id).delete()

            entity = SubscriptionsFB(
                page_id=page_id,
                page_name=page_name,
                access_token=page_access_token,
                client_id=request.user.userdetail.uniqueid
            )
            entity.save()

            response = {'status': 1}
        else:
            response = {'status': 2}

        return JsonResponse(response)
    else:
        return JsonResponse({'status': 2})


def fb_save_page_form(request):
    result = {}
    form_html = '<option value="">Select Form</option>'
    fbpage_id = request.GET.get('fbpage_id')
    fbform_id = request.GET.get('fbform_id')
    access_token = SubscriptionsFB.objects.filter(page_id=fbpage_id).values("access_token").first()

    if access_token and access_token["access_token"]:
        access_token = access_token["access_token"]
        url = f"https://graph.facebook.com/v8.0/{fbpage_id}/leadgen_forms?pretty=0&limit=1000&access_token={access_token}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(data)

            if "data" in data and data["data"]:
                formdata = data["data"]

                for forms in formdata:
                    selected = ""

                    if fbform_id and fbform_id == forms["id"]:
                        selected = "selected='selected'"

                    form_html += f'<option {selected} formid="{forms["id"]}" value="{forms["id"]}">{forms["name"]}</option>'

                result["message"] = "success"
                result["form_html"] = form_html
            else:
                result["message"] = "No forms found!"
        else:
            result["message"] = response.text
    else:
        result["message"] = "Forms Not Found"

    return JsonResponse(result)



# @login_required
# def fb_save_subscription(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     clientid = udetail.uniqueid
#     if request.method == 'POST':
#         page_access_token = request.POST.get('page_access_token')
#         page_id = request.POST.get('page_id')
#         page_name = request.POST.get('page_name')

#         if page_access_token and page_id and page_name:
#             app_id = "904530936725782"
#             app_secret = "ec87fa0f8adf8337e4fa7f1c9b09343b"
#             graph_url = f"https://graph.facebook.com/oauth/access_token?client_id={app_id}&client_secret={app_secret}&grant_type=fb_exchange_token&fb_exchange_token={access_token}"

#             response = requests.get(graph_url)
#             data = response.json()
#             print(data)
#             long_token = data["access_token"]

#             graph_url = f"https://graph.facebook.com/{id}?fields=access_token&access_token={long_token}"
#             response = requests.get(graph_url)
#             data = response.json()
#             final_token = data["access_token"]

#             access_token = final_token

#             # appId = "904530936725782"
#             # appSecret = "ec87fa0f8adf8337e4fa7f1c9b09343b"
#             # graph_url = f"https://graph.facebook.com/oauth/access_token?client_id="{appId}"&client_secret="{appSecret}"&grant_type=fb_exchange_token&fb_exchange_token="{accessToken}"
            
#             # r =  json_decode(file_get_contents(graph_url));
#             # longtoken=$r->access_token;
#             # r=json_decode(file_get_contents("https://graph.facebook.com/{$id}?fields=access_token&access_token={$longtoken}")); // get user id
#             # finaltoken=$r->access_token;
#             # accessToken =  $finaltoken;

#             # Perform the necessary operations to save the subscription

#             SubscriptionsFB.objects.filter(page_id=page_id).delete()

#             entity = SubscriptionsFB(
#                 page_id=page_id,
#                 page_name=page_name,
#                 access_token=page_access_token,
#                 client_id = clientid
#             )
#             entity.save()
#             response = {'status': 1}
#         else:
#             response = {'status': 2}

#         return JsonResponse(response)
#     else:
#         return JsonResponse({'status': 2})


# @login_required
# def fb_save_subscription(request):
#     if request.method == 'POST':
#         page_access_token = request.POST.get('page_access_token')
#         page_id = request.POST.get('page_id')
#         page_name = request.POST.get('page_name')

#         if page_access_token and page_id and page_name:
#             app_id = "904530936725782"
#             app_secret = "ec87fa0f8adf8337e4fa7f1c9b09343b"

#             # Exchange the short-lived access token for a long-lived one
#             graph_url = f"https://graph.facebook.com/oauth/access_token?client_id={app_id}&client_secret={app_secret}&grant_type=fb_exchange_token&fb_exchange_token={page_access_token}"
#             response = requests.get(graph_url)
#             data = response.json()
#             print(data)
#             long_token = data["access_token"]

#             # Retrieve the final access token for the user
#             graph_url = f"https://graph.facebook.com/{page_id}?fields=access_token&access_token={long_token}"
#             response = requests.get(graph_url)
#             data = response.json()
#             final_token = data["access_token"]

#             access_token = final_token

#             # Perform the necessary operations to save the subscription

#             SubscriptionsFB.objects.filter(page_id=page_id).delete()

#             entity = SubscriptionsFB(
#                 page_id=page_id,
#                 page_name=page_name,
#                 access_token=page_access_token,
#                 client_id=request.user.userdetail.uniqueid
#             )
#             entity.save()

#             response = {'status': 1}
#         else:
#             response = {'status': 2}

#         return JsonResponse(response)
#     else:
#         return JsonResponse({'status': 2})
    


def facebookSubscriptions_delete(request, id):
    if request.method == 'POST' and id:
        SubscriptionsFB.objects.filter(id=id).delete()
        messages.success("Facebook Subscription has been deleted successfully")
    else:
        messages.error("Unable to delete this subscription. Please try again later")
    return redirect('facebookSubscriptions')


def facebookProducts(request):
    paginat_limit = 10
    # productfbforms = ProductFB.objects.order_by('-id').all()
    try:
        udetail = userdetail.objects.get(user_id=request.user.id)
        # clientid = udetail.uniqueid
        productfbforms = ProductFB.objects.filter(client_id=udetail.uniqueid).all().order_by('-id')


        paginator = Paginator(productfbforms, 5)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except ProductFB.DoesNotExist:
        page_obj:None  
    context = {
        'productfbforms': productfbforms
    }
    return render(request, 'productFB/index.html', context)



def facebookProducts_add(request):
    products = Product.objects.filter(status='active').order_by('-id').all()
    subscriptions = SubscriptionsFB.objects.order_by('-id').all()
    context = {
        'products': products,
        'subscriptions': subscriptions
    }
    return render(request, 'productFB/add.html', context)

def store(request):
    data = request.POST
    productforms = ProductFB()
    product = Product.objects.get(pk=data["product_id"])
    fbpage = SubscriptionsFB.objects.get(pk=data["fbpage_id"])
    fbform = data["page_form_id"]
    
    productforms.product_id = product.id
    productforms.product_name = product.name
    productforms.fbpage_id = fbpage.id
    productforms.fbpage_name = fbpage.name
    productforms.fbform_id = fbform.id
    productforms.fbform_name = fbform.name
    productforms.status = data["status"]
    
    productforms.save()
    messages.success(request, 'Product FB Form has been added successfully')
    return redirect('facebookProducts.add')

def facebookProducts_edit(request, id):
    products = Product.objects.filter(status='active').order_by('-id').all()
    subscriptions = SubscriptionsFB.objects.order_by('-id').all()
    productforms = ProductFB.objects.get(pk=id)
    context = {
        'products': products,
        'subscriptions': subscriptions,
        'productforms': productforms
    }
    return render(request, 'productFB/edit.html', context)

def update(request):
    data = request.POST
    productforms = ProductFB.objects.get(pk=data["id"])
    product = Product.objects.get(pk=data["product_id"])
    fbpage = SubscriptionsFB.objects.get(pk=data["fbpage_id"])
    fbform = data["page_form_id"]
    
    productforms.product_id = product.id
    productforms.product_name = product.name
    productforms.fbpage_id = fbpage.id
    productforms.fbpage_name = fbpage.name
    productforms.fbform_id = fbform.id
    productforms.fbform_name = fbform.name
    productforms.status = data["status"]
    
    productforms.save()
    messages.success(request, 'Product FB Form has been updated successfully')
    return redirect('facebookProducts.edit', id=data["id"])


def facebookTelecallers(request):
    paginat_limit = 10
    # Telecallerfbforms = TelecallerFB.objects.order_by('-id').all()
    try:
        udetail = userdetail.objects.get(user_id=request.user.id)
        # clientid = udetail.uniqueid
        telecallerfbforms = TelecallerFB.objects.filter(client_id=udetail.uniqueid).all().order_by('-id')


        paginator = Paginator(telecallerfbforms, 5)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except TelecallerFB.DoesNotExist:
        page_obj:None  
    context = {
        'telecallerfbforms': page_obj,
    }
    return render(request, 'telecallerFB/index.html', context)



def facebookTelecallers_add(request):
    user_id = request.user.id
    telecaller_id = userdetail.objects.get(user_id=request.user.id)
    # print(user_id, telecaller_id, timezone.now(), '----------')
    clientid = telecaller_id.uniqueid
    user_department = telecaller_id.department

    # telecaller_users = User.objects.filter(department_id=1).exclude(id=userData.id).values('id', 'name')
    telecallers = userdetail.objects.filter(uniqueid=clientid, department='telecaller').values('user_id', 'user__username')
    # telecallers = Telecaller.objects.filter(status='active').order_by('-id').all()
    # assigned_lead = LeadAssignedUser.objects.filter(lead_id=lead_id).order_by('-id').annotate(
    # assigned_by_name=F('user_id__username')).values('lead_id', 'user_id', 'assigned', 'created_at', 'assigned_by_name')
    subscriptions = SubscriptionsFB.objects.order_by('-id').all()
    context = {
        'telecallers': telecallers,
        'subscriptions': subscriptions
    }
    return render(request, 'telecallerFB/add.html', context)

def store(request):
    data = request.POST
    telecallerforms = TelecallerFB()
    telecaller = telecaller.objects.get(pk=data["telecaller_id"])
    fbpage = SubscriptionsFB.objects.get(pk=data["fbpage_id"])
    fbform = data["page_form_id"]
    
    telecallerforms.telecaller_id = telecaller.id
    telecallerforms.telecaller_name = telecaller.name
    telecallerforms.fbpage_id = fbpage.id
    telecallerforms.fbpage_name = fbpage.name
    telecallerforms.fbform_id = fbform.id
    telecallerforms.fbform_name = fbform.name
    telecallerforms.status = data["status"]
    
    telecallerforms.save()
    messages.success(request, 'telecaller FB Form has been added successfully')
    return redirect('facebooktelecallers.add')

def facebookTelecallers_edit(request, id):
    user_id = request.user.id
    telecaller_id = userdetail.objects.get(user_id=request.user.id)
    # print(user_id, telecaller_id, timezone.now(), '----------')
    clientid = telecaller_id.uniqueid
    user_department = telecaller_id.department

    # telecaller_users = User.objects.filter(department_id=1).exclude(id=userData.id).values('id', 'name')
    telecallers = userdetail.objects.filter(uniqueid=clientid, department='telecaller').values('user_id', 'user__username')

    # telecallers = telecaller.objects.filter(status='active').order_by('-id').all()
    subscriptions = SubscriptionsFB.objects.order_by('-id').all()
    telecallerforms = TelecallerFB.objects.get(pk=id)
    context = {
        'telecallers': telecallers,
        'subscriptions': subscriptions,
        'telecallerforms': telecallerforms
    }
    return render(request, 'telecallerFB/edit.html', context)

def update(request):
    data = request.POST
    telecallerforms = TelecallerFB.objects.get(pk=data["id"])
    telecaller = telecaller.objects.get(pk=data["telecaller_id"])
    fbpage = SubscriptionsFB.objects.get(pk=data["fbpage_id"])
    fbform = data["page_form_id"]
    
    telecallerforms.telecaller_id = telecaller.id
    telecallerforms.telecaller_name = telecaller.name
    telecallerforms.fbpage_id = fbpage.id
    telecallerforms.fbpage_name = fbpage.name
    telecallerforms.fbform_id = fbform.id
    telecallerforms.fbform_name = fbform.name
    telecallerforms.client_id = telecaller.client_id

    telecallerforms.status = data["status"]
    
    telecallerforms.save()
    messages.success(request, 'telecaller FB Form has been updated successfully')
    return redirect('facebooktelecallers.edit', id=data["id"])


@login_required
def facebookCommunication(request):
    try:
        udetail = userdetail.objects.get(user_id=request.user.id)
        # clientid = udetail.uniqueid
        commfbforms = CommunicationFB.objects.filter(
            client_id=udetail.uniqueid).all().order_by('-id')


        paginator = Paginator(commfbforms, 5)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except CommunicationFB.DoesNotExist:
        page_obj:None  
    return render(request, "communicationFB/index.html", {"commfbforms": commfbforms, 'page_obj': page_obj})


@login_required
def facebookCommunication_add(request):
    communication = Communication.objects.filter(status='active').order_by('-id').all()
    subscriptions = SubscriptionsFB.objects.values("page_id").annotate().order_by('-id')
    return render(request, 'communicationFB/add.html', {"subscriptions": subscriptions, "Communication": communication})

@login_required
def store(request):
    if request.method == "POST":
        data = request.POST
        commforms = CommunicationFB()
        commforms.communication_id = data["comm_id"]
        commforms.communication_name = data["comm_name"]
        commforms.fbpage_id = data["fbpage_id"]
        commforms.fbpage_name = data["fbpage_name"]
        commforms.fbform_id = data["page_form_id"]
        commforms.fbform_name = data["page_form_name"]
        commforms.status = data["status"]
        commforms.created_at = timezone.now()
        commforms.created_by = request.user.id
        commforms.updated_at = timezone.now()
        commforms.updated_by = request.user.id
        commforms.save()
        messages.success("Communication FB Form has been added successfully")
        return redirect('facebookCommunication.add')
    else:
        messages.error("Invalid request method")
        return redirect('facebookCommunication.add')

@login_required
def facebookCommunication_edit(request, id):
    communication = Communication.objects.filter(status='active').order_by('-id').all()
    subscriptions = SubscriptionsFB.objects.values("page_id").annotate().order_by('-id')
    commforms = CommunicationFB.objects.get(id=id)
    return render(request, "communicationFB/edit.html", {"commforms": commforms, "subscriptions": subscriptions, "Communication": communication})

@login_required
def update(request):
    if request.method == "POST":
        data = request.POST
        commforms = CommunicationFB.objects.get(id=data["id"])
        commforms.communication_id = data["comm_id"]
        commforms.communication_name = data["comm_name"]
        commforms.fbpage_id = data["fbpage_id"]
        commforms.fbpage_name = data["fbpage_name"]
        commforms.fbform_id = data["page_form_id"]
        commforms.fbform_name = data["page_form_name"]
        commforms.status = data["status"]
        commforms.updated_at = timezone.now()
        commforms.updated_by = request.user.id
        commforms.save()
        messages.success("message", "Communication FB Form has been updated successfully")
        return redirect('facebookCommunication.edit', id=data["id"])
    else:
        messages.error("error", "Invalid request method")
        return redirect('facebookCommunication.edit', id=data["id"])








# def fb_save_page_form(request):
#     result = {}
#     form_html = '<option value="">Select Form</option>'
#     fbpage_id = request.GET.get('fbpage_id')
#     fbform_id = request.GET.get('fbform_id')
#     access_token = SubscriptionsFB.objects.filter(page_id=fbpage_id).values("access_token").first()
    
#     if access_token and access_token["access_token"]:
#         access_token = access_token["access_token"]
#         url = f"https://graph.facebook.com/v8.0/{fbpage_id}/leadgen_forms?pretty=0&limit=1000&access_token={access_token}"
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             data = response.json()
            
#             if "data" in data and data["data"]:
#                 formdata = data["data"]
                
#                 for forms in formdata:
#                     selected = ""
                    
#                     if fbform_id and fbform_id == forms["id"]:
#                         selected = "selected='selected'"
                    
#                     form_html += f"<option {selected} formid='{forms['id']}' value='{json.dumps({'id': forms['id'], 'name': forms['name']})}'>{forms['name']}</option>"
                
#                 result["message"] = "success"
#                 result["form_html"] = form_html
#             else:
#                 result["message"] = "No forms found!"
#         else:
#             result["message"] = response.text
#     else:
#         result["message"] = "Forms Not Found"
    
#     return JsonResponse(result)













def telecaller_fb_page_form(request):
    result = {}
    form_html = '<option value="">Select Form</option>'
    fbpage_id = request.GET.get('fbpage_id')
    access_token = SubscriptionsFB.objects.filter(page_id=fbpage_id).values("access_token").first()
    
    if access_token and access_token["access_token"]:
        access_token = access_token["access_token"]
        url = f"https://graph.facebook.com/v8.0/{fbpage_id}/leadgen_forms?pretty=0&limit=1000&access_token={access_token}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if "data" in data and data["data"]:
                formdata = data["data"]
                
                for forms in formdata:
                    form_html += f"<option formid='{forms['id']}' value='{forms['id']}'>{forms['name']}</option>"
                
                result["message"] = "success"
                result["form_html"] = form_html
            else:
                result["message"] = "No forms found!"
        else:
            result["message"] = response.text
    else:
        result["message"] = "Forms Not Found"
    
    return JsonResponse(result)


def multiple_fb_forms(fbpage_id, fbform_id):
    result = {}
    form_html = ''
    access_token = SubscriptionsFB.objects.filter(page_id=fbpage_id).values("access_token").first()
    
    if access_token and access_token["access_token"]:
        access_token = access_token["access_token"]
        url = f"https://graph.facebook.com/v8.0/{fbpage_id}/leadgen_forms?pretty=0&limit=1000&access_token={access_token}"
        response = requests.get(url)
        
        if response.status_code == 200:
            form_list_arr = []
            data = response.json()
            
            if "data" in data and data["data"]:
                formdata = data["data"]
                fbform_id_arr = fbform_id.split(",")
                
                for forms in formdata:
                    if forms["id"] in fbform_id_arr:
                        form_list_arr.append(forms["name"])
                
                if form_list_arr:
                    form_list_arr = ",".join(form_list_arr)
                
                result["message"] = "success"
                result["form_list"] = form_list_arr
            else:
                result["message"] = "No form found!"
        else:
            result["message"] = response.text
    else:
        result["message"] = "Form Not Found"
    
    return result


def update_telecaller_fb_page_form(request):
    result = {}
    form_html = '<option value="">Select Form</option>'
    fbpage_id = request.GET.get('fbpage_id')
    fbform_id = request.GET.get('fbform_id')
    access_token = SubscriptionsFB.objects.filter(page_id=fbpage_id).values("access_token").first()
    
    if access_token and access_token["access_token"]:
        access_token = access_token["access_token"]
        url = f"https://graph.facebook.com/v8.0/{fbpage_id}/leadgen_forms?pretty=0&limit=1000&access_token={access_token}"
        response = requests.get(url)
        
        if response.status_code == 200:
            form_list_arr = []
            data = response.json()
            
            if "data" in data and data["data"]:
                formdata = data["data"]
                fbform_id_arr = fbform_id.split(",")
                
                for forms in formdata:
                    selected = ""
                    
                    if forms["id"] in fbform_id_arr:
                        selected = "selected='selected'"
                    
                    form_html += f"<option {selected} formid='{forms['id']}' value='{forms['id']}'>{forms['name']}</option>"
                
                result["message"] = "success"
                result["form_html"] = form_html
            else:
                result["message"] = "No forms found!"
        else:
            result["message"] = response.text
    else:
        result["message"] = "Forms Not Found"
    
    return JsonResponse(result)
