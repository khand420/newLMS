from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Leads, Sources, Stage, LeadType, StageQuestions, LeadScores, LeadAssignedUser, LeadTransferUser, LeadAttachments, LeadComments, LeadStatusLOG, DeletedLead, DuplicateLeads
from product.models import Product
from calls.models import Calls
from timeslot.models import timeslot
from .forms import LeadCreate, StageCreate, SourceCreate, LeadTypeCreate
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import site
# from userdetail import models as userdetail
from userdetail.models import userdetail
from django.contrib import messages
from django.utils.text import slugify
import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import re
# from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum
# from datetime import datetime
from django.urls import reverse
from location.models import Location

import json
from django.views.decorators.csrf import csrf_exempt


# from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
import uuid
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# from .helpers import get_status_id
from .func import  get_status_id, get_lead_by_id , get_product_by_id, get_source_by_id, get_source_user, get_status_by_id, get_transferred_user, get_transferredto_user, get_type_by_id
from django.core.exceptions import ObjectDoesNotExist


from django.core.serializers.json import DjangoJSONEncoder


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Stage):
            return str(obj)  # Serialize the Stage object as a string
        if isinstance(obj, Product):
            return obj.name  # Serialize the Product object using its name
        if isinstance(obj, Sources):
            return obj.name  # Serialize the Sources object using its name
        if isinstance(obj, LeadType):
            return obj.name
        # Add similar handling for other custom objects as needed
        return super().default(obj)
    
# @login_required
# def leadlisting(request):
#     # Fetching user details
#     user_data = request.user
#     udetail = userdetail.objects.get(user_id=user_data.id)
#     clientid = udetail.uniqueid
#     shelf = Leads.objects.filter(client_id=udetail.uniqueid).order_by('-id')

#     # telecaller_users = User.objects.filter(department_id=1).exclude(id=user_data.id).values('id', 'name')
#     telecallers_id = userdetail.objects.filter(
#         uniqueid=clientid, department='telecaller').values_list('user_id', flat=True)
#     telecaller_users = User.objects.filter(id__in=telecallers_id)
#     print(telecaller_users)

#     statuses = Stage.objects.filter(status='active').values('id', 'name')
#     types = LeadType.objects.all().values('id', 'name')
#     products = Product.objects.all().values('id', 'name')
#     # product_name = get_product_by_id(lead.product_id) if lead.product_id else ''
#     sources = Sources.objects.all().values('id', 'name')

#     drid = user_data.id
#     leaddata = {}
#     if 'edit' in request.META.get('HTTP_REFERER', ''):
#         pagerest = request.session.get('pagerest')
#         leaddata = request.session.get('leaddata')
#         del request.session['leaddata']
#     else:
#         pagerest = "false"

#     leads = Leads.objects.exclude(lead_status_id=25)

#     if request.is_ajax():
#         request.session['leaddata'] = {
#             'searchText': request.POST.get('searchText'),
#             'status': request.POST.get('status'),
#             'type': request.POST.get('type'),
#             'product': request.POST.get('product'),
#             'source': request.POST.get('source'),
#             'creation_date_sort': request.POST.get('creation_date_sort'),
#             'filter_created_date': request.POST.get('filter_created_date'),
#             'filter_updated_date': request.POST.get('filter_updated_date'),
#             'filter_date_range': request.POST.get('filter_date_range'),
#             'filter_update_range': request.POST.get('filter_update_range'),
#             'locationq': request.POST.get('locationq'),
#             'star_sort': request.POST.get('star_sort'),
#             'telecaller': request.POST.get('telecaller'),
#             'offsetval': request.POST.get('offsetval'),
#         }

#         # Fetching filters from POST data
#         search_text = request.POST.get('searchText')
#         status = request.POST.get('status')
#         lead_type = request.POST.get('type')
#         product = request.POST.get('product')
#         lead_source = request.POST.get('source')
#         filter_created_date = request.POST.get('filter_created_date')
#         filter_updated_date = request.POST.get('filter_updated_date')
#         filter_date_range = request.POST.get('filter_date_range')
#         filter_update_range = request.POST.get('filter_update_range')
#         locationq = request.POST.get('locationq')

#         # Filtering leads based on filters
#         leads = leads.filter(client_id=clientid)
#         # product_id = int(product) if product else None

#         if search_text:
#             leads = leads.filter(Q(name__icontains=search_text) | Q(phone_number__icontains=search_text))

#         if status:
#             leads = leads.filter(lead_status_id=status)

#         if lead_type:
#             leads = leads.filter(lead_type_id=lead_type)

#         if product:
#             leads = leads.filter(product_id=product)

#         if lead_source:
#             leads = leads.filter(lead_source_id=lead_source)

#         if filter_created_date:
#             leads = leads.filter(created_at__date=filter_created_date)

#         if filter_updated_date:
#             leads = leads.filter(updated_at__date=filter_updated_date)

#         if filter_date_range:
#             leads = leads.filter(created_at__range=filter_date_range.split(','))

#         if filter_update_range:
#             leads = leads.filter(updated_at__range=filter_update_range.split(','))

#         if locationq:
#             leads = leads.filter(city__icontains=locationq)

#         # Fetching leads assigned to the telecaller
#         telecaller_id = request.POST.get('telecaller')
#         if telecaller_id:
#             telecaller_assigned_leads = LeadAssignedUser.objects.filter(user_id=telecaller_id).values_list('lead_id', flat=True)
#             leads = leads.filter(id__in=telecaller_assigned_leads)

#         # Sorting leads
#         creation_date_sort = request.POST.get('creation_date_sort')
#         if creation_date_sort:
#             leads = leads.order_by('created_at' if creation_date_sort == 'asc' else '-created_at')
#         else:
#             leads = leads.order_by('-id')

#         # Prepare data for response

#         lead_data = []
#         for lead in leads:
#             print(lead, '------------')
#             lead_id = ''
#             if lead.is_transfer == 1:
#                 lead_id += '<span class="taglabel"><i class="fa fa-exclamation-circle" title="Transferred by ' + get_transferred_user(lead.id) + ' to ' + get_transferredto_user(lead.id) + '" aria-hidden="true"></i></span>'
#             lead_id += str(lead.id)
#             # product_name = get_product_by_id(lead.product_id)
#             # print(product_name,'----------')
#             # product_id = lead.product_id if lead.product_id else None
#             # product_name = get_product_by_id(product_id) if product_id else ''
#             product_id = lead.product_id if lead.product_id else None
#             product_name = get_product_by_id(product_id) if product_id else ''


#             lead_data.append({
#                 # 'product': get_product_by_id(lead.product_id) if lead.product_id else '',
#                 'product': product_name,
#                 # 'product': get_product_by_id(lead.product_id).name if lead.product_id else '',
#                 'leadid': lead_id,
#                 'date': lead.created_at.strftime('%Y-%m-%d %H:%M:%S'), 
#                 'city': lead.city.capitalize(),
#                 'name': lead.name.capitalize(),
#                 # product_name = get_product_by_id(lead.product_id) if lead.product_id else ''
#                 # 'product':get_product_by_id(lead.product_id).name if lead.product_id else ''
#                 # 'product':get_product_by_id(lead.product_id) if lead.product_id else ''
           
           

#                 'updated_date': lead.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
#                 'source': get_source_by_id(lead.lead_source_id).name + '<a href="#" data-toggle="tooltip" title="' + get_source_user(lead.lead_source_id) + '"><i class="fa fa-info-circle"></i></a>' if lead.lead_source_id else '',
#                 'stage':get_status_by_id(lead.lead_status_id).name if lead.lead_status_id else '',
#                 'keyword': lead.gkeyword if lead.gkeyword else ''
#             })
#             print(lead_data, "*******8")

#         # return JsonResponse({'data': lead_data})
#         leadid = str(lead.id)
#         if lead.is_transfer or not lead.is_assigned:
#             if lead.lead_status_id:
#                 transferred_by = "Transferred User"  # Replace with your logic to get transferred user
#                 transferred_to = "Transferred To User"  # Replace with your logic to get transferred to user
#                 leadid = '<span class="taglabel"><i class="fa fa-exclamation-circle" title="Transferred by {} to {}"></i></span>{}'.format(
#                     transferred_by, transferred_to, lead.id
#                 )
#         source = ''
#         if lead.lead_source:
#             source_user = "Source User"  # Replace with your logic to get source user
#             source = '{}<a href="#" data-toggle="tooltip" title="{}"><i class="fa fa-info-circle"></i></a>'.format(
#                 lead.lead_source.name, source_user
#             )
#         actions = '<a onclick="ivrcall({}, {})" style="color:red" href="javascript:void(0);" class="clicktocall" title="click2call"><i class="fa fa-volume-control-phone"></i></a> <a href="{}" title="Edit"><i class="fas fa-edit"></i></a> <a onclick="return confirm(`Do you really want to delete this lead?`)" style="color:red" href="{}" title="Delete"><i class="fa fa-trash"></i></a> <a href="#" data-lead_id="{}" data-toggle="modal" data-target="#lead_assigning_modal" title="Add lead transfer" class="openlead_assigning_modal"><i class="fas fa-user-plus"></i></a> <a href="#" data-lead_id="{}" data-toggle="modal" data-target="#attachmentModal" title="Add attachment" class="openAttachmentModal"><i class="fas fa-list"></i></a>'.format(
#             lead.phone_number, lead.id, edit_url, delete_url, lead.id, lead.id
#         )

#         data.append({
#             'leadid': leadid,
#             'source': source,
#             'actions': actions
#         })

#         return JsonResponse(data, safe=False)

#     return render(request, 'lead/index.html', {
#         'leaddata': leaddata,
#         'pagerest': pagerest,
#         'telecaller_users': telecaller_users,
#         'statuses': statuses,
#         'types': types,
#         'products': products,
#         'sources': sources,
#     })



@login_required
def lead_edit(request, id):
    request.session['pagerest'] = 'true'
    # user_data = request.user
    # user_department = user_data.department
    udetail = userdetail.objects.get(user=request.user)
    user_department = udetail.department 
    # ivruser = []

    # if user_department == 1:
    #     ivruser.append({'name': user_data.name, 'user_id': user_data.ivr_user_id})
    # else:
    #     # Assuming you have an IvrController model with an ivr_user() method
    #     ivr_controller = IvrController()
    #     ivruser = ivr_controller.ivr_user()

    statuses = Stage.objects.filter(status='active').order_by('-id')
    lead_types = LeadType.objects.all().order_by('-id')
    lead_sources = Sources.objects.all().order_by('-id')
    products = Product.objects.all().order_by('-id')
    locations = Location.objects.all().order_by('-id')
 
    lead = Leads.objects.get(id=id)  # Assuming Lead is your model for leads

    context = {
        # 'ivruser': ivruser,
        'lead': lead,
        'statuses': statuses,
        'lead_types': lead_types,
        'lead_sources': lead_sources,
        'products': products,
        'user_department': user_department,
        'locations': locations,
    }

    return render(request, 'lead/edit.html', context)


def lead_delete(request):
    pass

def leadlisting(request):
    user_data = request.user
    udetail = userdetail.objects.get(user_id=user_data.id)
    clientid = udetail.uniqueid
    shelf = Leads.objects.filter(client_id=udetail.uniqueid).order_by('-id')

    # telecaller_users = User.objects.filter(department_id=1).exclude(id=user_data.id).values('id', 'name')
    telecallers_id = userdetail.objects.filter(
        uniqueid=clientid, department='telecaller').values_list('user_id', flat=True)
    telecaller_users = User.objects.filter(id__in=telecallers_id)
    # print(telecaller_users)

    statuses = Stage.objects.filter(status='active').values('id', 'name')
    types = LeadType.objects.all().values('id', 'name')
    products = Product.objects.all().values('id', 'name')
    # product_name = get_product_by_id(lead.product_id) if lead.product_id else ''
    sources = Sources.objects.all().values('id', 'name')

    # ivr_user = []
    # if user_department == 1:
    #     ivr_user.append({'name': user_data.name, 'user_id': user_data.ivr_user_id})
    # else:
    #     # Assuming you have an IvrController model with an ivr_user() method
    #     ivr_controller = IvrController()
    #     ivr_user = ivr_controller.ivr_user()

    # telecaller_users = User.objects.filter(department_id=1).exclude(id=user_data.id).values('id', 'name')
    # statuses = LeadStatus.objects.filter(status='active').values('id', 'name')
    # types = LeadType.objects.all().values('id', 'name')
    # products = Product.objects.all().values('id', 'name')
    # sources = LeadSource.objects.all().values('id', 'name')

    drid = user_data.id
    lead_data = {}
    if 'edit' in request.META.get('HTTP_REFERER', ''):
        pagerest = request.session.get('pagerest')
        lead_data = request.session.get('leaddata')
        request.session.pop('leaddata', None)
    else:
        pagerest = "false"

    leads = Leads.objects.exclude(lead_status_id=25)

    if request.is_ajax():
        search_text = request.GET.get('searchText')
        status = request.GET.get('status')
        lead_type = request.GET.get('type')
        product = request.GET.get('product')
        lead_source = request.GET.get('source')
        creation_date_sort = request.GET.get('creation_date_sort')
        filter_created_date = request.GET.get('filter_created_date')
        filter_updated_dates = request.GET.get('filter_updated_dates')
        filter_telecaller = request.GET.get('filter_telecaller')

        if search_text:
            leads = leads.filter(Q(name__icontains=search_text) | Q(phone__icontains=search_text))

        if status:
            leads = leads.filter(lead_status_id=status)

        if lead_type:
            leads = leads.filter(lead_type_id=lead_type)

        if product:
            leads = leads.filter(product_id=product)

        if lead_source:
            leads = leads.filter(lead_source_id=lead_source)

        if filter_created_date:
            created_date = datetime.strptime(filter_created_date, "%Y-%m-%d")
            leads = leads.filter(created_date__date=created_date.date())

        if filter_updated_dates:
            updated_dates_list = filter_updated_dates.split(',')
            updated_dates_list = [datetime.strptime(date, "%Y-%m-%d") for date in updated_dates_list]
            leads = leads.filter(updated_date__date__in=updated_dates_list)

        if filter_telecaller:
            leads = leads.filter(assigned_to_id=filter_telecaller)

        total_leads_count = leads.count()

        if creation_date_sort == 'asc':
            leads = leads.order_by('created_date')
        elif creation_date_sort == 'desc':
            leads = leads.order_by('-created_date')

        start = int(request.GET.get('start'))
        length = int(request.GET.get('length'))

        data = []
        for row in leads[start:start+length]:
            actions = ''
            actions += '<a onclick="ivrcall({phone}, {id})" style="color:red" href="javascript:void(0);" class="clicktocall" title="click2call"><i class="fa fa-volume-control-phone"></i></a>'.format(phone=row.phone, id=row.id)
            
            actions += ' <a href="{url}" title="Edit"><i class="fas fa-edit"></i></a>'.format(url=reverse('leads.edit', kwargs={'id': row.id}))
            
            actions += ' <a onclick="return confirm(`Do you really want to delete this lead?`)" style="color:red" href="{url}" title="Delete"><i class="fa fa-trash"></i></a>'.format(url=reverse('leads.delete', kwargs={'id': row.id}))
            
            if not row.is_transfer:
                actions += ' <a href="#" data-lead_id="{id}" data-toggle="modal" data-target="#lead_assigning_modal" title="Add lead transfer" class="openlead_assigning_modal"><i class="fas fa-user-plus"></i></a>'.format(id=row.id)
            
            actions += ' <a href="#" data-lead_id="{id}" data-toggle="modal" data-target="#attachmentModal" title="Add attachment" class="openAttachmentModal"><i class="fas fa-list"></i></a>'.format(id=row.id)
            
            data.append({
                'DT_RowId': row.id,
                'DT_RowAttr': {
                    'data-status': row.lead_status_id,
                    'data-type': row.lead_type_id,
                    'data-product': row.product_id,
                    'data-source': row.lead_source_id,
                    # 'data-telecaller': row.assigned_to_id
                },
                'DT_RowClass': 'clickable-row',
                'DT_RowData': {
                    'url': reverse('leadlisting')
                },
                'id': row.id,
                'date': row.created_at.strftime("%d-%m-%Y"),
                'city': row.city,
                'phone': row.phone,
                'name': row.name,
                'product': row.product_id,
                'updated_date': row.updated_at.strftime("%d-%m-%Y"),
                'source': row.lead_source_id,
                'stage': row.lead_status_id, 
                'keyword': row.gkeyword,
                'actions': actions
            })

        return JsonResponse({
            "draw": int(request.GET.get('draw')),
            "recordsTotal": total_leads_count,
            "recordsFiltered": total_leads_count,
            "data": data
        }, encoder=CustomJSONEncoder)

    context = {
        # 'ivr_user': ivr_user,
        'telecaller_users': telecaller_users,
        'statuses': statuses,
        'types': types,
        'products': products,
        'sources': sources,
        'pagerest': pagerest,
        'lead_data': lead_data
    }
    return render(request, "lead/index.html", context)



# -----main 
# @login_required
# def leadlisting(request):
#     try:
#         udetail = userdetail.objects.get(user_id=request.user.id)
#         clientid = udetail.uniqueid
#         leads = Leads.objects.filter(
#             client_id=udetail.uniqueid).all().order_by('-id')

#         # telecallers_id = userdetail.objects.filter(
#         #     uniqueid=clientid, department='telecaller').values_list('user_id', flat=True)
#         # telecallers_name = User.objects.filter(id__in=telecallers_id)
#         # print(telecallers)

#         search_text = request.GET.get('searchText', '')
#         if search_text:
#             shelf = leads.filter(Q(name__icontains=search_text) | Q(
#                 email__icontains=search_text))

#         paginator = Paginator(leads, 5)  # Show 25 contacts per page.
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         # print(page_obj)


#         # telecaller_users = User.objects.filter(
#         #     department_id=1).exclude(id=udetail).values('id', 'name')

#         # telecallers = userdetail.objects.filter(uniqueid=clientid, department='telecaller').values('user_id', 'user__name', 'user__last_name')
#         telecallers = userdetail.objects.filter(uniqueid=clientid, department='telecaller').values('user_id', 'user__username')
#         statuses = Stage.objects.filter(status='active').values('id', 'name')
#         types = LeadType.objects.all().values('id', 'name')
#         products = Product.objects.all().values('id', 'name')
#         sources = Sources.objects.all().values('id', 'name')

#         # drid = udetail
#         # leaddata = {}
#         # if 'edit' in request.META.get('HTTP_REFERER', ''):
#         #     pagerest = request.session.get('pagerest')
#         #     leaddata = request.session.get('leaddata')
#         #     del request.session['leaddata']
#         # else:
#         #     pagerest = "false"

#         # print(leaddata)    

#         # leads = Leads.objects.exclude(lead_status_id=25)
#         # leads = Leads.objects.filter(client_id=udetail.uniqueid).exclude(lead_status_id=25)
#         # print(leads)

#         # data = []
#         # # print(leads)
#         # for lead in leads:
#         #     leadid = str(lead.id)
#         #     # if lead.is_transfer or not lead.is_assigned:
#         #     if lead.is_transfer:
#         #         if lead.lead_status_id:
#         #             transferred_by = "Transferred User"  # Replace with your logic to get transferred user
#         #             transferred_to = "Transferred To User"  # Replace with your logic to get transferred to user
#         #             leadid = '<span class="taglabel"><i class="fa fa-exclamation-circle" title="Transferred by {} to {}"></i></span>{}'.format(
#         #                 transferred_by, transferred_to, lead.id
#         #             )
#         #     source = ''
#         #     if lead.lead_source_id:
#         #         source_user = "Source User"  # Replace with your logic to get source user
#         #         source = '{}<a href="#" data-toggle="tooltip" title="{}"><i class="fa fa-info-circle"></i></a>'.format(
#         #             lead.lead_source_id.name, source_user
#         #         )
#         #     # edit_url = 'lead_update/{}'.format(lead.id)  # Define the edit URL here
#         #     # delete_url = 'lead_delete/{}'.format(lead.id)  # Define the delete URL here
#         #     # actions = '<a onclick="ivrcall({}, {})" style="color:red" href="javascript:void(0);" class="clicktocall" title="click2call"><i class="fa fa-volume-control-phone"></i></a> <a href="{}" title="Edit"><i class="fas fa-edit"></i></a> <a onclick="return confirm(`Do you really want to delete this lead?`)" style="color:red" href="{}" title="Delete"><i class="fa fa-trash"></i></a> <a href="#" data-lead_id="{}" data-toggle="modal" data-target="#lead_assigning_modal" title="Add lead transfer" class="openlead_assigning_modal"><i class="fas fa-user-plus"></i></a> <a href="#" data-lead_id="{}" data-toggle="modal" data-target="#attachmentModal" title="Add attachment" class="openAttachmentModal"><i class="fas fa-list"></i></a>'.format(
#         #     #     lead.phone, lead.id, edit_url, delete_url, lead.id, lead.id
#         #     # )
#         #     actions = ''
#         #     actions += '<a onclick="ivrcall(' + lead.phone + ',' + str(lead.id) + ')" style="color:red" href="javascript:void(0);" class="clicktocall" title="click2call"><i class="fa fa-volume-control-phone"></i></a>'

#         #     # actions += '<a onclick="ivrcall(' + lead.phone + ',' + lead.id + ')" style="color:red" href="javascript:void(0);" class="clicktocall" title="click2call"><i class="fa fa-volume-control-phone"></i></a>'
#         #     actions += ' <a href="' + reverse('leads.edit', kwargs={'id': lead.id}) + '" title="Edit"><i class="fas fa-edit"></i></a>'
#         #     actions += ' <a onclick="return confirm(\'Do you really want to delete this lead?\')" style="color:red" href="' + reverse('leads.delete', kwargs={'id': lead.id}) + '" title="Delete"><i class="fa fa-trash"></i></a>'

#         #     data.append({
#         #         'leadid': leadid,
#         #         'source': source,
#         #         'actions': actions
#         #     })
#         # print(data)
#         # JsonResponse(data, safe=False)



#     except Leads.DoesNotExist:
#         page_obj = None
#     return render(request, 'lead/index.html', {
#                                                'page_obj': page_obj,
#                                             #    'leads': leads,
#                                                'telecallers': telecallers,
#                                             #    'leaddata': leaddata,
#                                             #    'telecaller_users': telecaller_users,
#                                             #    'pagerest': pagerest,
#                                                'statuses': statuses,
#                                                'products':products,
#                                                'sources': sources,
#                                                'types': types,

#                                                })

@login_required
def lead_add(request):
    udetail = userdetail.objects.get(user_id=request.user.id)
    client_id = udetail.uniqueid
    user_department = udetail.department

    if request.method == 'POST':
        upload = LeadCreate(request.POST, client_id=client_id)
        if upload.is_valid():
            source = upload.save(commit=False)
            source.client_id = client_id
            name = upload.cleaned_data['name']
            email = upload.cleaned_data['email']
            phone = upload.cleaned_data['phone']
            comment = request.POST.get('comment')
            if request.POST.get('lead_status_id') == '23':
                upload.ringing_date = datetime.now()

            if Leads.objects.filter(name=name).exists():
                messages.error(request, 'Name must be unique.')
                return redirect('leadlisting')
            if Leads.objects.filter(email=email).exists():
                messages.error(request, 'Email must be unique.')
                return redirect('leadlisting')
            if Leads.objects.filter(phone=phone).exists():
                messages.error(request, 'Phone must be unique.')
                return redirect('leadlisting')
            else:
                upload.save()
                messages.success(request, 'Lead added successfully.')

                print("Lead added successfully. ID:", source.id)  

                # Validate and process StageQuestions data
                question_count = StageQuestions.objects.filter(
                    lead_status_id=source.lead_status_id, parent_id__isnull=True).count()

                print("Question count:", question_count)  

                if question_count:
                    post_data = request.POST.get('questionForm', '')
                    if post_data:
                        post_data = post_data.split('&')
                        insert_data = []

                        for i in range(1, question_count + 1):
                            answer_id = next((item.split('=')[1] for item in post_data if item.startswith(
                                'answer_' + str(i))), None)
                            if answer_id:
                                answer_data = StageQuestions.objects.filter(
                                    pk=answer_id).first()
                                question_id = next((item.split(
                                    '=')[1] for item in post_data if item.startswith('question_' + str(i))), None)
                                question_data = StageQuestions.objects.filter(
                                    pk=question_id).first()

                                if answer_data and question_data:
                                    lead_score = LeadScores()
                                    lead_score.question = question_data.text
                                    lead_score.answer = answer_data.text
                                    lead_score.score = answer_data.score
                                    lead_score.lead_id = source.id
                                    lead_score.client_id = client_id
                                    lead_score.lead_status_id = source.lead_status_id
                                    lead_score.created_at = datetime.now()
                                    lead_score.updated_at = datetime.now()
                                    insert_data.append(lead_score)

                        LeadScores.objects.bulk_create(insert_data)

                leadid = source
                lead_comment = LeadComments(lead_id=leadid, comment=comment, client_id=client_id)
                lead_comment.save()

                print("Lead comment saved. ID:", lead_comment.id) 

                # Check for "choose_date_time" in POST data
                if request.POST.get("choose_date_time"):
                    telecaller_id = request.user.id
                    if user_department != 'telecaller':
                        # sources_data = Sources.objects.filter(assign_user=request.user, lead_source__id=source.id).first()
                        sources_data = Sources.objects.filter(assign_user=request.user, leads__id=source.id).first()

                        if sources_data:
                            telecaller_id = sources_data.user_id

                    calls = Calls(
                        date=request.POST.get("date"),
                        lead_id=leadid,
                        lead_status_id=leadid.lead_status_id,
                        status=1,
                        client_id=client_id,
                        telecallerid=telecaller_id,
                    )
                    calls.save()

                    print("Call saved. ID:", calls.id)  

                return redirect('leadlisting')
        else:
            # Handle form validation errors
            errors = upload.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'{field}: {error}')
    else:
        upload = LeadCreate(client_id=client_id)

    return render(request, 'lead/add.html', {'leadform': upload})


# @login_required
# def lead_add(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     # userid = request.user
#     # source = None
#     user_department = udetail.department

#     if request.method == 'POST':
#         upload = LeadCreate(request.POST, client_id=client_id)
#         if upload.is_valid():
#             source = upload.save(commit=False)
#             source.client_id = client_id
#             name = upload.cleaned_data['name']
#             email = upload.cleaned_data['email']
#             phone = upload.cleaned_data['phone']
#             comment = request.POST.get('comment')
#             if request.POST.get('lead_status_id') == '23':
#                 upload.ringing_date = datetime.now()

#             # lead_id = source.id  # Move this line inside the if block

#             # if Leads.objects.filter(name=name).exists():
#             #     messages.error(request, 'Name must be unique.')
#             if Leads.objects.filter(name=name).exists():
#                 messages.error(request, 'Name must be unique.')
#                 return redirect('leadlisting')
#             if Leads.objects.filter(email=email).exists():
#                 messages.error(request, 'Email must be unique.')
#                 return redirect('leadlisting')
#             if Leads.objects.filter(phone=phone).exists():
#                 messages.error(request, 'Phone must be unique.')
#                 return redirect('leadlisting')
#             else:
#                 upload.save()
#                 messages.success(request, 'Lead added successfully.')


                
     
        

#                 question_count = StageQuestions.objects.filter(
#                     lead_status_id=source.lead_status_id, parent_id__isnull=True).count()

#                 if question_count:
#                     post_data = request.POST.get('questionForm', '')
#                     if post_data:
#                         post_data = post_data.split('&')
#                         insert_data = []

#                         for i in range(1, question_count + 1):
#                             answer_id = next((item.split('=')[1] for item in post_data if item.startswith(
#                                 'answer_' + str(i))), None)
#                             if answer_id:
#                                 answer_data = StageQuestions.objects.filter(
#                                     pk=answer_id).first()
#                                 question_id = next((item.split(
#                                     '=')[1] for item in post_data if item.startswith('question_' + str(i))), None)
#                                 question_data = StageQuestions.objects.filter(
#                                     pk=question_id).first()

#                                 if answer_data and question_data:
#                                     lead_score = LeadScores()
#                                     lead_score.question = question_data.text
#                                     lead_score.answer = answer_data.text
#                                     lead_score.score = answer_data.score
#                                     lead_score.lead_id = source.id
#                                     lead_score.client_id = client_id
#                                     lead_score.lead_status_id = source.lead_status_id
#                                     lead_score.created_at = timezone.now()
#                                     lead_score.updated_at = timezone.now()
#                                     insert_data.append(lead_score)

#                         LeadScores.objects.bulk_create(insert_data)

#                 leadid = source        
#                 lead_comment = LeadComments(lead_id=leadid, comment=comment, client_id=client_id)
#                 lead_comment.save()

#                 if request.POST.get("choose_date_time"):
#                     telecaller_id = request.user.id
#                     if user_department != 'telecaller':
#                         # sources_data = Sources.objects.filter(assign_user=request.user, lead_source_id=source.lead_source_id).first()
#                         sources_data = Sources.objects.filter(assign_user=request.user, lead_source__id=source.id).first()


#                         # sources_data = Sources.objects.filter(assign_user=request.user, lead_source__lead_source_id=source.lead_source_id).first()
#                         # sources_data = Sources.objects.filter(assign_user=request.user, lead_source_id=source.lead_source_id).first()


#                         if sources_data:
#                             telecaller_id = sources_data.user_id

#                     calls = Calls(
#                         date=request.POST.get("date"),
#                         lead_id=leadid.id,
#                         lead_status_id=leadid.lead_status_id.id,
#                         status=1,
#                         client_id=client_id,
#                         telecallerid=telecaller_id,
#                     )
#                     calls.save()


#                 return redirect('leadlisting')
#         else:
#             errors = upload.errors.as_data()
#             for field, field_errors in errors.items():
#                 for error in field_errors:
#                     messages.error(request, f'{field}: {error}')
#     else:
#         upload = LeadCreate(client_id=client_id)
#             # Get the lead_id from the newly created lead if available
#     # lead_id = source.id if source and hasattr(source, 'id') else None
#     # lead_id = source.id if source and hasattr(source, 'id') else None
#     # print(lead_id, '------------')

#     return render(request, 'lead/add.html', {'leadform': upload,
#                                             #   'lead_id': lead_id
#                                               })


# def lead_add(request):
#     if request.method == 'POST':
#         upload = LeadCreate(request.POST)
#         if upload.is_valid():
#             data = upload.cleaned_data

#             duplicate_lead = Leads.objects.filter(phone=data['phone']).exclude(email='').filter(email=data['email']).count()

#             if duplicate_lead:
#                 messages.error(request, 'This Lead already exists. Please use a different mobile and email address')
#                 return redirect('leads')

#             lead = upload.save(commit=False)
#             lead.salutation = data['salutation']
#             lead.name = data['name']
#             lead.phone = data['phone']
#             lead.city = data['city']
#             lead.spouse_name = data['spouse_name']
#             lead.alternate_number = data['alternate_number']
#             lead.centre_name = data['centre_name']
#             lead.email = data['email']
#             lead.lead_source_id = data['lead_source_id']
#             lead.primary_lead_source_id = data['lead_source_id']
#             lead.lead_status_id = data['lead_status_id']

#             if data['lead_status_id'] == 23:
#                 lead.ringing_date = timezone.now()

#             lead.product_id = data['product_id']
#             lead.is_potential = data['is_potential'] if data['is_potential'] else 'no'
#             lead.save()

#             # Saving answers
#             question_form_data = request.POST.get('questionForm', '')
#             if question_form_data:
#                 post_data = question_form_data.split('&')
#                 question_count = StageQuestions.objects.filter(lead_status_id=data['lead_status_id'], parent_id=None).count()
#                 insert_data = []
#                 for i in range(1, question_count + 1):
#                     answer_id = next((item.split('=')[1] for item in post_data if item.startswith('answer_' + str(i))), None)
#                     if answer_id:
#                         answer_data = StageQuestions.objects.filter(pk=answer_id).first()
#                         question_id = next((item.split('=')[1] for item in post_data if item.startswith('question_' + str(i))), None)
#                         question_data = StageQuestions.objects.filter(pk=question_id).first()
#                         if answer_data and question_data:
#                             lead_score = StageQuestions()
#                             lead_score.question = question_data.text
#                             lead_score.answer = answer_data.text
#                             lead_score.score = answer_data.score
#                             lead_score.lead_id = lead.id
#                             lead_score.lead_status_id = data['lead_status_id']
#                             lead_score.created_at = timezone.now()
#                             lead_score.updated_at = timezone.now()
#                             insert_data.append(lead_score)

#                 LeadScores.objects.filter(lead_id=lead.id).delete()
#                 LeadScores.objects.bulk_create(insert_data)

#             score = LeadScores.objects.filter(lead_id=lead.id).aggregate(sum_score=Sum('score'))
#             score = score.get('sum_score', 0)
#             score_range = ''

#             if score is not None:
#                 if 0 < score <= 25:
#                     score_range = '0-25'
#                 elif 26 <= score <= 50:
#                     score_range = '26-50'
#                 elif 51 <= score <= 75:
#                     score_range = '51-75'
#                 elif 76 <= score <= 1000:
#                     score_range = '76-100'

#                 lead_type_data = LeadType.objects.filter(score_range=score_range).first()
#                 if lead_type_data:
#                     lead.lead_type_id = lead_type_data.id
#                     lead.save()

#             # status_log = StatusLog()
#             # status_log.lead_id = lead.id
#             # status_log.lead_status_id = lead.lead_status_id
#             # status_log.user_id = request.user.id
#             # status_log.salutation = data['salutation']
#             # status_log.name = data['name']
#             # status_log.phone = data['phone']
#             # status_log.email = data['email']
#             # status_log.product_id = data['product_id']
#             # status_log.lead_source_id = data['lead_source_id']
#             # status_log.city = data['city']
#             # status_log.spouse_name = data['spouse_name']
#             # status_log.alternate_number = data['alternate_number']
#             # status_log.centre_name = data['centre_name']
#             # status_log.comment = data['comment']
#             # status_log.save()

#             # if data['choose_date_time']:
#             #     telecaller_id = request.user.id
#             #     if request.user.department_id != 1:
#             #         sources_data = LeadSourceUser.objects.filter(lead_source_id=data['lead_source_id']).first()
#             #         if sources_data:
#             #             telecaller_id = sources_data.user_id
#             #     call = Call()
#             #     call.date = data['date']
#             #     call.lead_id = lead.id
#             #     call.lead_status_id = lead.lead_status_id
#             #     call.status = 1
#             #     call.telecallerid = telecaller_id
#             #     call.save()

#             # if data['comment']:
#             #     lead_comment = LeadComment()
#             #     lead_comment.lead_id = lead.id
#             #     lead_comment.comment = data['comment']
#             #     lead_comment.save()

#             # # Send Welcome Template
#             # # welcome_template = Template.objects.filter(pk=1).first()
#             # # if welcome_template:
#             # #     welcome_template.first_name = lead.name
#             # #     send_mail(lead.email, welcome_template)

#             # if lead.lead_status_id != 1:
#             #     status_template = LeadStatus.objects.filter(pk=1).first()
#             #     if status_template and status_template.email_template_id:
#             #         template = Template.objects.filter(pk=status_template.email_template_id).first()
#             #         if template:
#             #             template.first_name = lead.name
#             #             if data['date']:
#             #                 template.date = data['date']
#             #             send_mail(lead.email, template)

#             #     if status_template and status_template.sms_template_id:
#             #         template = Template.objects.filter(pk=status_template.sms_template_id).first()
#             #         if template:
#             #             message = template.message.replace('{NAME}', lead.name.capitalize())
#             #             if data['date']:
#             #                 message = message.replace('{DATE}', data['date'].strftime('%Y-%m-%d'))
#             #                 message = message.replace('{TIME}', data['date'].strftime('%H:%M'))
#             #             # send_sms(lead.phone, message)

#             # if lead.status and lead.status.email_template_id:
#             #     template = Template.objects.filter(pk=lead.status.email_template_id).first()
#             #     if template:
#             #         template.first_name = lead.name
#             #         if data['date']:
#             #             template.date = data['date']
#             #         send_mail(lead.email, template)

#             # if lead.status and lead.status.sms_template_id:
#             #     template = Template.objects.filter(pk=lead.status.sms_template_id).first()
#             #     if template:
#             #         message = template.message.replace('{NAME}', lead.name.capitalize())
#             #         if data['date']:
#             #             message = message.replace('{DATE}', data['date'].strftime('%Y-%m-%d'))
#             #             message = message.replace('{TIME}', data['date'].strftime('%H:%M'))
#             #         # send_sms(lead.phone, message)

#             # admin_mail_data = {
#             #     'subject': 'New Lead',
#             #     'lead': lead
#             # }
#             # notify_email = self.notify_email.split(',')
#             # send_mail(notify_email, admin_mail_data)

#             messages.success(request, 'Lead has been added successfully')
#             return redirect('leads:add')

#     else:
#         messages.error(request, 'Unable to add Lead. Please try again later')

#     return render(request, 'leads/lead_add.html')

# @login_required
# def lead_update(request, id):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     lead = get_object_or_404(Leads, id=id, client_id=client_id)

#     lead_comment = LeadComments.objects.filter(lead_id=id).first()

#     if request.method == 'POST':
#         # Pass the client_id as a keyword argument
#         upload = LeadCreate(request.POST, instance=lead, client_id=client_id)
#         if upload.is_valid():
#             source = upload.save(commit=False)
#             source.client_id = client_id
#             name = upload.cleaned_data['name']
#             comment = request.POST.get('comment')


#             if Leads.objects.filter(name=name).exclude(id=id).exists():
#                 messages.error(request, 'Name must be unique.')
#             else:
#                 # upload = LeadCreate(instance=lead, client_id=client_id)
#                 if lead_comment:
#                      upload.fields["comment"].initial = lead_comment.comment
#                 upload.save()
#                 messages.success(request, 'Lead updated successfully.')

#                 question_count = StageQuestions.objects.filter(lead_status_id=source.lead_status_id, parent_id__isnull=True).count()
#                 # question_count = StageQuestions.objects.filter(lead_status_id=source.lead_status_id, parent_id__isnull=True).count()

#                 print(question_count)

#                 if question_count:
#                     post_data = request.POST
#                     insert_data = []

#                     for i in range(1, question_count + 1):
#                         answer_id = post_data.get('answer_' + str(i))
#                         print(answer_id)
#                         if answer_id:
#                             answer_data = StageQuestions.objects.filter(
#                                 pk=answer_id).first()
#                             question_id = post_data.get('question_' + str(i))
#                             question_data = StageQuestions.objects.filter(
#                                 pk=question_id).first()
#                             print(question_data, answer_data, question_id)
#                             if answer_data and question_data:
#                                 lead_score = LeadScores()
#                                 lead_score.question = question_data.text
#                                 lead_score.answer = answer_data.text
#                                 lead_score.score = answer_data.score
#                                 lead_score.lead_id = source
#                                 lead_score.lead_status_id = source.lead_status_id
#                                 lead_score.client_id = source.client_id

#                                 lead_score.created_at = timezone.now()
#                                 lead_score.updated_at = timezone.now()
#                                 insert_data.append(lead_score)

#                     LeadScores.objects.filter(lead_id=source.id).delete()
#                     LeadScores.objects.bulk_create(insert_data)

#                     lead_comment = LeadComments(lead_id=source, comment=comment, client_id=client_id)
#                     lead_comment.save()

#                 # # Saving answers
#                 # question_count = StageQuestions.objects.filter(lead_status_id=source.lead_status_id, parent_id__isnull=True).count()
#                 # print(question_count, '..........')
#                 # if question_count:
#                 #     print('request.POST',request.POST)
#                 #     post_data = request.POST.get('questionForm', '')
#                 #     print(post_data, '################')
#                 #     if post_data:
#                 #         post_data = post_data.split('&')
#                 #         insert_data = []
#                 #         print(post_data,'********')
#                 #         for i in range(1, question_count + 1):
#                 #             answer_id = next((item.split('=')[1] for item in post_data if item.startswith('answer_' + str(i))), None)
#                 #             if answer_id:
#                 #                 print(answer_id, '-------')
#                 #                 answer_data = StageQuestions.objects.filter(pk=answer_id).first()
#                 #                 question_id = next((item.split('=')[1] for item in post_data if item.startswith('question_' + str(i))), None)
#                 #                 question_data = StageQuestions.objects.filter(pk=question_id).first()
#                 #                 print(question_data)
#                 #                 if answer_data and question_data:
#                 #                     lead_score = LeadScores()
#                 #                     lead_score.question = question_data.text
#                 #                     lead_score.answer = answer_data.text
#                 #                     lead_score.score = answer_data.score
#                 #                     lead_score.lead_id = source.id
#                 #                     source.client_id = client_id
#                 #                     lead_score.lead_status_id = source.lead_status_id
#                 #                     lead_score.created_at = timezone.now()
#                 #                     lead_score.updated_at = timezone.now()
#                 #                     insert_data.append(lead_score)

#                 #         LeadScores.objects.filter(lead_id=source.id).delete()
#                 #         LeadScores.objects.bulk_create(insert_data)

#                 # score = LeadScores.objects.filter(
#                 #     lead_id=source.id).aggregate(sum_score=Sum('score'))
#                 # score = score.get('sum_score', 0)

#                 # if score is not None and 0 < score <= 25:
#                 #     score_range = '0-25'
#                 # elif score is not None and 26 <= score <= 50:
#                 #     score_range = '26-50'
#                 # elif score is not None and 51 <= score <= 75:
#                 #     score_range = '51-75'
#                 # elif score is not None and 76 <= score <= 1000:
#                 #     score_range = '76-100'
#                 # else:
#                 #     score_range = ''

#                 # lead_type_data = LeadType.objects.filter(
#                 #     score_range=score_range).first()
#                 # if lead_type_data:
#                 #     source.lead_type_id = lead_type_data.id
#                 #     source.save()

#                 return redirect('leadlisting')
#         else:
#             errors = upload.errors.as_data()
#             for field, field_errors in errors.items():
#                 for error in field_errors:
#                     messages.error(request, f'{field}: {error}')
#     else:
#         upload = LeadCreate(instance=lead, client_id=client_id)

#     return render(request, 'lead/edit.html', {'leadform': upload, 'lead_id': id})

# @login_required
# def lead_update(request, id): 
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     userid = User.objects.get(id=request.user.id)
#     lead = get_object_or_404(Leads, id=id, client_id=client_id)
#     lead_comment = LeadComments.objects.filter(lead_id=id).first()
#     lead_logs = LeadStatusLOG.objects.filter(lead_id=id)


#     if request.method == 'POST':
#         # Pass the client_id as a keyword argument
#         upload = LeadCreate(request.POST, instance=lead, client_id=client_id)
#         if upload.is_valid():
#             source = upload.save(commit=False)
#             source.client_id = client_id
#             name = upload.cleaned_data['name']
#             email = upload.cleaned_data['email']
#             phone = upload.cleaned_data['phone']

#             comment = request.POST.get('comment')

#             if Leads.objects.filter(name=name).exclude(id=id).exists():
#                 messages.error(request, 'Name must be unique.')
#             if Leads.objects.filter(email=email).exclude(id=id).exists():
#                 messages.error(request, 'Email must be unique.')   
#             if Leads.objects.filter(phone=phone).exclude(id=id).exists():
#                 messages.error(request, 'Phone must be unique.') 
            
#             else:
#                 if lead_comment:
#                     lead_comment.comment = comment  # Update the comment value
#                     lead_comment.save()
#                 else:
#                     lead_comment = LeadComments(lead_id=source, comment=comment, client_id=client_id)
#                     lead_comment.save()

#                 upload.save()





#                 question_count = StageQuestions.objects.filter(lead_status_id=source.lead_status_id, parent_id__isnull=True).count()
#                 if question_count:
#                     post_data = request.POST
#                     insert_data = []

#                     for i in range(1, question_count + 1):
#                         answer_id = post_data.get('answer_' + str(i))
#                         if answer_id:
#                             answer_data = StageQuestions.objects.filter(pk=answer_id).first()
#                             question_id = post_data.get('question_' + str(i))
#                             question_data = StageQuestions.objects.filter(pk=question_id).first()
#                             if answer_data and question_data:
#                                 lead_score = LeadScores()
#                                 lead_score.question = question_data.text
#                                 lead_score.answer = answer_data.text
#                                 lead_score.score = answer_data.score
#                                 lead_score.lead_id = source
#                                 lead_score.lead_status_id = source.lead_status_id
#                                 lead_score.client_id = source.client_id
#                                 lead_score.created_at = timezone.now()
#                                 lead_score.updated_at = timezone.now()
#                                 insert_data.append(lead_score)

#                     LeadScores.objects.filter(lead_id=source.id).delete()
#                     LeadScores.objects.bulk_create(insert_data)



                    
#                     # Check if the lead status has changed
#                     if lead.lead_status_id != source.lead_status_id:
#                         field_change = 1  # Status changed
#                     else:
#                         field_change = 0  # Status not changed

#                     # Create the status log
#                     status_log = LeadStatusLOG()
#                     status_log.lead_id = source
#                     status_log.lead_status_id = source.lead_status_id
#                     status_log.user_id = userid
#                     status_log.salutation = upload.cleaned_data['salutation']
#                     status_log.name = upload.cleaned_data['name']
#                     status_log.phone = request.POST.get('phonelog', '')
#                     status_log.email = upload.cleaned_data['email']
#                     status_log.product_id = upload.cleaned_data['product_id'].id
#                     status_log.lead_source_id = upload.cleaned_data['lead_source_id'].id
#                     status_log.city = upload.cleaned_data['city']
#                     status_log.spouse_name = upload.cleaned_data['spouse_name']
#                     status_log.alternate_number = upload.cleaned_data['alternate_number']
#                     status_log.centre_name = upload.cleaned_data['centre_name']
#                     status_log.comment = comment
#                     status_log.field_change = field_change
#                     status_log.save()

                    

#                 messages.success(request, 'Lead updated successfully.')
#                 return redirect('leadlisting')
#         else:
#             errors = upload.errors.as_data()
#             for field, field_errors in errors.items():
#                 for error in field_errors:
#                     messages.error(request, f'{field}: {error}')
#     else:

#         upload = LeadCreate(instance=lead, client_id=client_id)
#         lead_comment = LeadComments.objects.filter(lead_id=lead.id).first()
#         if lead_comment:
#             upload.initial['comment'] = lead_comment.comment

#     return render(request, 'lead/edit.html', {'leadform': upload, 'lead_id': id, 'lead_comment': lead_comment, 'lead_logs': lead_logs})



# @login_required
# def lead_update(request, id):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     userid = User.objects.get(id=request.user.id)
#     lead = get_object_or_404(Leads, id=id, client_id=client_id)
#     lead_comment = LeadComments.objects.filter(lead_id=id).first()
#     lead_logs = LeadStatusLOG.objects.filter(lead_id=id)

#     if request.method == 'POST':
#         upload = LeadCreate(request.POST, instance=lead, client_id=client_id)
#         if upload.is_valid():
#             source = upload.save(commit=False)
#             source.client_id = client_id
#             name = upload.cleaned_data['name']
#             email = upload.cleaned_data['email']
#             phone = upload.cleaned_data['phone']
#             comment = request.POST.get('comment')

#             print(upload.cleaned_data)

#             if Leads.objects.filter(name=name).exclude(id=id).exists():
#                 messages.error(request, 'Name must be unique.')
#                 return redirect('leadlisting')
#             if Leads.objects.filter(email=email).exclude(id=id).exists():
#                 messages.error(request, 'Email must be unique.')
#                 return redirect('leadlisting')
#             if Leads.objects.filter(phone=phone).exclude(id=id).exists():
#                 messages.error(request, 'Phone must be unique.')
#                 return redirect('leadlisting')

#             if lead_comment:
#                 lead_comment.comment = comment
#                 lead_comment.save()
#             else:
#                 lead_comment = LeadComments(lead_id=source, comment=comment, client_id=client_id)
#                 lead_comment.save()

#             upload.save()

#             question_count = StageQuestions.objects.filter(lead_status_id=source.lead_status_id, parent_id__isnull=True).count()
#             if question_count:
#                 post_data = request.POST
#                 insert_data = []

#                 for i in range(1, question_count + 1):
#                     answer_id = post_data.get('answer_' + str(i))
#                     if answer_id:
#                         answer_data = StageQuestions.objects.filter(pk=answer_id).first()
#                         question_id = post_data.get('question_' + str(i))
#                         question_data = StageQuestions.objects.filter(pk=question_id).first()
#                         if answer_data and question_data:
#                             lead_score = LeadScores()
#                             lead_score.question = question_data.text
#                             lead_score.answer = answer_data.text
#                             lead_score.score = answer_data.score
#                             lead_score.lead_id = source
#                             lead_score.lead_status_id = source.lead_status_id
#                             lead_score.client_id = source.client_id
#                             lead_score.created_at = timezone.now()
#                             lead_score.updated_at = timezone.now()
#                             insert_data.append(lead_score)

#                 LeadScores.objects.filter(lead_id=source.id).delete()
#                 LeadScores.objects.bulk_create(insert_data)

#             # Check if any field has changed
#             field_changes = {}
#             fields = ['salutation', 'name', 'phone', 'email', 'product_id', 'lead_source_id',
#                       'city', 'spouse_name', 'alternate_number', 'centre_name']
#             # for field in fields:
#             #     new_value = upload.cleaned_data[field]
#             #     old_value = getattr(lead, field)
#             #     if new_value != old_value:
#             #         field_changes[field] = new_value
#             #     print(old_value, new_value)   
#             for field in fields:
#                 new_value = upload.cleaned_data[field]
#                 old_value = getattr(lead, field)
#                 print(f"Field: {field}, Old Value: {old_value}, New Value: {new_value}")
#                 if new_value != old_value:
#                     field_changes[field] = new_value
 

#             if field_changes:
#                 status_log = LeadStatusLOG()
#                 status_log.lead_id = lead
#                 status_log.lead_status_id = lead.lead_status_id
#                 status_log.user_id = userid
#                 status_log.field_change = 1 if lead.lead_status_id != source.lead_status_id else 0
#                 status_log.comment = comment

#                 # Set the changed fields in the status log
#                 for field, value in field_changes.items():
#                     setattr(status_log, field, value)

#                 status_log.save()

#             messages.success(request, 'Lead updated successfully.')
#             return redirect('leadlisting')

#         else:
#             errors = upload.errors.as_data()
#             for field, field_errors in errors.items():
#                 for error in field_errors:
#                     messages.error(request, f'{field}: {error}')
#             return redirect('leadlisting')

#     else:
#         upload = LeadCreate(instance=lead, client_id=client_id)
#         if lead_comment:
#             upload.initial['comment'] = lead_comment.comment

#     return render(request, 'lead/edit.html', {'leadform': upload, 'lead_id': id, 'lead_comment': lead_comment, 'leads': lead_logs})

# @login_required
# def lead_update(request, id):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     userid = User.objects.get(id=request.user.id)
#     lead = get_object_or_404(Leads, id=id, client_id=client_id)
#     lead_comment = LeadComments.objects.filter(lead_id=id).first()
#     lead_logs = LeadStatusLOG.objects.filter(lead_id=id)

#     if request.method == 'POST':
#         upload = LeadCreate(request.POST, instance=lead, client_id=client_id)
#         if upload.is_valid():
#             source = upload.save(commit=False)
#             source.client_id = client_id
#             name = upload.cleaned_data['name']
#             email = upload.cleaned_data['email']
#             phone = upload.cleaned_data['phone']
#             comment = request.POST.get('comment')

#             if Leads.objects.filter(name=name).exclude(id=id).exists():
#                 messages.error(request, 'Name must be unique.')
#                 return redirect('leadlisting')
#             if Leads.objects.filter(email=email).exclude(id=id).exists():
#                 messages.error(request, 'Email must be unique.')
#                 return redirect('leadlisting')
#             if Leads.objects.filter(phone=phone).exclude(id=id).exists():
#                 messages.error(request, 'Phone must be unique.')
#                 return redirect('leadlisting')

#             if lead_comment:
#                 lead_comment.comment = comment
#                 lead_comment.save()
#             else:
#                 lead_comment = LeadComments(lead_id=source, comment=comment, client_id=client_id)
#                 lead_comment.save()

#             # Check if any field has changed
#             fields = ['salutation', 'name', 'phone', 'email', 'product_id', 'lead_source_id',
#                       'city', 'spouse_name', 'alternate_number', 'centre_name']

#             if upload.has_changed():
#                 field_changes = {field: upload.cleaned_data[field] for field in fields if field in upload.changed_data}
#                 field_change = 1
#             else:
#                 field_changes = {}
#                 field_change = 0

#             # Assign the updated field values to the source object
#             for field, value in field_changes.items():
#                 setattr(source, field, value)

#             source.save()

#             question_count = StageQuestions.objects.filter(lead_status_id=source.lead_status_id, parent_id__isnull=True).count()
#             if question_count:
#                 post_data = request.POST
#                 insert_data = []

#                 for i in range(1, question_count + 1):
#                     answer_id = post_data.get('answer_' + str(i))
#                     if answer_id:
#                         answer_data = StageQuestions.objects.filter(pk=answer_id).first()
#                         question_id = post_data.get('question_' + str(i))
#                         question_data = StageQuestions.objects.filter(pk=question_id).first()
#                         if answer_data and question_data:
#                             lead_score = LeadScores()
#                             lead_score.question = question_data.text
#                             lead_score.answer = answer_data.text
#                             lead_score.score = answer_data.score
#                             lead_score.lead_id = source
#                             lead_score.lead_status_id = source.lead_status_id
#                             lead_score.client_id = source.client_id
#                             lead_score.created_at = timezone.now()
#                             lead_score.updated_at = timezone.now()
#                             insert_data.append(lead_score)

#                 LeadScores.objects.filter(lead_id=source.id).delete()
#                 LeadScores.objects.bulk_create(insert_data)

#                 # Save data to LeadStatusLOG
#                 status_log = LeadStatusLOG()
#                 status_log.lead_id = lead
#                 status_log.lead_status_id = lead.lead_status_id
#                 status_log.user_id = userid
#                 status_log.comment = comment

#                 # Set the changed fields in the status log
#                 for field, value in field_changes.items():
#                     setattr(status_log, field, value)
#                     print(field, value)  # Add this debug print to check field and value

#                 # Set the remaining fields to empty if no change
#                 fields_to_empty = set(fields) - set(field_changes.keys())
#                 for field in fields_to_empty:
#                     setattr(status_log, field, '')
#                     print(field)  # Add this debug print to check field

#                 status_log.field_change = field_change
#                 status_log.save()

#             messages.success(request, 'Lead updated successfully.')
#             return redirect('leadlisting')

#         else:
#             errors = upload.errors.as_data()
#             for field, field_errors in errors.items():
#                 for error in field_errors:
#                     messages.error(request, f'{field}: {error}')
#             return redirect('leadlisting')

#     else:
#         upload = LeadCreate(instance=lead, client_id=client_id)
#         if lead_comment:
#             upload.initial['comment'] = lead_comment.comment

#     return render(request, 'lead/edit.html', {'leadform': upload, 'lead_id': id, 'lead_comment': lead_comment, 'leads': lead_logs})


# @login_required
# def lead_update(request, id):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     userid = User.objects.get(id=request.user.id)
#     lead = get_object_or_404(Leads, id=id, client_id=client_id)
#     lead_comment = LeadComments.objects.filter(lead_id=id).first()
#     lead_logs = LeadStatusLOG.objects.filter(lead_id=id)

#     if request.method == 'POST':
#         upload = LeadCreate(request.POST, instance=lead, client_id=client_id)
#         if upload.is_valid():
#             source = upload.save(commit=False)
#             source.client_id = client_id
#             name = upload.cleaned_data['name']
#             email = upload.cleaned_data['email']
#             phone = upload.cleaned_data['phone']
#             comment = request.POST.get('comment')

#             if Leads.objects.filter(name=name).exclude(id=id).exists():
#                 messages.error(request, 'Name must be unique.')
#                 return redirect('leadlisting')
#             if Leads.objects.filter(email=email).exclude(id=id).exists():
#                 messages.error(request, 'Email must be unique.')
#                 return redirect('leadlisting')
#             if Leads.objects.filter(phone=phone).exclude(id=id).exists():
#                 messages.error(request, 'Phone must be unique.')
#                 return redirect('leadlisting')

#             if lead_comment:
#                 lead_comment.comment = comment
#                 lead_comment.save()
#             else:
#                 lead_comment = LeadComments(lead_id=source, comment=comment, client_id=client_id)
#                 lead_comment.save()

#             # Check if any field has changed
#             fields = ['salutation', 'name', 'phone', 'email', 'product_id', 'lead_source_id',
#                       'city', 'spouse_name', 'alternate_number', 'centre_name']
#             field_changes = {field: upload.cleaned_data[field] for field in fields if upload.cleaned_data[field] != getattr(lead, field)}
#             # print(field_change)

#             # Convert empty string to None for the 'product_id' field
#             if 'product_id' in field_changes and field_changes['product_id'] == '':
#                 field_changes['product_id'] = None

#             # Set the field_change value correctly
#             field_change = 1 if field_changes else 0

#             # Assign the updated field values to the source object
#             for field, value in field_changes.items():
#                 setattr(source, field, value)

#             source.save()

#             # Save data to LeadStatusLOG
#             status_log = LeadStatusLOG()
#             status_log.lead_id = lead
#             status_log.lead_status_id = lead.lead_status_id
#             status_log.user_id = userid
#             status_log.comment = comment

#             # Set the changed fields in the status log
#             for field, value in field_changes.items():
#                 setattr(status_log, field, value)

#             status_log.field_change = field_change
#             status_log.save()

#             messages.success(request, 'Lead updated successfully.')
#             return redirect('leadlisting')

#         else:
#             errors = upload.errors.as_data()
#             for field, field_errors in errors.items():
#                 for error in field_errors:
#                     messages.error(request, f'{field}: {error}')
#             return redirect('leadlisting')

#     else:
#         upload = LeadCreate(instance=lead, client_id=client_id)
#         if lead_comment:
#             upload.initial['comment'] = lead_comment.comment

#     return render(request, 'lead/edit.html', {'leadform': upload, 'lead_id': id, 'lead_comment': lead_comment, 'leads': lead_logs})


@login_required
def lead_update(request, id):
    udetail = userdetail.objects.get(user_id=request.user.id)
    client_id = udetail.uniqueid
    userid = User.objects.get(id=request.user.id)
    lead = get_object_or_404(Leads, id=id, client_id=client_id)
    lead_comment = LeadComments.objects.filter(lead_id=id).first()
    lead_logs = LeadStatusLOG.objects.filter(lead_id=id)

    if request.method == 'POST':
        upload = LeadCreate(request.POST, instance=lead, client_id=client_id)
        if upload.is_valid():
            source = upload.save(commit=False)
            source.client_id = client_id
            name = upload.cleaned_data['name']
            email = upload.cleaned_data['email']
            phone = upload.cleaned_data['phone']
            comment = request.POST.get('comment')

            if Leads.objects.filter(name=name).exclude(id=id).exists():
                messages.error(request, 'Name must be unique.')
                return redirect('leadlisting')
            if Leads.objects.filter(email=email).exclude(id=id).exists():
                messages.error(request, 'Email must be unique.')
                return redirect('leadlisting')
            if Leads.objects.filter(phone=phone).exclude(id=id).exists():
                messages.error(request, 'Phone must be unique.')
                return redirect('leadlisting')

            if lead_comment:
                lead_comment.comment = comment
                lead_comment.save()
            else:
                lead_comment = LeadComments(lead_id=source, comment=comment, client_id=client_id)
                lead_comment.save()

            # Check if any field has changed
            fields = ['salutation', 'name', 'phone', 'email', 'product_id', 'lead_source_id',
                      'city', 'spouse_name', 'alternate_number', 'centre_name']
            field_changes = {}

            for field in fields:
                new_value = upload.cleaned_data[field]
                old_value = getattr(lead, field)
                if new_value != old_value:
                    field_changes[field] = new_value

            print("Field Changes:", field_changes)  # Debug print

            # Update the lead object with new field values
            lead.salutation = upload.cleaned_data['salutation']
            lead.name = upload.cleaned_data['name']
            lead.phone = upload.cleaned_data['phone']
            lead.email = upload.cleaned_data['email']
            lead.lead_source_id = upload.cleaned_data['lead_source_id']
            lead.city = upload.cleaned_data['city']
            lead.spouse_name = upload.cleaned_data['spouse_name']
            lead.alternate_number = upload.cleaned_data['alternate_number']
            lead.centre_name = upload.cleaned_data['centre_name']
            # lead.product_id = upload.cleaned_data['product_id'].id
                        # Handle the product_id field separately
            product_id = upload.cleaned_data['product_id']
            if product_id:
                lead.product_id = product_id
            else:
                lead.product_id = None
            lead.save()

            # Save data to LeadStatusLOG
            status_log = LeadStatusLOG()
            status_log.lead_id = lead
            status_log.lead_status_id = lead.lead_status_id
            status_log.user_id = userid
            status_log.comment = comment

            # Set the changed fields in the status log
            for field, value in field_changes.items():
                setattr(status_log, field, value)
                print(field, value)  # Add this debug print to check field and value

            # Set the remaining fields to empty if no change
            fields_to_empty = set(fields) - set(field_changes.keys())
            for field in fields_to_empty:
                setattr(status_log, field, '')
                print(field)  # Add this debug print to check field

            status_log.field_change = int(bool(field_changes) or field_changes.get('product_id') == '')
            status_log.save()

            print("Status Log:", status_log.__dict__)  # Debug print

            messages.success(request, 'Lead updated successfully.')

            # Handle the "choose_date_time" field to save Calls object
            if request.POST.get("choose_date_time"):
                telecaller_id = request.user.id
                if udetail.department != 'telecaller':
                    # sources_data = Sources.objects.filter(assign_user=request.user, lead_source_id=source.lead_source_id).first()
                    sources_data = Sources.objects.filter(assign_user=request.user, lead_source__id=source.id).first()

                    if sources_data:
                        telecaller_id = sources_data.user_id

                calls = Calls(
                    date=request.POST.get("date"),
                    lead_id=lead.id,
                    lead_status_id=lead.lead_status_id.id,
                    status=1,
                    client_id=client_id,
                    telecallerid=telecaller_id,
                )
                calls.save()
            return redirect('leadlisting')

        else:
            errors = upload.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('leadlisting')

    else:
        upload = LeadCreate(instance=lead, client_id=client_id)
        if lead_comment:
            upload.initial['comment'] = lead_comment.comment
    # lead_id = source.id if source and hasattr(source, 'id') else None


    return render(request, 'lead/edit.html', {'leadform': upload, 'lead_id': id, 'lead_comment': lead_comment, 'leads': lead_logs})


# @login_required
# def lead_add(request):
#     if request.method == 'POST':
#         upload = LeadCreateForm(request.POST)
#         if upload.is_valid():
#             data = upload.cleaned_data


#             lead = Lead()
#             lead.salutation = data['salutation']
#             lead.name = data['name']
#             lead.phone = data['phone']
#             lead.city = data['city']
#             lead.spouse_name = data['spouse_name']
#             lead.alternate_number = data['alternate_number']
#             lead.centre_name = data['centre_name']
#             lead.email = data['email']
#             lead.lead_source_id = data['lead_source_id']
#             lead.primary_lead_source_id = data['lead_source_id']
#             lead.lead_status_id = data['lead_status_id']
#             if data['lead_status_id'] == 23:
#                 lead.ringing_date = timezone.now()

#             lead.product_id = data['product_id']
#             lead.is_potential = data.get('is_potential', 'no')
#             lead.save()

#             # Saving answers
#             question_count = StatusQuestion.objects.filter(lead_status_id=data['lead_status_id'], parent__isnull=True).count()
#             if question_count:
#                 post_data = request.POST.get('questionForm', '')
#                 if post_data:
#                     post_data = post_data.split('&')
#                     insert_data = []
#                     for i in range(1, question_count + 1):
#                         answer_id = next((item.split('=')[1] for item in post_data if item.startswith('answer_' + str(i))), None)
#                         if answer_id:
#                             answer_data = StatusQuestion.objects.filter(pk=answer_id).first()
#                             question_id = next((item.split('=')[1] for item in post_data if item.startswith('question_' + str(i))), None)
#                             question_data = StatusQuestion.objects.filter(pk=question_id).first()
#                             if answer_data and question_data:
#                                 lead_score = LeadScore()
#                                 lead_score.question = question_data.text
#                                 lead_score.answer = answer_data.text
#                                 lead_score.score = answer_data.score
#                                 lead_score.lead_id = lead.id
#                                 lead_score.lead_status_id = data['lead_status_id']
#                                 lead_score.created_at = timezone.now()
#                                 lead_score.updated_at = timezone.now()
#                                 insert_data.append(lead_score)

#                     LeadScore.objects.bulk_create(insert_data)

#             score = LeadScore.objects.filter(lead_id=lead.id).aggregate(sum_score=models.Sum('score'))
#             score = score.get('sum_score', 0)

#             if 0 < score <= 25:
#                 score_range = '0-25'
#             elif 26 <= score <= 50:
#                 score_range = '26-50'
#             elif 51 <= score <= 75:
#                 score_range = '51-75'
#             elif 76 <= score <= 1000:
#                 score_range = '76-100'
#             else:
#                 score_range = ''

#             lead_type_data = LeadType.objects.filter(score_range=score_range).first()
#             if lead_type_data:
#                 lead.lead_type_id = lead_type_data.id
#                 lead.save()

#             status_log = StatusLog()
#             status_log.lead_id = lead.id
#             status_log.lead_status_id = lead.lead_status_id
#             status_log.user_id = request.user.id
#             status_log.salutation = data['salutation']
#             status_log.name = data['name']
#             status_log.phone = data['phone']
#             status_log.email = data['email']
#             status_log.product_id = data['product_id']
#             status_log.lead_source_id = data['lead_source_id']
#             status_log.city = data['city']
#             status_log.spouse_name = data['spouse_name']
#             status_log.alternate_number = data['alternate_number']
#             status_log.centre_name = data['centre_name']
#             status_log.comment = data['comment']
#             status_log.save()

#             if data.get('choose_date_time'):
#                 telecaller_id = request.user.id
#                 if request.user.department_id != 1:
#                     source_data = LeadSourceUser.objects.filter(lead_source_id=data['lead_source_id']).first()
#                     if source_data:
#                         telecaller_id = source_data.user_id

#                 call = Call()
#                 call.date = data['date']
#                 call.lead_id = lead.id
#                 call.lead_status_id = lead.lead_status_id
#                 call.status = 1
#                 call.telecaller_id = telecaller_id
#                 call.save()

#             if data.get('comment'):
#                 lead_comment = LeadComment()
#                 lead_comment.lead_id = lead.id
#                 lead_comment.comment = data['comment']
#                 lead_comment.save()

#             # Send Welcome Template
#             # welcome_template = Template.objects.filter(pk=1).first()
#             # if welcome_template:
#             #     welcome_template.first_name = lead.name
#             #     send_mail(lead.email, welcome_template)

#             if lead.lead_status_id != 1:
#                 status_template = LeadStatus.objects.filter(pk=1).first()
#                 if status_template and status_template.email_template_id:
#                     template = Template.objects.filter(pk=status_template.email_template_id).first()
#                     if template:
#                         template.first_name = lead.name
#                         if data.get('date'):
#                             template.date = data['date']

#                         send_mail(lead.email, template)

#                 if status_template and status_template.sms_template_id:
#                     template = Template.objects.filter(pk=status_template.sms_template_id).first()
#                     if template:
#                         message = template.message.replace("{NAME}", lead.name)
#                         if data.get('date'):
#                             message = message.replace("{DATE}", datetime.strptime(data['date'], '%Y-%m-%d').strftime('%Y-%m-%d'))
#                             message = message.replace("{TIME}", datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M'))

#                         # Helper.sendSMS(lead.phone, message)

#             if lead.status and lead.status.email_template_id:
#                 template = Template.objects.filter(pk=lead.status.email_template_id).first()
#                 if template:
#                     template.first_name = lead.name
#                     if data.get('date'):
#                         template.date = data['date']

#                     send_mail(lead.email, template)

#             if lead.status and lead.status.sms_template_id:
#                 template = Template.objects.filter(pk=lead.status.sms_template_id).first()
#                 if template:
#                     message = template.message.replace("{NAME}", lead.name)
#                     if data.get('date'):
#                         message = message.replace("{DATE}", datetime.strptime(data['date'], '%Y-%m-%d').strftime('%Y-%m-%d'))
#                         message = message.replace("{TIME}", datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M'))

#                     # Helper.sendSMS(lead.phone, message)

#             admin_mail_data = {
#                 'subject': "New Lead",
#                 'lead': lead,
#             }
#             notify_email = self.notifyEmail.split(',')
#             send_mail(notify_email, admin_mail_data)

#             # notification = {
#             #     'toastrMessage': f"New Lead Added named {lead.name}",
#             #     'alert-type': 'success'
#             # }

#             request.session['message'] = "Lead has been added successfully"
#             return redirect('leads:add')
#             # return redirect('leads:add').with(notification)
#         else:
#             request.session['error'] = "Unable to add Lead. Please try again later"


# @login_required
# def lead_update(request, id):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     lead = get_object_or_404(Leads, id=id, client_id=client_id)

#     if request.method == 'POST':
#         upload = LeadCreate(request.POST, instance=lead, client_id=client_id)
#         if upload.is_valid():
#             name = upload.cleaned_data['name']
#             if Leads.objects.exclude(id=id).filter(name=name).exists():
#                 messages.error(request, 'Name must be unique.')
#             else:
#                 upload.save()
#                 messages.success(request, 'Lead updated successfully.')
#                 return redirect('leadlisting')
#         else:
#             errors = upload.errors.as_data()
#             for field, field_errors in errors.items():
#                 for error in field_errors:
#                     messages.error(request, f'{field}: {error}')
#     else:
#         upload = LeadCreate(instance=lead, client_id=client_id)

#     return render(request, 'lead/edit.html', {'leadform': upload})


# def lead_update(request, id):
#     upload ={}

#     # fetch the object related to passed id
#     obj = get_object_or_404(Leads, id = id)

#     # pass the object as instance in form
#     form = LeadCreate(request.POST or None, instance = obj)

#     # save the data from the form and
#     # redirect to detail_view
#     if form.is_valid():
#         form.save()
#         return redirect('leadlisting')
#     return render(request, 'lead/edit.html', {'leadform':form})



# def lead_delete(request, id):
#     Lead = Leads.objects.get(id=id)
#     Lead.delete()
#     return redirect("leadlisting")

from django.db import connection
# def lead_delete(request, id):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     if id:
#         # Save Lead Log
#         findlead = Leads.objects.get(id=id)
#         leadarray = findlead.__dict__
#         leadarray['deleted_at'] = timezone.now()
#         leadarray['deleted_by'] = client_id
#         DeletedLead.objects.create(**leadarray)

#         # Save Lead Log
#         with connection.cursor() as cursor:
#             cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
#             res = Leads.objects.filter(id=id).delete()
#             statusLog = LeadStatusLOG()
#             statusLog.lead_id = id
#             statusLog.user_id = udetail
#             statusLog.deleted_at = timezone.now()
#             statusLog.deleted_by = client_id
#             statusLog.save()
#             cursor.execute('SET FOREIGN_KEY_CHECKS=1;')

#         if res[0]:
#             messages.success(request, 'Lead has been deleted successfully.')
#             # request.session.flash("message", "Lead has been deleted successfully")
#         else:
#             messages.error(request, 'Unable to delete this lead. Please try again later')
#             # request.session.flash("error", "Unable to delete this lead. Please try again later")
#     else:
#          messages.error(request, 'You are not authorized to access this location')
#         # request.session.flash("error", "You are not authorized to access this location")
#     return redirect("leadlisting")

# @login_required
 # def lead_delete(request, id):
#     userid = request.user.id
#     # user = get_object_or_404(User, id=userid)

#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
    

#     if id:
#         # Save Lead Log
#         findlead = Leads.objects.get(id=id)
#         lead_dict = {
#             'salutation': findlead.salutation,
#             'name': findlead.name,
#             'phone': findlead.phone,
#             'email': findlead.email,
#             'company': findlead.company,
#             'product_id': findlead.product_id,
#             'lead_source_id': findlead.lead_source_id,
#             'primary_lead_source_id': findlead.primary_lead_source_id,
#             'lead_type_id': findlead.lead_type_id,
#             'lead_status_id': findlead.lead_status_id,
#             'ringing_date': findlead.ringing_date,
#             'created_at': findlead.created_at,
#             'updated_at': findlead.updated_at,
#             'created_by': findlead.created_by,
#             'is_potential': findlead.is_potential,
#             'city': findlead.city,
#             'spouse_name': findlead.spouse_name,
#             'alternate_number': findlead.alternate_number,
#             'centre_name': findlead.centre_name,
#             'fbpage_id': findlead.fbpage_id,
#             'fbform_id': findlead.fbform_id,
#             'ivr_virtual_number': findlead.ivr_virtual_number,
#             'is_transfer': findlead.is_transfer,
#             'transfer_to': findlead.transfer_to,
#             'other_data': findlead.other_data,
#             'lead_data': findlead.lead_data,
#             'star_patient': findlead.star_patient,
#             'last_mesage_time': findlead.last_mesage_time,
#             'gcampaignid': findlead.gcampaignid,
#             'gadgroupid': findlead.gadgroupid,
#             'gkeyword': findlead.gkeyword,
#             'gdevice': findlead.gdevice,
#             'gdata': findlead.gdata,
#             'communication_id': findlead.communication_id,
#             'client_id': findlead.client_id,
#             'deleted_at': timezone.now(),
#             'deleted_by': userid,
#         }
#         DeletedLead.objects.create(**lead_dict)

#         # Save Lead Log
#         with connection.cursor() as cursor:
#             cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
#             res = Leads.objects.filter(id=id).delete()
#             statusLog = LeadStatusLOG()
#             statusLog.lead_id = id
#             statusLog.user_id = userid
#             statusLog.deleted_at = timezone.now()
#             statusLog.deleted_by = userid
#             statusLog.save()
#             cursor.execute('SET FOREIGN_KEY_CHECKS=1;')

#         if res[0]:
#             messages.success(request, 'Lead has been deleted successfully.')
#         else:
#             messages.error(request, 'Unable to delete this lead. Please try again later')
#     else:
#         messages.error(request, 'You are not authorized to access this location')

#     return redirect("leadlisting")


# @login_required
# def lead_delete(request, id):
#     userid = request.user.id

#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid

#     # findlead = get_object_or_404(Leads, id=id) 
#     findlead = Leads.objects.get(id=id) 

#     User = get_user_model()
#     user_instance = User.objects.get(id=userid)  # Retrieve the User instance

#     # Save Lead Log
#     lead_dict = {
#         'salutation': findlead.salutation,
#         'name': findlead.name,
#         'phone': findlead.phone,
#         'email': findlead.email,
#         'company': findlead.company,
#         'product_id': findlead.product_id,
#         'lead_source_id': findlead.lead_source_id,
#         'primary_lead_source_id': findlead.primary_lead_source_id,
#         'lead_type_id': findlead.lead_type_id,
#         'lead_status_id': findlead.lead_status_id,
#         'ringing_date': findlead.ringing_date,
#         'created_at': findlead.created_at,
#         'updated_at': findlead.updated_at,
#         'created_by': findlead.created_by,
#         'is_potential': findlead.is_potential,
#         'city': findlead.city,
#         'spouse_name': findlead.spouse_name,
#         'alternate_number': findlead.alternate_number,
#         'centre_name': findlead.centre_name,
#         'fbpage_id': findlead.fbpage_id,
#         'fbform_id': findlead.fbform_id,
#         'ivr_virtual_number': findlead.ivr_virtual_number,
#         'is_transfer': findlead.is_transfer,
#         'transfer_to': findlead.transfer_to,
#         'other_data': findlead.other_data,
#         'lead_data': findlead.lead_data,
#         'star_patient': findlead.star_patient,
#         'last_mesage_time': findlead.last_mesage_time,
#         'gcampaignid': findlead.gcampaignid,
#         'gadgroupid': findlead.gadgroupid,
#         'gkeyword': findlead.gkeyword,
#         'gdevice': findlead.gdevice,
#         'gdata': findlead.gdata,
#         'communication_id': findlead.communication_id,
#         'client_id': findlead.client_id,
#         'deleted_at': timezone.now(),
#         'deleted_by': userid,
#     }

#     DeletedLead.objects.create(**lead_dict)

#     statusLog = LeadStatusLOG()
#     statusLog.lead_id = findlead.id
#     statusLog.user_id = user_instance
#     statusLog.deleted_at = timezone.now()
#     statusLog.deleted_by = userid
#     statusLog.client_id = client_id

#     statusLog.save()  # Save the statusLog instance before deleting findlead

#     # Delete Lead
#     res = findlead.delete()

#     if res[0]:
#         messages.success(request, 'Lead has been deleted successfully.')
#     else:
#         messages.error(request, 'Unable to delete this lead. Please try again later')

#     return redirect("leadlisting")

from django.db import IntegrityError

@login_required
def lead_delete(request, id):
    userid = request.user.id

    udetail = userdetail.objects.get(user_id=request.user.id)
    client_id = udetail.uniqueid

    findlead = Leads.objects.get(id=id) 

    User = get_user_model()
    user_instance = User.objects.get(id=userid)  # Retrieve the User instance

    try:
        deleted_lead = DeletedLead.objects.get(phone=findlead.phone)
        deleted_lead = DeletedLead.objects.get(name=findlead.name)
        deleted_lead = DeletedLead.objects.get(email=findlead.email)

        # Update the existing DeletedLead entry
        deleted_lead.deleted_at = timezone.now()
        deleted_lead.deleted_by = userid
        deleted_lead.save()
    except DeletedLead.DoesNotExist:
        # Create a new DeletedLead entry
        lead_dict = {
            'salutation': findlead.salutation,
            'name': findlead.name,
            'phone': findlead.phone,
            'email': findlead.email,
            'company': findlead.company,
            'product_id': findlead.product_id,
            'lead_source_id': findlead.lead_source_id,
            'primary_lead_source_id': findlead.primary_lead_source_id,
            'lead_type_id': findlead.lead_type_id,
            'lead_status_id': findlead.lead_status_id,
            'ringing_date': findlead.ringing_date,
            'created_at': findlead.created_at,
            'updated_at': findlead.updated_at,
            'created_by': findlead.created_by,
            'is_potential': findlead.is_potential,
            'city': findlead.city,
            'spouse_name': findlead.spouse_name,
            'alternate_number': findlead.alternate_number,
            'centre_name': findlead.centre_name,
            'fbpage_id': findlead.fbpage_id,
            'fbform_id': findlead.fbform_id,
            'ivr_virtual_number': findlead.ivr_virtual_number,
            'is_transfer': findlead.is_transfer,
            'transfer_to': findlead.transfer_to,
            'other_data': findlead.other_data,
            'lead_data': findlead.lead_data,
            'star_patient': findlead.star_patient,
            'last_mesage_time': findlead.last_mesage_time,
            'gcampaignid': findlead.gcampaignid,
            'gadgroupid': findlead.gadgroupid,
            'gkeyword': findlead.gkeyword,
            'gdevice': findlead.gdevice,
            'gdata': findlead.gdata,
            'communication_id': findlead.communication_id,
            'client_id': findlead.client_id,
            'deleted_at': timezone.now(),
            'deleted_by': userid,
        }

        try:
            DeletedLead.objects.create(**lead_dict)
        except IntegrityError:
            # Handle the case where another process created a DeletedLead entry with the same phone concurrently
            deleted_lead = DeletedLead.objects.get(phone=findlead.phone)
            deleted_lead = DeletedLead.objects.get(name=findlead.name)
            deleted_lead = DeletedLead.objects.get(email=findlead.email)
            # Update the existing DeletedLead entry
            deleted_lead.deleted_at = timezone.now()
            deleted_lead.deleted_by = userid
            deleted_lead.save()

    statusLog = LeadStatusLOG()
    statusLog.lead_id = findlead
    statusLog.user_id = user_instance
    statusLog.deleted_at = timezone.now()
    statusLog.deleted_by = userid
    statusLog.client_id = client_id

    statusLog.save()  # Save the statusLog instance before deleting findlead

    # Delete Lead
    res = findlead.delete()

    if res[0]:
        messages.success(request, 'Lead has been deleted successfully.')
    else:
        messages.error(request, 'Unable to delete this lead. Please try again later')

    return redirect("leadlisting")



def upload_files(request):
    udetail = userdetail.objects.get(user_id=request.user.id)
    client_id = udetail.uniqueid

    if request.method == 'POST':
        files = request.FILES.getlist('files')
        allowed_file_extensions = ['pdf', 'jpg', 'png', 'docx']
        flag = 1

        if files:
            for file in files:
                extension = file.name.split('.')[-1].lower()
                filename = f'file_{uuid.uuid4()}.{extension}'
                if extension in allowed_file_extensions:
                    attachment = LeadAttachments()
                    lead_id = request.POST.get('attachment_lead_id')
                    lead = Leads.objects.get(id=lead_id)  # Retrieve the Leads instance
                    attachment.lead_id = lead
                    attachment.client_id = client_id

                    # File upload location
                    fs = FileSystemStorage(location='media/lead_media')
                    try:
                        fs.save(filename, file)
                        attachment.file = filename
                        attachment.save()
                    except Exception as e:
                        flag = 2
                        print(f"Error occurred while saving file: {e}")
                else:
                    flag = 3

            if flag == 1:
                messages.success(request, "File(s) have been uploaded successfully")
            elif flag == 3:
                messages.error(request, "Unable to upload some files. Only PDF, PNG, JPG, and DOCX are allowed.")
            else:
                messages.error(request, "Unable to upload File(s). Please try again later")
        else:
            flag = 2
            messages.error(request, "No files found to upload. Please choose some file(s).")

    return redirect('leadlisting')

# def upload_files(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid

#     if request.method == 'POST':
#         files = request.FILES.getlist('files')
#         allowed_file_extensions = ['pdf', 'jpg', 'png', 'docx']
#         flag = 1

#         if files:
#             for file in files:
#                 extension = file.name.split('.')[-1]
#                 filename = f'file_{uuid.uuid4()}.{extension}'
#                 if extension in allowed_file_extensions:
#                     attachment = LeadAttachments()
#                     lead_id = request.POST.get('attachment_lead_id')
#                     lead = Leads.objects.get(id=lead_id)  # Retrieve the Leads instance
#                     attachment.lead_id = lead
#                     attachment.client_id = client_id

#                     # File upload location
#                     fs = FileSystemStorage(location='lead_media')
#                     try:
#                         fs.save(filename, file)
#                         attachment.file = filename
#                         attachment.save()
#                     except Exception as e:
#                         flag = 2
#                         print(f"Error occurred while saving file: {e}")
#                 else:
#                     flag = 3

#             if flag == 1:
#                 messages.success(request, "File(s) have been uploaded successfully")
#             elif flag == 3:
#                 messages.error(request, "Unable to upload some files. Only PDF, PNG, JPG, and DOCX are allowed.")
#             else:
#                 messages.error(request, "Unable to upload File(s). Please try again later")
#         else:
#             flag = 2
#             messages.error(request, "No files found to upload. Please choose some file(s).")

#     return redirect('leadlisting')



# @login_required
# def findslot(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     user_department = udetail.department

#     if request.method == 'POST':
#         date = request.POST.get('date_time_field', 'not work')
#         source_id = request.POST.get('lead_source_id', None)  # Use None as the default value
#         print("Date:", date)
#         print("Source ID:", source_id)

#         # # ...

#         # if user_department == 'telecaller':
#         #     # Get the leads for the telecaller
#         #     home_leads = Leads.objects.filter(calls__telecallerid=udetail.id, calls__status=1)
#         # else:
#         #     # Get the leads based on the source and user department
#         #     if source_id:
#         #         try:
#         #             # Here is the line causing the issue
#         #             source_data = Sources.objects.get(assign_user=udetail, lead_source_id=source_id)
#         #             telecaller_id = source_data.user_id
#         #             home_leads = Leads.objects.filter(calls__telecallerid=telecaller_id, calls__status=1)
#         #         except ObjectDoesNotExist:
#         #             home_leads = Leads.objects.none()
#         #     else:
#         #         home_leads = Leads.objects.none()

#         # # Get the leads that have a callback on the specified date
#         # callbacksarr = home_leads.filter(calls__date__icontains=date).values('id', 'name', 'calls__slot').order_by('calls__date').distinct()

#         if user_department == 'telecaller':
#             # Get the leads for the telecaller
#             home_leads = Leads.objects.filter(calls__telecallerid=udetail.id, calls__status=1)
#         else:
#             # Get the leads based on the source and user department
#             if source_id:
#                 try:
#                     # Assuming the `assign_user` field is a ManyToManyField to the `User` model
#                     # source_data = Sources.objects.get(id=source_id)
#                     # telecallers = source_data.assign_user.all()
#                     # home_leads = Leads.objects.filter(calls__telecallerid__in=telecallers, calls__status=1)

#                     # source_data = Sources.objects.get(assign_user=udetail, lead_source_id=source_id)
#                     # telecaller_id = source_data.user_id
#                     # home_leads = Leads.objects.filter(calls__telecallerid=telecaller_id, calls__status=1)

#                     # user_instance = User.objects.get(pk=request.user.id)
#                     # source_data = Sources.objects.get(assign_user=user_instance, lead_source_id=source_id)
#                     # telecaller_id = source_data.user_id
#                     # home_leads = Leads.objects.filter(calls__telecallerid=telecaller_id, calls__status=1)

#                     # source_data = Sources.objects.get(assign_user=request.user, id=source_id)
#                     # telecaller_id = source_data.assign_user.id
#                     # home_leads = Leads.objects.filter(calls__telecallerid=telecaller_id, calls__status=1)

#                      # Assuming the `lead_source_id` is a ForeignKey to the `Sources` model
#                     source_data = Sources.objects.get(id=source_id)
#                     home_leads = Leads.objects.filter(lead_source_id=source_data, calls__status=1)
#                 except ObjectDoesNotExist:
#                     home_leads = Leads.objects.none()
#             else:
#                 home_leads = Leads.objects.none()

#         # Get the leads that have a callback on the specified date
#         callbacksarr = home_leads.filter(calls__date__icontains=date).values('id', 'name', 'calls__slot').order_by('calls__date').distinct()


#         # callbacksarr = home_leads.filter(calls__date__icontains=date).values('id', 'name', 'calls__slot').order_by('calls__date').distinct()
#         print("Home Leads Query Filter:", home_leads.query)        

#         slotarr = timeslot.objects.exclude(slot_time__isnull=True).values_list('slot_time', flat=True)
#         allslot = list(slotarr)

#         bookslot = [callback['calls__slot'] for callback in callbacksarr]

#         result = list(set(allslot) - set(bookslot))

#         slot_options = "<select class='form-control select2' name='slot' id='slot' required onchange='checkslot()'>"
#         slot_options += "<option value=''>Select Slot</option>"
#         for rvalue in result:
#             slot_options += f"<option value='{rvalue}'>{rvalue}</option>"
#         slot_options += "</select><span id='sloterror'></span>"

#         return JsonResponse({'html': slot_options})


# @login_required
# def checkslot(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     user_department = udetail.department

#     msg = ""
#     if request.method == 'POST':
#         date = request.POST.get('date_time_field')
#         source_id = request.POST.get('lead_source_id')
#         slot = request.POST.get('slot')

#         if user_department != 'telecaller':
#             try:
#                 source_data = Sources.objects.get(assign_user=udetail, lead_source_id=source_id)
#                 telecaller_id = source_data.user_id
#                 callbacksarr = Leads.objects.filter(calls__date__icontains=date, calls__slot__icontains=slot,
#                                                    calls__status=1, calls__telecallerid=telecaller_id)
#                 if callbacksarr.exists():
#                     msg = 'Slot is not available please select another slot'
#             except ObjectDoesNotExist:
#                 pass

#         return JsonResponse({'msg': msg})



def my_view(request):

    admin_site: AdminSite = site

    if request.session.get('loggedin') == 'djangoo':
        form = StageCreate()
        return render(request, 'lead/my_form.html', {'form': form})
    else:
        return render(request, 'lead/my_form.html')


# @login_required
# def findslot(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     user_department = udetail.department
#     userid = request.user


#     if request.method == 'POST':
#         date = request.POST.get('date_time_field')
#         source_id = request.POST.get('lead_source_id')

#         print("Date:", date)
#         print("Source ID:", source_id)
        
#         # user_data = request.user
#         # user_department = user_data.department_id
#         if user_department == 'telecaller':
#             home_leads = Leads.objects.all()
#             # if user_department == 'telecaller':
#             related_sources_data = Sources.objects.filter(assign_user=udetail)
#             # related_sources_data = LeadSourceUser.objects.filter(user_id=user_data.id)
#             if related_sources_data.exists():
#                 related_sources = related_sources_data.values_list("lead_source_id", flat=True)
#                 home_leads = home_leads.filter(lead_source_id__in=related_sources)
        
#             assign_leads_arr = LeadAssignedUser.objects.filter(user_id=udetail).values_list("lead_id", flat=True)
#             transfer_leads_arr = LeadTransferUser.objects.filter(user_id=udetail).values_list("lead_id", flat=True)

#             telecaller_leads_arr = list(set(list(assign_leads_arr) + list(transfer_leads_arr)))
#             home_leads = home_leads.filter(id__in=telecaller_leads_arr)
            
#             telecaller_leads_record = home_leads.values_list('id', flat=True)
        
#             callbacksarr = Leads.objects.filter(calls__date__icontains=date,
#                                                calls__status=1,
#                                                calls__telecallerid=udetail) \
#                                       .values('id', 'name', 'calls__slot') \
#                                       .order_by('calls__date') \
#                                       .distinct()
#         else:
#             telecallerId = None
#             if source_id:
#                 source_data = Sources.objects.filter(assign_user=udetail, lead_source_id=source_id)
#                 # source_data = LeadSourceUser.objects.filter(lead_source_id=source_id).first()
#                 if source_data:
#                    telecallerId = source_data.user_id

#             callbacksarr = Leads.objects.filter(calls__date__icontains=date,
#                                                calls__status=1)
#             if telecallerId:
#                 callbacksarr = callbacksarr.filter(calls__telecallerid=telecallerId)

#             callbacksarr = callbacksarr.values('id', 'name', 'calls__slot') \
#                                      .order_by('calls__date') \
#                                      .distinct()

#         slotarr = timeslot.objects.exclude(slot_time__isnull=True).values_list('slot_time', flat=True)
#         allslot = list(slotarr)
        
#         bookslot = [callback['calls__slot'] for callback in callbacksarr]
        
#         result = list(set(allslot) - set(bookslot))
        
#         slot_options = ""
#         if result:
#             slot_options += "<select class='form-control select2' name='slot' id='slot' required onchange='checkslot()'>"
#             slot_options += "<option value=''>Select Slot</option>"
#             for rvalue in result:
#                 slot_options += f"<option value='{rvalue}'>{rvalue}</option>"
#             slot_options += "</select><span id='sloterror'></span>"

#         return JsonResponse({'html': slot_options})

@login_required
def findslot(request):
    udetail = userdetail.objects.get(user=request.user)
    user_department = udetail.department
    userid = request.user

    slot_options = ""

    if request.method == 'POST':
        date = request.POST.get('date')
        source_id = request.POST.get('lead_source_id')
        

        print("Date:", date)
        print("Source ID:", source_id)

        # if not date:
        #     return JsonResponse({'html': ""})
        
        if user_department == 'telecaller':
            home_leads = Leads.objects.all()

            related_sources_data = Sources.objects.filter(assign_user= userid)
            if related_sources_data.exists():
                related_sources = related_sources_data.values_list("lead_source_id", flat=True)
                home_leads = home_leads.filter(lead_source_id__in=related_sources)
        
            assign_leads_arr = LeadAssignedUser.objects.filter(user_id= userid).values_list("lead_id", flat=True)
            transfer_leads_arr = LeadTransferUser.objects.filter(user_id= userid).values_list("lead_id", flat=True)

            telecaller_leads_arr = list(set(list(assign_leads_arr) + list(transfer_leads_arr)))
            home_leads = home_leads.filter(id__in=telecaller_leads_arr)
            
            telecaller_leads_record = home_leads.values_list('id', flat=True)
        
            callbacksarr = Leads.objects.filter(calls__date__icontains=date,
                                               calls__status=1,
                                               calls__telecallerid=udetail) \
                                      .values('id', 'name', 'calls__slot') \
                                      .order_by('calls__date') \
                                      .distinct()
        else:
            telecallerId = None
            if source_id:
                try:
                    # Assuming `assign_user` is a ManyToManyField to the `User` model in the Sources model
                    # source_data = Sources.objects.filter(assign_user=userid, lead_source_id=source_id)
                    # source_data = Sources.objects.filter(lead_source_id=source_id)
                    # Assuming the correct field name for lead_source_id is "leads"
                    source_data = Sources.objects.filter(leads__id=source_id)
                    # Assuming you want to get the assign_user for each instance in source_data
                    for source_instance in source_data:
                        user_instance = source_instance.assign_user.first()
                        if user_instance:
                            telecallerId = user_instance.id
            # Do something with telecallerId if needed
                except ObjectDoesNotExist:
                    pass

            # callbacksarr = Leads.objects.filter(calls__date__icontains=date, calls__status=1)
            # callbacksarr = Leads.objects.filter(created_at__icontains=date, calls__status=1)
            callbacksarr = Leads.objects.filter(created_at__icontains=date, calls__status=1)


            print('callbackArray', callbacksarr)
            if telecallerId:
                callbacksarr = callbacksarr.filter(calls__telecallerid=telecallerId)

            callbacksarr = callbacksarr.values('id', 'name', 'calls__slot') \
                                     .order_by('calls__date') \
                                     .distinct()
            
            print('callbackArray2', callbacksarr)
            
        slotarr = timeslot.objects.exclude(slot_time__isnull=True).values_list('slot_time', flat=True)
        allslot = list(slotarr)
        
        bookslot = [callback['calls__slot'] for callback in callbacksarr]
        
        result = list(set(allslot) - set(bookslot))
        
        # print('result', result)
        # slot_options = ""
        # if result:
        #     slot_options += "<select class='form-control select2' name='slot' id='slot' required onchange='checkslot()'>"
        #     slot_options += "<option value=''>Select Slot</option>"
        #     for rvalue in result:
        #         slot_options += f"<option value='{rvalue}'>{rvalue}</option>"
        #     slot_options += "</select><span id='sloterror'></span>"
        # print(slot_options,'-----')
        # return JsonResponse({'html': slot_options}) 
        # return JsonResponse(slot_options) 

        if result:
            slot_options += "<select class='form-control select2' name='slot' id='slot' required onchange='checkSlot()'>"
            slot_options += "<option value=''>Select Slot</option>"
            for rvalue in result:
                slot_options += f"<option value='{rvalue}'>{rvalue}</option>"
            slot_options += "</select><span id='sloterror'></span>"
        print({'html': slot_options})
        return JsonResponse({'html': slot_options})
    # else:
    #     return JsonResponse({'html': ''})
        


@login_required
def checkslot(request):
    udetail = userdetail.objects.get(user=request.user)
    user_department = udetail.department
    userid = request.user


    msg = ""
    if request.method == 'POST':
        date = request.POST.get('date')
        source_id = request.POST.get('lead_source_id')
        slot = request.POST.get('slot')

        # user_data = request.user
        # user_department = user_data.department_id
        if user_department != 'telecaller':
        # if user_department != 1:
            telecallerId = None
            if source_id:
                # source_data = LeadSourceUser.objects.filter(lead_source_id=source_id).first()
                # source_data = Sources.objects.filter(assign_user=udetail, lead_source_id=source_id).first()
                source_data = Sources.objects.filter(leads__id=source_id)

                if source_data:
                   telecallerId = source_data.user_id

            callbacksarr = Leads.objects.filter(calls__date__icontains=date,
                                               calls__slot__icontains=slot,
                                               calls__status=1,
                                               calls__telecallerid=telecallerId) \
                                      .values('id', 'calls__slot') \
                                      .order_by('calls__date') \
                                      .distinct()

            if callbacksarr.exists():
                msg = 'Slot is not available please select another slot'

        return JsonResponse({'msg': msg})
    


from django.db.models import F

def lead_transfer_user(request):
    lead_id = request.POST.get('lead_id')
    assign = 0
    table_html = ""
    current_assigned = ""

    transferred_lead = LeadTransferUser.objects.filter(lead_id=lead_id).order_by('-id').annotate(
        transferred_by_name=F('transferred_by__name')
    ).values('lead_id', 'user_id', 'transferred', 'created_at', 'transferred_by', 'transferred_by_name')

    if transferred_lead:
        for transferred in transferred_lead:
            transfer = "NO"
            if transferred['transferred'] == 1:
                transfer = "YES"
                current_assigned = "Lead currently assigned to {}.".format(transferred['transferred_by_name'])

            transferred_by = User.objects.filter(id=transferred['transferred_by']).values('id', 'name').first()

            table_html += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(transferred['transferred_by_name'], transferred['created_at'], transferred_by['name'])

    return JsonResponse({"message": table_html, "current_assigned": current_assigned, "assign": assign})


@csrf_exempt
def lead_assigned_user(request):
    # lead_id = request.GET.get('lead_id')  # Use 'lead_id' instead of 'assigning_lead_id'
    lead_id = request.POST.get('assigning_lead_id')
    print(lead_id)
    if not lead_id:
        return JsonResponse({"message": "No lead ID provided.", "assign": 0})

    assign = 0

    # assigned_lead = LeadAssignedUser.objects.filter(lead_id=lead_id).order_by('-id').annotate(
    #     assigned_by_name=F('user_id__username')
    # ).values('lead_id', 'user_id', 'assigned', 'created_at', 'assigned_by_name')

    assigned_lead = LeadAssignedUser.objects.filter(lead_id=lead_id).order_by('-id').annotate(
    assigned_by_name=F('user_id__username')).values('lead_id', 'user_id', 'assigned', 'created_at', 'assigned_by_name')



    table_html = "<tr><td colspan='3'>Lead not assigned to telecaller yet!</td></tr>"
    if assigned_lead:
        table_html = ""
        for assigned in assigned_lead:
            assign = "NO"
            if assigned['assigned'] == 1:
                assign = "YES"
            table_html += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                assigned['assigned_by_name'], assigned['created_at'], assign
            )
        assign = 1

    return JsonResponse({"message": table_html, "assign": assign})




@login_required
def update_lead_assigning(request):
    udetail = userdetail.objects.get(user_id=request.user.id)
    client_id = udetail.uniqueid

    lead_id = request.POST.get('assigning_lead_id')
    user_id = request.POST.get('telecaller')

    # Retrieve the User object based on user_id
    user = get_object_or_404(User, id=user_id)

    lead = get_object_or_404(Leads, id=lead_id)

    leadassign = LeadAssignedUser(
        lead_id=lead.id,
        user_id=user,  # Assign the User object instead of user_id
        assigned=1,
        client_id=client_id
    )

    try:
        leadassign.save()  # No need for the if statement

        messages.success(request, "Lead assigned successfully")
    except Exception as e:
        messages.error(request, f"An error occurred while updating the lead: {str(e)}")

    return redirect('leadlisting')


def get_questions(request):
    questions_data = {}
    stage_id = request.POST.get('stageId')
    # Modified line to provide a default value of an empty string
    lead_id = request.POST.get('leadId')

    count = LeadScores.objects.filter(
        lead_id=lead_id, lead_status_id=stage_id).count()
    # print(count)
    # print(stage_id, lead_id)

    if count > 0:
        questions_data = {"status": 2}
    else:
        questions = StageQuestions.objects.filter(
            lead_status_id=stage_id, parent_id=None)
        # print('questions', questions)
        for question in questions:
            answers = StageQuestions.objects.filter(parent_id=question.id)
            # print('answers', answers)
            for answer in answers:
                if question.id not in questions_data:
                    questions_data[question.id] = {}
                if question.text not in questions_data[question.id]:
                    questions_data[question.id][question.text] = {}
                questions_data[question.id][question.text][answer.id] = answer.text
        # print(questions_data, 'questions_data')
        if not questions_data:
            questions_data = {"status": 2}
    return JsonResponse(questions_data)



def save_answers(request):
    if request.method == 'POST':
        lead_id = request.POST.get('leadId')
        stage_id = request.POST.get('stageId')
        answers = request.POST.getlist('answers[]')

        lead = get_object_or_404(Leads, id=lead_id)
        stage = get_object_or_404(Stage, id=stage_id)

        for answer in answers:
            question_id, answer_id = answer.split('_')
            question = get_object_or_404(StageQuestions, id=question_id)

            lead_score = LeadScores.objects.create(
                question=question.text,
                answer=answer_id,
                score=question.score,
                lead_id=lead,
                lead_status_id=stage
            )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


# @login_required
# def lead_log(request):
#     # user_data = request.user
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     clientid = udetail.uniqueid
#     # leads = Leads.objects.filter(client_id=udetail.uniqueid).all().order_by('-id')



#     # search_text = request.GET.get('searchText', '')
#     # if search_text:
#     #     shelf = leads.filter(Q(name__icontains=search_text) | Q(
#     #         email__icontains=search_text))

#     # paginator = Paginator(leads, 5)  # Show 25 contacts per page.
#     # page_number = request.GET.get('page')
#     # page_obj = paginator.get_page(page_number)
#     # # print(page_obj)



#     telecallers = userdetail.objects.filter(uniqueid=clientid, department='telecaller').values('user_id', 'user__username')
#     statuses = Stage.objects.filter(status='active').values('id', 'name')
#     types = LeadType.objects.values('id', 'name')
#     products = Product.objects.values('id', 'name')
#     sources = Sources.objects.values('id', 'name')

#     leads = LeadStatusLOG.objects.select_related('user_id')
#     leads = leads.select_related('status')
#     leads = leads.select_related('type')
#     leads = leads.select_related('product')
#     leads = leads.select_related('source')

#     # search_text = request.GET.get('searchText')
#     # type_id = request.GET.get('type')
#     # source_id = request.GET.get('source')
#     # product_id = request.GET.get('product')
#     # status_id = request.GET.get('status')
#     # telecaller_id = request.GET.get('telecaller')
#     # filter_date_range = request.GET.get('filter_date_range')

#     # if telecaller_id:
#     #     leads = leads.filter(user_id=telecaller_id)

#     # if search_text:
#     #     leads = leads.filter(Q(name__icontains=search_text) | Q(lead_id__icontains=search_text) | Q(email__icontains=search_text) | Q(phone__icontains=search_text))

#     # if filter_date_range:
#     #     lead_from, lead_to = filter_date_range.split('-')
#     #     leads = leads.filter(created_at__gte=lead_from, created_at__lt=lead_to)

#     # leads = leads.order_by('-created_at').paginate(self.paginatLimit)

#     # helper = Helper()
#     return render(request, 'lead/leadlogs.html', {
#         # 'telecallerId': telecaller_id,
#         'telecallers': telecallers,
#         'leads': leads,
#         # 'ivruser': ivr_user,
#         # 'searchText': search_text,
#         'statuses': statuses,
#         'types': types,
#         'products': products,
#         'sources': sources,
#         # 'typeId': type_id,
#         # 'productId': product_id,
#         # 'statusId': status_id,
#         # 'sourceId': source_id,
#         # 'Helper': helper
#     })



@login_required
def lead_log(request):
    try:        
        udetail = userdetail.objects.get(user_id=request.user.id)
        clientid = udetail.uniqueid

        telecallers = userdetail.objects.filter(uniqueid=clientid, department='telecaller').values('user_id', 'user__username')
        statuses = Stage.objects.filter(status='active').values('id', 'name')
        types = LeadType.objects.values('id', 'name')
        products = Product.objects.values('id', 'name')
        sources = Sources.objects.values('id', 'name')

        # searchText = request.GET.get("searchText")
        # typeId = request.GET.get("type")
        # sourceId = request.GET.get("source")
        # productId = request.GET.get("product")
        # statusId = request.GET.get("status")
        # telecallerId = request.GET.get("telecaller")
        # filter_date_range = request.GET.get("filter_date_range")


        leads = LeadStatusLOG.objects.filter(client_id=udetail.uniqueid).all().order_by('-id')
        paginator = Paginator(leads, 5)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        leads = paginator.get_page(page_number)


        # if telecallerId:
        #     leads = leads.filter(user_id=telecallerId)

        # if searchText:
        #     leads = leads.filter(
        #         Q(name__icontains=searchText)
        #         | Q(lead_id__icontains=searchText)
        #         | Q(email__icontains=searchText)
        #         | Q(phone__icontains=searchText)
        #     )

        # if filter_date_range:
        #     lead_from, lead_to = filter_date_range.split("-")
        #     leads = leads.filter(
        #         created_at__gte=lead_from,
        #         created_at__lt=lead_to,
        #     )

    except LeadStatusLOG.DoesNotExist:
        leads = None

    return render(request,"lead/leadlogs.html",
        {
        # 'telecallerId': telecaller_id,
        'telecallers': telecallers,
        'leads': leads,
        # 'ivruser': ivr_user,
        # 'searchText': search_text,
        'statuses': statuses,
        'types': types,
        'products': products,
        'sources': sources,
        # 'typeId': type_id,
        # 'productId': product_id,
        # 'statusId': status_id,
        # 'sourceId': source_id,
        # 'Helper': helper
        },
    )


# from django.db.models import Count
# def duplicateleads(request):
#     try:
#         udetail = userdetail.objects.get(user_id=request.user.id)
#         clientid = udetail.uniqueid
#         leads = Leads.objects.filter(client_id=udetail.uniqueid).all().order_by('-id')
#         duplicates = leads.values('phone').annotate(count=Count('phone')).filter(count__gt=1)
#         # duplicates = leads.values('phone').annotate(count=Count('phone')).filter(count__gt=1)

#         # for lead in leads:
#         #     if lead.phone not in duplicates.values_list('phone', flat=True):
#         #         duplicates = duplicates.union(Leads.objects.filter(phone=lead.phone).annotate(count=1))


#         search_text = request.GET.get('searchText', '')
#         if search_text:
#             shelf = leads.filter(Q(name__icontains=search_text) | Q(
#                 email__icontains=search_text))

#         paginator = Paginator(leads, 5)  # Show 25 contacts per page.
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#     except Leads.DoesNotExist:
#         page_obj = None
#     return render(request, 'duplicateleads/index.html', { 'page_obj': page_obj, 'duplicates': duplicates})


from django.db.models import Count

def duplicateleads(request):
    try:
        udetail = userdetail.objects.get(user_id=request.user.id)
        clientid = udetail.uniqueid
        leads = DuplicateLeads.objects.filter(client_id=udetail.uniqueid).all().order_by('-id')
        duplicates = leads.values('phone').annotate(count=Count('phone')).filter(count__gt=1)

        search_text = request.GET.get('searchText', '')
        if search_text:
            leads = leads.filter(Q(name__icontains=search_text) | Q(email__icontains=search_text))
            duplicates = leads.values('phone').annotate(count=Count('phone')).filter(count__gt=1)

        paginator = Paginator(leads, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except Leads.DoesNotExist:
        page_obj = None

    return render(request, 'duplicateleads/index.html', {'page_obj': page_obj, 'duplicates': duplicates})


# def delete_duplicate_lead(request, duplicate_id):
#     duplicate = get_object_or_404(DuplicateLeads, id=duplicate_id)
#     if request.method == 'POST':
#         duplicate.delete()
#         messages.success(request, 'Duplicate lead deleted successfully.')
#     return redirect('duplicateleads')

def delete_duplicates(request):
    if request.method == 'POST':
        lead_ids = request.POST.getlist('lead_ids')
        DuplicateLeads.objects.filter(id__in=lead_ids).delete()
        return redirect('duplicateleads')
    else:
        return redirect('duplicateleads')
    

@login_required
def parkedleads(request):
    try:
        udetail = userdetail.objects.get(user_id=request.user.id)
        user_department = udetail.department
        # leads = Leads.objects.filter(client_id=clientid).all().order_by('-id')
        # user_data = request.user
        # user_department = user_data.department

        statuses = Stage.objects.values("id", "name")
        types = LeadType.objects.values("id", "name")
        products = Product.objects.values("id", "name")
        sources = Sources.objects.values("id", "name")

        leads = Leads.objects.all()
        search_text = request.GET.get("searchText")
        type_id = request.GET.get("type")
        source_id = request.GET.get("source")
        product_id = request.GET.get("product")
        status_id = request.GET.get("status")
        # parked_lead = Stage.objects.get(slug="parked")

        if search_text:
            leads = leads.filter(
                Q(name__icontains=search_text) |
                Q(email__icontains=search_text) |
                Q(phone__icontains=search_text)
            )


        if user_department == 'telecaller':
            related_sources_data = Sources.objects.filter(assign_user=udetail)
            related_sources = [data.id for data in related_sources_data]
            leads = leads.filter(lead_source_id__in=related_sources)

        # leads = leads.filter(lead_status_id__in=[parked_lead.id, 25]).order_by('-id')
        
        
        paginator = Paginator(leads, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except Leads.DoesNotExist:
        page_obj = None
    context = {
        'leads': page_obj,
        'searchText': search_text,
        'statuses': statuses,
        'types': types,
        'products': products,
        'sources': sources,
        'typeId': type_id,
        'productId': product_id,
        'statusId': status_id,
        'sourceId': source_id
    }

    return render(request, 'parkedleads/index.html', context)


def update_status(request):
    if request.method == 'POST':
        selected_leads = request.POST.getlist('selectedLeads')
        status_data = get_status_id("parked")
        
        try:
            leads = Leads.objects.filter(id__in=selected_leads)
            leads.update(lead_status_id=status_data.id)

            log_data = []
            for lead_id in selected_leads:
                log_data.append({
                    'lead_id': lead_id,
                    'lead_status_id': status_data.id,
                    'created_at': timezone.now(),
                    'updated_at': timezone.now()
                })
            LeadStatusLOG.objects.bulk_create(log_data)

            messages.success(request, "Selected leads status have been updated")
        except Exception as e:
            messages.error(request, "Unable to update the status. Please try again later.")
        
        return redirect('home')

# Lead Types
def leadTypes(request):
    try:
        udetail = userdetail.objects.get(user_id=request.user.id)
        shelf = LeadType.objects.filter(
            client_id=udetail.uniqueid).all().order_by('-id')
        # shelf = Sources.objects.all().order_by('-id')
        paginator = Paginator(shelf, 3)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # print(page_obj)
    except LeadType.DoesNotExist:
        page_obj = None
    return render(request, 'leadType/index.html', {'page_obj': page_obj})


@login_required
def leadType_add(request):

    udetail = userdetail.objects.get(user_id=request.user.id)
    upload = LeadTypeCreate(request=request)
    if request.method == 'POST':
        upload = LeadTypeCreate(request.POST, request.FILES, request=request)
        if upload.is_valid():
            leadType = upload.save(commit=False)
            leadType.client_id = udetail.uniqueid

            # Check uniqueness of name field
            name = upload.cleaned_data['name']
            if LeadType.objects.filter(name=name).exists():
                messages.error(request, 'Name must be unique.')
            else:
                upload.save()
                messages.success(request, 'leadTypes added successfully.')
                return redirect('leadTypes')
        else:
            errors = upload.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'{field}: {error}')

    return render(request, 'leadType/edit.html', {'leadform': upload})


@login_required
def leadType_update(request, pk):
    udetail = userdetail.objects.get(user_id=request.user.id)
    leadType = get_object_or_404(LeadType, pk=pk)
    if request.method == 'POST':
        upload = LeadTypeCreate(
            request.POST, request.FILES, instance=leadType, request=request)
        if upload.is_valid():
            leadType = upload.save(commit=False)
            leadType.client_id = udetail.uniqueid

            # Check uniqueness of name field
            name = upload.cleaned_data['name']
            if LeadType.objects.exclude(pk=pk).filter(name=name).exists():
                messages.error(request, 'Name must be unique.')
            else:
                upload.save()
                messages.success(request, 'LeadType updated successfully.')
                return redirect('leadTypes')
        else:
            errors = upload.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'{field}: {error}')
    else:
        upload = LeadTypeCreate(instance=leadType, request=request)

    return render(request, 'leadType/edit.html', {'leadform': upload})


@login_required
def leadType_delete(request, pk):
    leadType = get_object_or_404(LeadType, pk=pk)
    if request.method == 'POST':
        leadType.delete()
        messages.success(request, 'LeadType deleted successfully.')
        return redirect('leadTypes')

    return render(request, 'leadType/delete.html', {'leadType': leadType})


@login_required
def sources(request):
    try:
        udetail = userdetail.objects.get(user_id=request.user.id)
        shelf = Sources.objects.filter(
            client_id=udetail.uniqueid).all().order_by('-id')
        # shelf = Sources.objects.all().order_by('-id')
        paginator = Paginator(shelf, 3)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # print(page_obj)
    except Sources.DoesNotExist:
        page_obj = None
    return render(request, 'source/index.html', {'page_obj': page_obj})


@login_required
def source_add(request):
    udetail = userdetail.objects.get(user_id=request.user.id)
    # Pass the request object to the form
    upload = SourceCreate(request=request)
    if request.method == 'POST':
        # Pass the request object to the form
        upload = SourceCreate(request.POST, request.FILES, request=request)
        if upload.is_valid():
            source = upload.save(commit=False)
            source.client_id = udetail.uniqueid  # Set the client_id to the user's client_id

            # upload.save_m2m()  # Save ManyToManyField data
            # user_ids = request.POST.getlist('assign_user')  # Get selected user IDs from the form
            # source.assign_users(user_ids)  # Assign users to the source

            # user_ids = request.POST.getlist('assign_user')  # Get selected user IDs from the form
            # source.assign_user.set(user_ids)  # Assign users to the source
            # upload.save_m2m()  # Save ManyToManyField data

            # Check uniqueness of name field
            name = upload.cleaned_data['name']
            if Sources.objects.filter(name=name).exists():
                messages.error(request, 'Name must be unique.')
            else:
                upload.save()
                upload.save_m2m()  # Save ManyToManyField data
                messages.success(request, 'Source added successfully.')
                return redirect('sources')
        else:
            errors = upload.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'{field}: {error}')

    return render(request, 'source/add.html', {'leadform': upload, 'user_department': udetail.department})


@login_required
def source_update(request, id):
    udetail = userdetail.objects.get(user_id=request.user.id)
    # print("id:", id)
    # print("client_id:", udetail.uniqueid)
    source = get_object_or_404(Sources, id=id, client_id=udetail.uniqueid)
    # print('source:', source)
    # Pass the request object and instance to the form
    upload = SourceCreate(instance=source, request=request)

    if request.method == 'POST':
        # Pass the request object and instance to the form
        upload = SourceCreate(request.POST, request.FILES,
                              instance=source, request=request)
        if upload.is_valid():
            # updated_source = upload.save(commit=False)
            # updated_source.client_id = udetail.uniqueid  # Set the client_id to the user's client_id

            # Check uniqueness of name field
            name = upload.cleaned_data['name']
            if Sources.objects.filter(name=name).exclude(id=id).exists():
                messages.error(request, 'Name must be unique.')
            else:
                upload.save()
                messages.success(request, 'Source updated successfully.')
                return redirect('sources')
        else:
            errors = upload.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'{field}: {error}')

    return render(request, 'source/edit.html', {'leadform': upload, 'user_department': udetail.department, 'id': id})


def stages(request):
    try:
        udetail = userdetail.objects.get(user_id=request.user.id)
        shelf = Stage.objects.filter(
            client_id=udetail.uniqueid).all().order_by('-id')
        # shelf = Sources.objects.all().order_by('-id')
        search_text = request.GET.get('searchText', '')
        if search_text:
            shelf = shelf.filter(Q(name__icontains=search_text) | Q(
                description__icontains=search_text))

        paginator = Paginator(shelf, 25)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # print(page_obj)
    except Stage.DoesNotExist:
        page_obj = None
    return render(request, 'stage/index.html', {'page_obj': page_obj})


# @login_required
# def stage_add(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     if request.method == 'POST':
#         data = request.POST
#         upload = StageCreate(request.POST, client_id=client_id)
#         if upload.is_valid():
#             source = upload.save(commit=False)
#             source.client_id = client_id
#             # stage = Stage.objects.get(id=source.id)

#             name = upload.cleaned_data['name']
#             if Stage.objects.filter(name=name).exists():
#                 messages.error(request, 'Name must be unique.')
#             else:
#                 for key in data:
#                     if key.startswith('questions-'):
#                         question_arr = data.getlist(key)
#                         question_value = question_arr[0]
#                         answers_arr = data.getlist(key.replace('questions-', 'questions-answers-'))
#                         scores_arr = data.getlist(key.replace('questions-', 'questions-scores-'))
#                         print(question_arr, answers_arr, scores_arr)
#                         if question_value:
#                             status_question = StageQuestions()
#                             status_question.text = question_value
#                             status_question.lead_status_id = source.id
#                             status_question.parent_id = None
#                             status_question.score = 0
#                             status_question.save()

#                             for answer, score in zip(answers_arr, scores_arr):
#                                 if answer.strip() and score.strip():
#                                     print('--------', answer, score)
#                                     status_answer = StageQuestions()
#                                     status_answer.text = answer
#                                     status_answer.lead_status_id = source.id
#                                     status_answer.parent_id = status_question.pk
#                                     status_answer.score = int(score) if score else 0
#                                     status_answer.save()
#                 upload.save()

#                 messages.success(request, 'Stage added successfully.')
#                 return redirect('stages')
#         else:
#             errors = upload.errors.as_data()
#             for field, field_errors in errors.items():
#                 for error in field_errors:
#                     messages.error(request, f'{field}: {error}')
#     else:
#         upload = StageCreate(client_id=client_id)
#     return render(request, 'stage/add.html', {'form': upload})



@login_required
def stage_add(request):
    udetail = userdetail.objects.get(user_id=request.user.id)
    client_id = udetail.uniqueid
    if request.method == 'POST':
        upload = StageCreate(request.POST, client_id=client_id)
        if upload.is_valid():
            source = upload.save(commit=False)
            source.client_id = client_id

            name = upload.cleaned_data['name']
            if Stage.objects.filter(name=name).exists():
                messages.error(request, 'Name must be unique.')
            else:
                source.save()

                for key, value in request.POST.items():
                    if key.startswith('questions-') and value and not key.endswith('answers[]') and not key.endswith('scores[]'):
                        question_value = value
                        print(question_value, '---------')

                        index = key.split('-')[1]
                        answers_arr = request.POST.getlist(
                            f'questions-{index}-answers[]')
                        scores_arr = request.POST.getlist(
                            f'questions-{index}-scores[]')

                        status_question = StageQuestions()
                        status_question.text = question_value
                        status_question.lead_status_id = source
                        status_question.parent_id = None
                        status_question.score = 0
                        status_question.save()

                        for answer, score in zip(answers_arr, scores_arr):
                            if answer.strip() and score.strip() and score != '0':
                                status_answer = StageQuestions()
                                status_answer.text = answer
                                status_answer.lead_status_id = source
                                status_answer.parent_id = status_question
                                status_answer.score = int(
                                    score) if score else 0
                                status_answer.save()

                # for key, value in request.POST.items():
                #     if key.startswith('questions-') and value:
                #         print(key, value)
                #         question_value = value
                #         # if question_value == '0':
                #         #     continue
                #         index = key.split('-')[1]
                #         answers_arr = request.POST.getlist(f'questions-{index}-answers[]')
                #         scores_arr = request.POST.getlist(f'questions-{index}-scores[]')
                #         print(question_value,'---------')
                #         print(answers_arr, scores_arr)

                #         status_question = StageQuestions()
                #         status_question.text = question_value
                #         status_question.lead_status_id = source
                #         status_question.parent_id = None
                #         status_question.score = 0
                #         status_question.save()

                #         for answer, score in zip(answers_arr, scores_arr):
                #             if answer.strip() and score.strip() and score != '0':
                #                 status_answer = StageQuestions()
                #                 status_answer.text = answer
                #                 status_answer.lead_status_id = source
                #                 status_answer.parent_id = status_question
                #                 status_answer.score = int(score) if score else 0
                #                 status_answer.save()

                messages.success(request, 'Stage added successfully.')
                return redirect('stages')
        else:
            errors = upload.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'{field}: {error}')
    else:
        upload = StageCreate(client_id=client_id)
    return render(request, 'stage/add.html', {'form': upload})


@login_required
def stage_update(request, id):
    udetail = userdetail.objects.get(user_id=request.user.id)
    client_id = udetail.uniqueid
    stage = Stage.objects.get(id=id)

    if request.method == 'POST':
        upload = StageCreate(request.POST, client_id=client_id, instance=stage)
        if upload.is_valid():
            source = upload.save(commit=False)
            source.client_id = client_id

            name = upload.cleaned_data['name']
            if Stage.objects.filter(name=name).exclude(id=stage.id).exists():
                messages.error(request, 'Name must be unique.')
            else:
                source.save()

                # Save or update questions and answers
                for key, value in request.POST.items():
                    if key.startswith('questions-') and value and not key.endswith('answers[]') and not key.endswith('scores[]'):
                        index = key.split('-')[1]
                        question_value = value
                        answers_arr = request.POST.getlist(
                            f'questions-{index}-answers[]')
                        scores_arr = request.POST.getlist(
                            f'questions-{index}-scores[]')

                        # Update existing question or create a new one
                        question_id = request.POST.get(f'questions-{index}-id')
                        if question_id:
                            question = StageQuestions.objects.get(
                                id=question_id)
                            question.text = question_value
                            question.save()
                        else:
                            question = StageQuestions.objects.create(
                                text=question_value,
                                lead_status_id=stage,
                                parent_id=None,
                                score=0
                            )

                        # Save or update answers for the question
                        for answer, score in zip(answers_arr, scores_arr):
                            answer_id = request.POST.get(
                                f'questions-{index}-answer-{answers_arr.index(answer)}-id')
                            if answer_id:
                                answer_obj = StageQuestions.objects.get(
                                    id=answer_id)
                                answer_obj.text = answer
                                answer_obj.score = int(score) if score else 0
                                answer_obj.save()
                            else:
                                StageQuestions.objects.create(
                                    text=answer,
                                    lead_status_id=stage,
                                    parent_id=question,
                                    score=int(score) if score else 0
                                )

                messages.success(request, 'Stage updated successfully.')
                return redirect('stages')
        else:
            errors = upload.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'{field}: {error}')
    else:
        upload = StageCreate(instance=stage)

    return render(request, 'stage/edit.html', {'form': upload, 'stage': stage})

