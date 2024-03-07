from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Leads, Sources, Stage, LeadType, StageQuestions, LeadScores, LeadAssignedUser, LeadTransferUser, LeadAttachments, LeadComments, LeadStatusLOG, DeletedLead, DuplicateLeads
from apps.product.models import Product
from apps.calls.models import Calls, Timeslots
from web_project import TemplateLayout
from .forms import LeadCreate, StageCreate, SourceCreate, LeadTypeCreate
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import site
# from userdetail import models as userdetail
from apps.authentication.models import UserDetails
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
from datetime import datetime
from django.urls import reverse
from apps.location.models import Location

import json
import csv
from django.views.decorators.csrf import csrf_exempt


# from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
import uuid
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# from .helpers import get_status_id
from .func import  get_status_id, get_lead_by_id , get_product_by_id, get_source_by_id, get_source_user, get_status_by_id, get_transferred_user, get_transferredto_user, get_type_by_id, get_product_name_by_id
from django.core.exceptions import ObjectDoesNotExist

from apps.template.models import Template
from django.core.serializers.json import DjangoJSONEncoder

from django.core.mail import send_mail
from django.db import models

from apps.leads.ivr import ivr_user




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







                #         {% with udetail=UserDetails.objects.get(user_id=request.user.id) %}
                #         {% with clientid=udetail.uniqueid %}
                #             {% with user_department=udetail.department %}
                #                 {% if user_department != 'telecaller' %}
                #         {% endwith %}
                #     {% endwith %}
                # {% endwith %}






# @login_required
# def leadlisting(request):
#     # Fetching user details
#     user_data = request.user
#     udetail = UserDetails.objects.get(user_id=user_data.id)
#     clientid = udetail.uniqueid
#     shelf = Leads.objects.filter(client_id=udetail.uniqueid).order_by('-id')

#     # telecaller_users = User.objects.filter(department_id=1).exclude(id=user_data.id).values('id', 'name')
#     telecallers_id = UserDetails.objects.filter(
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



# def store_lead(request):
#     if request.method == 'POST':
#         data = request.POST
#         lead = Leads()

#         duplicate_lead = Leads.objects.filter(phone=data["phone"]).or_filter(email=data["email"]).count()

#         if duplicate_lead:
#             messages.error(request, "This Lead already exists. Please use a different mobile and email address")
#             return redirect('leadlisting')

#         lead.salutation = data["salutation"]
#         lead.name = data["name"]
#         lead.phone = data["phone"]
#         lead.city = data["city"]
#         lead.spouse_name = data["spouse_name"]
#         lead.alternate_number = data["alternate_number"]
#         lead.centre_name = data["centre_name"]
#         lead.email = data["email"]
#         lead.lead_source_id = data["lead_source_id"]
#         lead.primary_lead_source_id = data["lead_source_id"]
#         lead.lead_status_id = data["lead_status_id"]

#         if data["lead_status_id"] == 23:
#             lead.ringing_date = datetime.now()

#         lead.product_id = data["product_id"]
#         lead.is_potential = "no" if not data.get("is_potential") else data["is_potential"]

#         if lead.save():

#             # saving answers
#             postData = request.POST.get("questionForm")
#             question_count = StageQuestions.objects.filter(lead_status_id=data["lead_status_id"], parent_id=None).count()
#             insert_data = []

#             if question_count:
#                 for i in range(1, question_count+1):
#                     if "answer_" + str(i) in postData and postData["answer_" + str(i)]:
#                         answer_id = int(postData["answer_" + str(i)])
#                         if answer_id:
#                             answer_data = StageQuestions.objects.get(id=answer_id)
#                             lead_score = LeadScoress()
#                             question_id = postData["question_" + str(i)]
#                             question_data = StageQuestions.objects.get(id=question_id)
#                             lead_score.question = question_data.text
#                             lead_score.answer = answer_data.text
#                             lead_score.score = answer_data.score
#                             lead_score.lead_id = lead.id
#                             lead_score.lead_status_id = data["lead_status_id"]
#                             lead_score.created_at = datetime.now()
#                             lead_score.updated_at = datetime.now()
#                             insert_data.append(lead_score)

#                 if insert_data:
#                     LeadScoress.objects.bulk_create(insert_data)

#                     # calculate score
#                     score = LeadScoress.objects.filter(lead_id=lead.id).sum("score")
#                     if score > 0 and score <= 25:
#                         range = "0-25"
#                     elif score >= 26 and score <= 50:
#                         range = "26-50"
#                     elif score >= 51 and score <= 75:
#                         range = "51-75"
#                     elif score >= 76 and score <= 1000:
#                         range = "76-100"

#                     lead_type_data = LeadType.objects.filter(score_range=range).first()
#                     if lead_type_data:
#                         lead.lead_type_id = lead_type_data.id
#                         lead.save()

#                     # save status log
#                     status_log = LeadStatusLOG()
#                     status_log.lead_id = lead.id
#                     status_log.lead_status_id = lead.lead_status_id
#                     status_log.user_id = request.user.id
#                     status_log.salutation = data["salutation"]
#                     status_log.name = data["name"]
#                     status_log.phone = data["phone"]
#                     status_log.email = data["email"]
#                     status_log.product_id = data["product_id"]
#                     status_log.lead_source_id = data["lead_source_id"]
#                     status_log.city = data["city"]
#                     status_log.spouse_name = data["spouse_name"]
#                     status_log.alternate_number = data["alternate_number"]
#                     status_log.centre_name = data["centre_name"]
#                     status_log.comment = data["comment"]
#                     status_log.save()

#                     if data.get("choose_date_time"):
#                         telecaller_id = request.user.id
#                         if request.user.department_id != 1:
#                             sources_data = Sources.objects.filter(lead_source_id=data["lead_source_id"]).first()
#                             if sources_data:
#                                 telecaller_id = sources_data.user_id
#                         calls = Calls()
#                         calls.date = data["date"]
#                         calls.lead_id = lead.id
#                         calls.lead_status_id = lead.lead_status_id
#                         calls.status = 1
#                         calls.telecallerid = telecaller_id
#                         calls.save()

#                     if data.get("comment"):
#                         lead_comment = LeadComments()
#                         lead_comment.lead_id = lead.id
#                         lead_comment.comment = data["comment"]
#                         lead_comment.save()

#             # Send Welcome Template
#             # welcome_template = Template.objects.get(id=1)
#             # if welcome_template:
#             #     welcome_template.first_name = lead.name
#             #     self.send_mail(lead.email, welcome_template)

#             if lead.lead_status_id != 1:
#                 status_template = LeadStatusLOG.objects.get(id=1)
#                 if status_template.email_template_id:
#                     temp = template.objects.get(id=status_template.email_template_id)
#                     temp.first_name = lead.name
#                     if data.get("date"):
#                         temp.date = data["date"]

#                     # self.send_mail(lead.email, template)

#         return redirect('leadlisting')



@login_required
def store_lead(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    udetail = UserDetails.objects.get(user_id=request.user.id)
    client_id = udetail.uniqueid
    user_department = udetail.department

    statuses = Stage.objects.filter(status='active').order_by('-id')
    lead_types = LeadType.objects.all().order_by('-id')
    lead_sources = Sources.objects.all().order_by('-id')
    products = Product.objects.all().order_by('-id')
    locations = Location.objects.all().order_by('-id')

    # lead = Leads() # Assuming Lead is your model for leads
    # print('Leadid-----', lead.id)

    lead = None
    if request.method == 'POST':
        # form = LeadCreate(request.POST, client_id=client_id)
        data = request.POST
        # print('data-------', data)
        lead = Leads()

        # duplicate_lead = Leads.objects.filter(phone=data["phone"]).or_filter(email=data["email"]).count()
        duplicate_lead = Leads.objects.filter(Q(phone=data["phone"]) | Q(email=data["email"])).count()

        if duplicate_lead:
            if user_department == 'telecaller':
                messages.error(request, "This Lead already exists. Please use a different mobile and email address")
                return redirect('telecaller-lead')
            else:
                messages.error(request, "This Lead already exists. Please use a different mobile and email address")
                return redirect('leadlisting')

        # lead.salutation = data["salutation"]
        # lead.name = data["name"]
        # lead.phone = data["phone"]
        # lead.city = data["city"]
        # lead.spouse_name = data["spouse_name"]
        # lead.alternate_number = data["alternate_number"]
        # lead.centre_name = data["centre_name"]
        # lead.email = data["email"]
        # lead.lead_source_id = data["lead_source_id"]
        # lead.primary_lead_source_id = data["lead_source_id"]
        # lead.lead_status_id = data["lead_status_id"]
        # lead.client_id = client_id

        lead_source_id = data["lead_source_id"]
        lead_status_id = data["lead_status_id"]
        centre_name_id =data["centre_name"]
        product_id = data["product_id"]
        lead_type_id = data["lead_type_id"]


        try:
            product = Product.objects.get(id=product_id)
            lead_source = Sources.objects.get(id=lead_source_id)
            lead_status = Stage.objects.get(id=lead_status_id)
            lead_type =  LeadType.objects.get(id=lead_type_id)
            centre_name = Location.objects.get(id=centre_name_id)   # Fetch the appropriate Stage instance
        except:
            if user_department == 'telecaller':
                messages.error(request, "Invalid lead source or lead status selected")
                return redirect('telecaller-lead')
            else:
                messages.error(request, "Invalid lead source or lead status selected")
                return redirect('leadlisting')

        lead = Leads(
            salutation=data["salutation"],
            name=data["name"],
            phone=data["phone"],
            city=data["city"],
            spouse_name=data["spouse_name"],
            alternate_number=data["alternate_number"],
            email=data["email"],
            # lead_source_id=data["lead_source_id"],
            primary_lead_source_id=data["lead_source_id"],
            lead_type_id=lead_type,
            lead_source_id=lead_source,
            # primary_lead_source_id=lead_source,
            centre_name=centre_name,
            lead_status_id=lead_status,
            client_id=client_id,
        )

        if data["lead_status_id"] == 23:
            lead.ringing_date = datetime.now()

        lead.product_id = product
        lead.is_potential = "no" if not data.get("is_potential") else data["is_potential"]

        try:
            lead.save()
            if lead.id is not None:
                # messages.success(request, "Lead has been added successfully")
                print("Lead ID:", lead.id)
                # return redirect('leadlisting')

                # saving answers
                postData = request.POST.get("questionForm")
                question_count = StageQuestions.objects.filter(lead_status_id=data["lead_status_id"], parent_id=None).count()
                insert_data = []

                if question_count:
                    for i in range(1, question_count+1):
                        if "answer_" + str(i) in postData and postData["answer_" + str(i)]:
                            answer_id = int(postData["answer_" + str(i)])
                            if answer_id:
                                answer_data = StageQuestions.objects.get(id=answer_id)
                                lead_score = LeadScores()
                                question_id = postData["question_" + str(i)]
                                question_data = StageQuestions.objects.get(id=question_id)
                                lead_score.question = question_data.text
                                lead_score.answer = answer_data.text
                                lead_score.score = answer_data.score
                                lead_score.lead_id = lead.id
                                lead_score.lead_status_id = data["lead_status_id"]
                                lead_score.created_at = datetime.now()
                                lead_score.updated_at = datetime.now()
                                insert_data.append(lead_score)
                    try:
                        if insert_data:
                            print("LeadScores", insert_data)
                            LeadScores.objects.bulk_create(insert_data)

                            # calculate score
                            score = LeadScores.objects.filter(lead_id=lead.id).aggregate(Sum('score'))['score__sum']
                            # if score > 0 and score <= 25:
                            #     range = "0-25"
                            # elif score >= 26 and score <= 50:
                            #     range = "26-50"
                            # elif score >= 51 and score <= 75:
                            #     range = "51-75"
                            # elif score >= 76 and score <= 1000:
                            #     range = "76-100"

                            if score > 0 and score <= 25:
                                score_range = "0-25"
                            elif score >= 26 and score <= 50:
                                score_range = "26-50"
                            elif score >= 51 and score <= 75:
                                score_range = "51-75"
                            elif score >= 76 and score <= 1000:
                                score_range = "76-100"


                            if score_range:
                                lead_type_data = LeadType.objects.filter(score_range=score_range).first()
                                lead.lead_type_id = lead_type_data.id
                                lead.save()


                            # # save status log
                            # status_log = LeadStatusLOG()
                            # status_log.lead_id = lead.id
                            # status_log.lead_status_id = data["lead_status_id"]

                            # status_log.save()

                        # status_log = LeadStatusLOG.objects.create(
                        #     lead_id=data["lead_id"],
                        #     user=request.user,
                        #     salutation=data["salutation"],
                        #     name=data["name"],
                        #     phone=data["phone"],
                        #     email=data["email"],
                        #     product_id=data["product_id"],
                        #     lead_source_id=data["lead_source_id"],
                        #     city=data["city"],
                        #     spouse_name=data["spouse_name"],
                        #     alternate_number=data["alternate_number"],
                        #     centre_name=data["centre_name"],
                        #     comment=data["comment"],
                        #     created_at = datetime.now(),
                        #     updated_at = datetime.now(),
                        # )
                        # print("Status Log ID:", status_log.id)

                        # Create and save Call if choose_date_time is not empty
                        # if data.get("date"):
                        if request.POST.get("choose_date_time"):
                            telecaller_id = request.user.id
                            if user_department != 'telcaller':
                            # Apply your logic to get telecaller_id here
                                sources_data = Sources.objects.filter(assign_user=request.user, leads__id=lead.id).first()
                                if sources_data:
                                    telecaller_id = sources_data.user_id

                            call = Calls.objects.create(
                                date=data["date"],
                                lead_id=lead,
                                lead_status_id=lead.lead_status_id,
                                status=1,
                                client_id=client_id,
                                telecallerid=telecaller_id,
                            )

                            print("Call ID:", call.id)

                        # Create and save LeadComment if comment is not empty
                        if data.get("comment"):
                            lead_comment = LeadComments.objects.create(
                                lead_id=lead,
                                comment=data["comment"],
                                client_id=client_id,
                            )
                        print("Lead Comment ID:", lead_comment.id)


                        # send email and SMS notifications
                        # if lead.status.email_template_id:
                        #     temp = template.objects.get(id=lead.status.email_template_id)
                        #     message_body = temp.message.replace("{NAME}", lead.name)
                        #     if data.get("date"):
                        #         message_body.replace("{DATE}", datetime.strptime(data["date"], '%Y-%m-%d').strftime('%Y-%m-%d'))
                        #         message_body.replace("{TIME}", datetime.strptime(data["date"], '%Y-%m-%d %H:%M:%S').strftime('%H:%M'))
                            # send_mail(
                            #     template.subject,
                            #     message_body,
                            #     settings.EMAIL_HOST_USER,
                            #     [lead.email],
                            #     fail_silently=False,
                            # )

                        # if lead.status.sms_template_id:
                        #     temp = template.objects.get(id=lead.status.sms_template_id)
                        #     message_body = temp.message.replace("{NAME}", lead.name)
                        #     if data.get("date"):
                        #         message_body.replace("{DATE}", datetime.strptime(data["date"], '%Y-%m-%d').strftime('%Y-%m-%d'))
                        #         message_body.replace("{TIME}", datetime.strptime(data["date"], '%Y-%m-%d %H:%M:%S').strftime('%H:%M'))
                            # send SMS using external service or API

                        # send email notification to admin
                        # admin_message_body = "New Lead added named " + lead.name
                        # send_mail(
                        #     "New Lead",
                        #     admin_message_body,
                        #     settings.EMAIL_HOST_USER,
                        #     [settings.NOTIFY_EMAIL],
                        #     fail_silently=False,
                        # )
                        if user_department == 'telecaller':
                            messages.success(request, "Lead has been added successfully")
                            return redirect('telecaller-lead')
                        else:
                            messages.success(request, "Lead has been added successfully")
                            return redirect('leadlisting')
                    # else:
                    #     messages.error(request, "Unable to add Lead. Please try again later")
                    #     return redirect('leadlisting')
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        messages.error(request, "Unable to add Lead. Please try again later")
                        return redirect('leadlisting')

        except Exception as e:
            print(f"An error occurred while saving the lead: {str(e)}")
            messages.error(request, "Unable to add Lead. Please try again later")
            return redirect('leadlisting')

    context.update({
    # 'ivruser': ivruser,
    'lead': lead,
    'statuses': statuses,
    'lead_types': lead_types,
    'lead_sources': lead_sources,
    'products': products,
    'user_department': user_department,
    'locations': locations,
})

    return render(request, 'lead/add.html', context)


@login_required
def update_lead(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    user_detail = UserDetails.objects.get(user_id=request.user.id)
    client_id = user_detail.uniqueid
    user_department = user_detail.department

    if request.method == 'POST':
        data = request.POST.dict()
        print('data', data)
        lead_id = data.get("id")

        if lead_id:
            try:
                lead = Leads.objects.get(pk=lead_id)
            except Leads.DoesNotExist:
                messages.error(request, "Lead not found.")
                return redirect("leadlisting")

            lead_status_id = data.get("lead_status_id")
            if lead_status_id:
                try:
                    stage = Stage.objects.get(pk=lead_status_id)
                    lead.lead_status_id = stage  # Set lead_status_id based on the stage instance
                except Stage.DoesNotExist:
                    messages.error(request, "Invalid lead status.")
                    return redirect("leadlisting")


            product_id = data.get("product_id")
            if product_id:
                try:
                    product = Product.objects.get(pk=product_id)
                    lead.product_id = product  # Set product_id based on the product instance
                except Product.DoesNotExist:
                    messages.error(request, "Invalid product.")
                    return redirect("leadlisting")

            # Compare the existing lead's attributes with the new data
            field_changes = {}
            for field in ["salutation", "name", "phone", "email", "lead_source_id", "city", "spouse_name", "alternate_number", "centre_name"]:
                if data.get(field) and getattr(lead, field) != data[field]:
                    field_changes[field] = data[field]

            # lead.product_id = data.get("product_id", lead.product_id)
            lead.is_potential = data.get("is_potential", "no")
            lead.updated_at = timezone.now()
            lead.client_id = client_id

            if field_changes:
                # Field changes occurred; create a status log entry
                status_log = LeadStatusLOG(
                    lead_id=lead,
                    lead_status_id=lead.lead_status_id,
                    user_id=request.user,
                    field_change=1,
                    client_id = lead.client_id,
                )
                for field, new_value in field_changes.items():
                    setattr(status_log, field, new_value)
                status_log.save()

            if data.get("choose_date_time"):
                # Handle calls
                telecaller_id = request.user.id
                if user_department != 'telecaller':
                    # sources_data = Sources.objects.filter(assign_user=request.user, lead_source_id=lead.lead_source_id).first()
                    # sources_data = Sources.objects.filter(assign_user= request.user, lead_source_id=data["lead_source_id"]).first()
                    sources_data = Sources.objects.filter(assign_user=request.user, name=lead.lead_source_id.name).first()

                    if sources_data:
                        telecaller_id = sources_data.user.id

                call = Calls(
                    date=data.get("date"),
                    lead_id=lead,
                    lead_status_id=lead.lead_status_id,
                    status=1,
                    telecallerid=telecaller_id,
                )
                call.save()
            else:
                # Update call status
                Calls.objects.filter(lead_id=lead).update(status=0, check_status=0)

            comment = data.get("comment")
            if comment:
                lead_comment = LeadComments(
                    lead_id=lead,
                    comment=comment,
                )
                lead_comment.save()

            messages.success(request, "Lead has been updated successfully")
        else:
            messages.error(request, "Invalid lead ID.")

        user_department = user_department  # I assume this variable is being used elsewhere

        if user_department == 1:
            return redirect("telecaller-lead")
        else:
            return redirect("leadlisting")
    else:
        # Handle GET request (display the form for updating leads)
        return render(request, "update_lead.html")



# @login_required
# def update_lead(request):
#     udetail = UserDetails.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     user_department = udetail.department

#     if request.method == 'POST':
#         # upload = LeadCreate(request.POST, client_id=client_id)
#         data = request.POST.dict()
#         print(data, '------')
#         # previous_url = data["previous_url"]
#         lead = Leads.objects.get(pk=data["id"])
#         print(lead)

#         # find data for log data changed or not
#         if lead:
#             salutation = data["salutation"] if lead.salutation != data["salutation"] else ''
#             namelog = data["name"] if lead.name != data["name"] else ''
#             phonelog = data["phone"] if lead.phone != data["phone"] else ''
#             emaillog = data["email"] if lead.email != data["email"] else ''
#             product_id = data["product_id"] if lead.product_id != data["product_id"] else ''
#             lead_sourceid = data["lead_source_id"] if lead.lead_source_id != data["lead_source_id"] else ''
#             city = data["city"] if lead.city != data["city"] else ''
#             spouse_name = data["spouse_name"] if lead.spouse_name != data["spouse_name"] else ''
#             alternate_number = data["alternate_number"] if lead.alternate_number != data["alternate_number"] else ''
#             centre_name = data["centre_name"] if lead.centre_name != data["centre_name"] else ''
#             comment = data["comment"] if data["comment"] else ''
#             if data.get("lead_status_id"):
#                 field_change = 0 if lead.lead_status_id != data["lead_status_id"] else 1
#             else:
#                 field_change = 0

#             # field_change  = 0 if lead.lead_status_id != data["lead_status_id"] else 1

#         lead.salutation = data["salutation"]
#         lead.name = data["name"]
#         lead.phone = data["phone"]
#         lead.email = data["email"]
#         lead.lead_source_id = data["lead_source_id"]
#         print(data["lead_source_id"]    , '-----------')
#         lead.city = data["city"]
#         lead.spouse_name = data["spouse_name"]
#         lead.alternate_number = data["alternate_number"]
#         lead.centre_name = data["centre_name"]

#         emailStatus = 0
#         smsStatus = 0

#         previousStatusId = lead.lead_status_id
#         if data["lead_status_id"] != previousStatusId:
#             emailStatus = 1
#             smsStatus = 1

#         if data["lead_status_id"] == 23:
#             lead.ringing_date = timezone.now()

#         lead.lead_status_id = data["lead_status_id"]
#         lead.product_id = data["product_id"]
#         lead.is_potential = data.get("is_potential", "no")
#         lead.updated_at = timezone.now()
#         lead.client_id = client_id

#         if lead.save():
#             postData = request.POST.get("questionForm")
#             postData_dict = dict(postData)
#             questionCount = StageQuestions.objects.filter(lead_status_id=data["lead_status_id"], parent_id__isnull=True).count()
#             insertData = []

#             if questionCount:
#                 for i in range(1, questionCount+1):
#                     answerId = postData_dict.get("answer_" + str(i))
#                     if answerId:
#                         answerData = StageQuestions.objects.get(pk=answerId)
#                         questionId = postData_dict.get("question_" + str(i))
#                         questionData = StageQuestions.objects.get(pk=questionId)
#                         leadScore = LeadScores(
#                             question=questionData.text,
#                             answer=answerData.text,
#                             score=answerData.score,
#                             lead=lead,
#                             lead_status_id=data["lead_status_id"],
#                             created_at=timezone.now(),
#                             updated_at=timezone.now(),
#                         )
#                         insertData.append(leadScore)

#                 LeadScores.objects.bulk_create(insertData)

#             score = LeadScores.objects.filter(lead=lead).aggregate(sum_score=models.Sum('score'))['sum_score']
#             range_ = ""
#             if score:
#                 if score > 0 and score <= 25:
#                     range_ = "0-25"
#                 elif score >= 26 and score <= 50:
#                     range_ = "26-50"
#                 elif score >= 51 and score <= 75:
#                     range_ = "51-75"
#                 elif score >= 76 and score <= 1000:
#                     range_ = "76-100"

#                 leadTypeData = LeadType.objects.filter(score_range=range_).first()
#                 if leadTypeData:
#                     lead.lead_type_id = leadTypeData.id
#                     lead.save()

#             statusLog = LeadStatusLOG(
#                 lead_id=lead,
#                 lead_status_id=lead.lead_status_id,
#                 user=request.user,
#                 salutation=salutation,
#                 name=namelog,
#                 phone=phonelog,
#                 email=emaillog,
#                 product_id=product_id,
#                 lead_source_id=lead_sourceid,
#                 city=city,
#                 spouse_name=spouse_name,
#                 alternate_number=alternate_number,
#                 centre_name=centre_name,
#                 comment=comment,
#                 field_change=field_change,
#             )
#             statusLog.save()

#             if data.get("choose_date_time"):
#                 Calls.objects.filter(lead=lead).update(status=0)
#                 user_data = request.user

#                 telecallerId = request.user.id
#                 if user_department != 'telecaller':
#                     SourcesData = Sources.objects.filter(assign_user= user_data, lead_source_id=data["lead_source_id"]).first()
#                     # SourcesData = LeadSourceUser.objects.filter(lead_source_id=data["lead_source_id"]).first()
#                     # related_sources = related_sources_data.values_list('lead_source_id', flat=True)
#                     if SourcesData:
#                        telecallerId = SourcesData.user.id

#                 calls = Calls(
#                     date=data["date"],
#                     lead_id=lead,
#                     lead_status_id=lead.lead_status_id,
#                     status=1,
#                     telecallerid=telecallerId,
#                 )
#                 calls.save()
#             else:
#                 Calls.objects.filter(lead=lead).update(status=0, check_status=0)

#             if comment:
#                 leadComment = LeadComments(
#                     lead_id=lead,
#                     comment=data["comment"],
#                 )
#                 leadComment.save()

#             if emailStatus and lead.status.email_template_id:
#               temp = template.objects.get(pk=lead.status.email_template_id)
#               temp.first_name = lead.name
#               if data.get("date"):
#                   temp.date = data["date"]

#              # send email

#             if smsStatus and lead.status.sms_template_id:
#                 temp = template.objects.get(pk=lead.status.sms_template_id)
#                 message = template.message.replace("{NAME}", ucfirst(lead.name))

#                 if data.get("date"):
#                     message.replace("{DATE}", timezone.now().strftime("%Y-%m-%d"))
#                     message.replace("{TIME}", timezone.now().strftime("%H:%M"))

#                 # send SMS

#             messages.success("Lead has been updated successfully")
#         else:
#             messages.error("error", "Unable to update lead. Please try again later")

#         usreDepartment=user_department
#         if usreDepartment == 1:
#             return redirect("telecaller-lead")
#         else:
#             return redirect("leadlisting")
#     else:
#         # upload = LeadCreate(client_id=client_id)
#         return render(request, "update_lead.html")


@login_required
def lead_edit(request, id):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)


    request.session['pagerest'] = 'true'
    # user_data = request.user
    # user_department = user_data.department
    udetail = UserDetails.objects.get(user=request.user)
    user_department = udetail.department
    # ivruser = []

    # if user_department == 1:
    #     ivruser.append({'name': user_data.name, 'user_id': user_data.ivr_user_id})
    # else:
    #     # Assuming you have an IvrController model with an ivr_user() method
    #     ivr_controller = IvrController()
    #     ivruser = ivr_controller.ivr_user()

    lead = Leads.objects.get(id=id)
    statuses = Stage.objects.filter(status='active').order_by('-id')
    lead_types = LeadType.objects.all().order_by('-id')
    lead_sources = Sources.objects.all().order_by('-id')
    products = Product.objects.all().order_by('-id')
    locations = Location.objects.all().order_by('-id')
    lead_logs = LeadStatusLOG.objects.filter(lead_id=id)
    comment_logs = LeadComments.objects.filter(lead_id=id)
    call_logs = Calls.objects.filter(lead_id=id)
    attcachment_logs = LeadAttachments.objects.filter(lead_id=id)



    # print('lead_logs----------', lead_logs)




    context.update({
        # 'ivruser': ivruser,
        'lead': lead,
        'lead_logs': lead_logs,
        'statuses': statuses,
        'lead_types': lead_types,
        'lead_sources': lead_sources,
        'products': products,
        'user_department': user_department,
        'locations': locations,
        'attcachment_logs':attcachment_logs,
        'call_logs':call_logs,
        'comment_logs':comment_logs,
    })

    return render(request, 'lead/edit.html', context)



@login_required
def leadlisting(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)


    user_data = request.user
    udetail = UserDetails.objects.get(user_id=user_data.id)
    clientid = udetail.uniqueid
    user_department = udetail.department
    shelf = Leads.objects.filter(client_id=udetail.uniqueid).order_by('-id')

    # telecaller_users = User.objects.filter(department_id=1).exclude(id=user_data.id).values('id', 'name')
    # telecallers_id = UserDetails.objects.filter(
    #     uniqueid=clientid, department='telecaller').values_list('user_id', flat=True)
    # telecaller_users = User.objects.filter(id__in=telecallers_id)
    # print(telecallers_id)

    # user_data = request.user
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
    # if ivr_users_response.status_code == 200:
    #     ivr_users_data = ivr_users_response.content
    #     ivr_users_data = json.loads(ivr_users_data.decode('utf-8')).get('user_arr', [])
        # ivr_users_data = ivr_users_response.json().get('user_arr', [])

        # print(ivr_users_data)

        # print(ivr_users_data, 'ivr_users-------')


    telecallers = UserDetails.objects.filter(uniqueid=clientid, department='telecaller').values('id', 'user__username', 'user_id')
    # print(telecallers)
    statuses = Stage.objects.filter(status='active').values('id', 'name')
    types = LeadType.objects.all().values('id', 'name')
    products = Product.objects.all().values('id', 'name')
    # product_name = get_product_by_id(lead.product_id) if lead.product_id else ''
    sources = Sources.objects.all().values('id', 'name')

    # drid = user_data.id
    lead_data = {}
    if 'edit' in request.META.get('HTTP_REFERER', ''):
        pagerest = request.session.get('pagerest')
        lead_data = request.session.get('leaddata')
        request.session.pop('leaddata', None)
    else:
        pagerest = "false"

    # leads = Leads.objects.exclude(lead_status_id=25)
    leads = Leads.objects.filter(client_id = clientid ).order_by('-id')


    try:
    # Your existing code here
        # if request.is_ajax():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            print( request.headers.get('x-requested-with') == 'XMLHttpRequest', '--------')
            # print('check get request',request.GET )

            search_text = request.GET.get('searchText')
            # print(search_text,'---------')

            status = request.GET.get('status')
            # print(status,'---------')

            lead_type = request.GET.get('type')
            product = request.GET.get('product')
            lead_source = request.GET.get('source')

            is_transferr = request.GET.get('istransfer')

            isasign = request.GET.get('isasign')

            star_lead = request.GET.get('star_lead')
            potential_lead = request.GET.get('potential_lead')

            invalidleads = request.GET.get('invalidleads')



            creation_date_sort = request.GET.get('creation_date_sort')
            filter_created_date = request.GET.get('filter_created_date')
            # filter_created_dates = request.GET.get('filter_created_dates')
            # filter_updated_date = request.GET.get('filter_updated_date')
            filter_updated_dates = request.GET.get('filter_updated_dates')
            filter_telecaller = request.GET.get('telecaller')

            # if search_text:
            #     leads = leads.filter(Q(name__icontains=search_text) | Q(phone__icontains=search_text))
            # print(search_text, 'search_text-----')
            if search_text:
                leads = leads.filter(Q(name__icontains=search_text) | Q(phone__icontains=search_text))
                # print("After search_text filter:", leads.count())



            if status:
                leads = leads.filter(lead_status_id=status)
                print("After search_text filter:", leads.count())
            print( 'status-----', status)

            if lead_type:
                leads = leads.filter(lead_type_id=lead_type)

            if product:
                leads = leads.filter(product_id=product)


            if lead_source:
                leads = leads.filter(lead_source_id=lead_source)
            if filter_created_date:
                created_date = datetime.strptime(filter_created_date, "%Y-%m-%d")
                leads = leads.filter(created_at__date=created_date.date())

            # print('filter_created_date---------', filter_updated_dates )
            if filter_updated_dates:
                updated_dates_list = filter_updated_dates.split(',')
                updated_dates_list = [datetime.strptime(date, "%Y-%m-%d") for date in updated_dates_list]
                leads = leads.filter(updated_at__date__in=updated_dates_list)
            # print('filter_telecalle--------', filter_telecaller)
            # lead_assigned_user_instance = LeadAssignedUser.objects.get(id=filter_telecaller)
            # if filter_telecaller:
            #     leads = leads.filter(assigned_to_id=filter_telecaller)
            if filter_telecaller:
                try:
                    lead_assigned_id= LeadAssignedUser.objects.filter(user_id=filter_telecaller).values('lead_id')
                    # print('lead_assigned_id---', lead_assigned_id)
                    leads = leads.filter(id__in=lead_assigned_id)
                    # print('lead---', leads)
                except LeadAssignedUser.DoesNotExist:
                    print(f"LeadAssignedUser with id={filter_telecaller} does not exist.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            total_leads_count = leads.count()

            if creation_date_sort == 'asc':
                leads = leads.order_by('created_at')
            elif creation_date_sort == 'desc':
                leads = leads.order_by('-created_at')


            if request.GET.get('filter_date_range'):
                date_range = request.GET.get('filter_date_range')
                start_date, end_date = date_range.split('-')

                start_date = datetime.strptime(start_date.strip(), "%Y-%m-%d")
                end_date = datetime.strptime(end_date.strip(), "%Y-%m-%d")

                leads = leads.filter(created_at__range=(start_date, end_date))


            print(request.GET.get('filter_update_range'))
            if request.GET.get('filter_update_range'):
                update_range = request.GET.get('filter_update_range')
                start_update, end_update = update_range.split('-')

                start_update = datetime.strptime(start_update.strip(), "%m/%d/%Y")
                end_update = datetime.strptime(end_update.strip(), "%m/%d/%Y")

                leads = leads.filter(updated_at__range=(start_update, end_update))

            if isasign == '1':
                lead_assigned_id= LeadAssignedUser.objects.filter(assigned=isasign).values('lead_id')
                print('lead_assigned_id---', lead_assigned_id)
                leads = leads.filter(id__in=lead_assigned_id)
                # print('lead_assigned_id---', lead_assigned_id)


            # print('istransferr', is_transferr)
            if is_transferr == '1':
                # print('istransferr===========', is_transferr)
                leads = leads.filter(is_transfer=is_transferr)

            if star_lead == '1':
                leads = leads.filter(star_patient='yes')
                # print('potential_lead', leads)
            if potential_lead == '1':
                leads = leads.filter(is_potential='yes')

            # if invalidleads:
            #     leads = leads.filter(lead_status_id=status)

            start = int(request.GET.get('start'))
            length = int(request.GET.get('length'))

            # print(start, length, '----------')

            # selected_lead_ids = []
            # ids = []
            # # Check if 'selected_lead_ids' is provided in the AJAX request data
            # if 'lead_check[]' in request.GET:
            #     selected_lead_ids = request.GET.getlist('lead_check[]')
            # print('selected lead',selected_lead_ids )
            # ids.extend(selected_lead_ids)
            # print('ids',ids)

            data = []
            source = ''
            for row in leads[start:start+length]:

                # cmnt = LeadComments.objects.filter(lead_id=row.id).values('comment')
                # print(cmnt)

                cmnt = LeadComments.objects.filter(lead_id=row.id).values('comment').last()
                last_comment = cmnt['comment'] if cmnt else '-'
                # print('----',type(last_comment))
                calls = Calls.objects.filter(lead_id=row.id).values('date').last()
                callbackdate = calls['date'] if cmnt else '-'

                count = LeadStatusLOG.objects.filter(lead_id=row.id).count()
                leadlogcount = count if count else '-'

                # if row.lead_source_id:
                #     sourcedata = get_source_by_id(row.lead_source_id)
                #     if sourcedata:
                #         source = f'{sourcedata.name}<a href="#" data-toggle="tooltip" title="{get_source_by_id(row.lead_source_id)}"><i class="fa fa-info-circle"></i></a>'

                is_selected = ''
                is_selected += f'<td class="sorting_1"><input type="checkbox" name="lead_check[]" id="lead_check_{row.id}" class="select-checkbox" onclick="checkassignlead({row.id})"></td>'

                actions = ''
                actions += ' <a onclick="ivrcall({phone}, {id})" style="color:red" href="javascript:void(0);" class="clicktocall" title="click2call"><i class="fa fa-volume-control-phone"></i></a>'.format(phone=row.phone, id=row.id)

                actions += ' <a href="{url}" title="Edit"><i class="fas fa-edit"></i></a>'.format(url=reverse('leads.edit', kwargs={'id': row.id}))

                actions += ' <a onclick="return confirm(`Do you really want to delete this lead?`)" style="color:red" href="{url}" title="Delete"><i class="fa fa-trash"></i></a>'.format(url=reverse('leads.delete', kwargs={'id': row.id}))

                if not row.is_transfer:
                    actions += ' <a href="#" data-lead_id="{id}" data-toggle="modal" data-target="#lead_assigning_modal" title="Add lead transfer" class="openlead_assigning_modal"><i class="fas fa-user-plus"></i></a>'.format(id=row.id)

                actions += ' <a href="#" data-lead_id="{id}" data-toggle="modal" data-target="#attachmentModal" title="Add attachment" class="openAttachmentModal"><i class="fas fa-list"></i></a>'.format(id=row.id)

                data.append({
                    # 'DT_RowId': row.id,
                    # 'DT_RowAttr': {
                    #     'status': row.lead_status_id,
                    #     'type': row.lead_type_id,
                    #     'product': row.product_id,
                    #     'source': row.lead_source_id,
                        # 'telecaller': row.assingn_user_id,
                    # },
                    # 'DT_RowClass': 'clickable-row',
                    # 'DT_RowData': {
                    #     'url': reverse('leadlisting')
                    # },
                    # 'checkbox': row.id,
                    'checkbox': is_selected,
                    'leadid': row.id,
                    'date': row.created_at.strftime("%d-%m-%Y"),
                    'city': row.city,
                    'phone': row.phone,
                    'name': row.name,
                    'product': row.product_id,
                    'updated_date': row.updated_at.strftime("%d-%m-%Y"),
                    'source': row.lead_source_id,
                    'stage': row.lead_status_id,
                    'keyword': row.gkeyword,
                    # 'communication': row.communication,
                    'comment':last_comment,
                    'callbackdate': callbackdate,
                    'leadlogcount': leadlogcount,
                    'actions': actions,
                })
                # print("Data before JSON response:", data)

            return JsonResponse({
                "draw": int(request.GET.get('draw')),
                "recordsTotal": total_leads_count,
                "recordsFiltered": total_leads_count,
                "data": data
            }, encoder=CustomJSONEncoder)
    except Exception as e:
        print("Exception:", e)

    #     return JsonResponse({
    #     'draw': int(request.GET['draw']),
    #     'recordsTotal': Leads.objects.count(),
    #     'recordsFiltered': leads.count(),
    #     'data': data,
    # })


    # print('pagerest value:', pagerest, types,lead_data)


    context.update({
        'ivruser': ivr_users_data,
        'telecaller_users': telecallers,
        # 'telecallers_id':telecallers,
        'statuses': statuses,
        'types': types,
        'products': products,
        'sources': sources,
        'pagerest': pagerest,
        'lead_data': lead_data
    })
    return render(request, "lead/index.html", context)


@login_required(login_url='/login/')
def telecaller_leads(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    # userData = request.user
    # usreDepartment = userData.department_id
    #     # user_data = request.user
    try:
        user_id = request.user.id
        telecaller_id = UserDetails.objects.get(user_id=request.user.id)
        print(user_id, telecaller_id, timezone.now(), '----------')
        clientid = telecaller_id.uniqueid
        user_department = telecaller_id.department

        # telecaller_users = User.objects.filter(department_id=1).exclude(id=userData.id).values('id', 'name')
        telecallers = UserDetails.objects.filter(uniqueid=clientid, department='telecaller').values('user_id', 'user__username')
        statuses = Stage.objects.filter(status='active').values('id', 'name')
        types = LeadType.objects.values('id', 'name')
        products = Product.objects.values('id', 'name')
        sources = Sources.objects.values('id', 'name')

        leaddata = {}
        # Handle the case where 'HTTP_REFERER' is not present
        if request.META.get('HTTP_REFERER'):
            if 'edit' in request.META.get('HTTP_REFERER'):
                pagerest = request.session.get('pagerest')
                leaddata = request.session.get('leaddata')
                request.session.pop('leaddata', None)
            else:
                pagerest = "false"
        else:
            pagerest = "false"

        leads = Leads.objects.all().order_by('-id')
        # print(leads)



        if request.is_ajax():
            locationq = request.GET.get('locationq')
            star_sort = request.GET.get('star_sort')
            unreadmsg = request.GET.get('unreadmsg')


            if request.GET.get('searchText'):
                leads = leads.filter(Q(name__icontains=request.GET.get('searchText')) | Q(phone__icontains=request.GET.get('searchText')) | Q(email__icontains=request.GET.get('searchText')) | Q(fbform_id__icontains=request.GET.get('searchText')) | Q(id__icontains=request.GET.get('searchText')))

            if request.GET.get('status'):
                leads = leads.filter(lead_status_id=request.GET.get('status'))

            if request.GET.get('type'):
                leads = leads.filter(lead_type_id=request.GET.get('type'))

            if request.GET.get('product'):
                leads = leads.filter(product_id=request.GET.get('product'))

            if request.GET.get('source'):
                leads = leads.filter(lead_source_id=request.GET.get('source'))

            if request.GET.get('filter_created_date'):
                created_date_list = request.GET.get('filter_created_date').split(',')
                created_date_list = [datetime.strptime(date, "%Y-%m-%d") for date in created_date_list]
                # leads = leads.filter(created_at__in=created_date.date())
                leads = leads.filter(created_at__date__in=created_date_list)
                # print(created_date_list,request.GET.get('filter_created_date'), leads, '***********************')



            if request.GET.get('filter_updated_date'):
                updated_dates_list = request.GET.get('filter_updated_date').split(',')
                updated_dates_list = [timezone.make_aware(datetime.strptime(date.strip(), "%Y-%m-%d"), timezone.get_default_timezone()) for date in updated_dates_list]

                leads = leads.filter(updated_at__date__in=updated_dates_list)

            if locationq:
                leads = leads.filter(centre_name=locationq)

            if star_sort:
                leads = leads.filter(star_patient=star_sort)


            if request.GET.get('transferred') == 'yes':
                leads = leads.filter(is_transfer= '1')

            if request.GET.get('filter_telecaller'):
                leads = leads.filter(assigned_to_id=request.GET.get('filter_telecaller'))

            # if request.GET.get('attachment_status'):
            #     if request.GET.get('attachment_status') == 'true':
            #         leads = leads.exclude(attachment=None)
            #     else:
            #         leads = leads.filter(attachment=None)


            if request.GET.get('creation_date_sort')  == 'asc':
                leads = leads.order_by('created_at')
            elif request.GET.get('creation_date_sort') == 'desc':
                leads = leads.order_by('-created_at')

            if request.GET.get('filter_date_range'):
                date_range = request.GET.get('filter_date_range')
                start_date, end_date = date_range.split('-')

                start_date = datetime.strptime(start_date.strip(), "%m/%d/%Y")
                end_date = datetime.strptime(end_date.strip(), "%m/%d/%Y")

                leads = leads.filter(created_at__range=(start_date, end_date))

            if request.GET.get('filter_update_range'):
                update_range = request.GET.get('filter_update_range')
                start_update, end_update = update_range.split('-')

                start_update = datetime.strptime(start_update.strip(), "%m/%d/%Y")
                end_update = datetime.strptime(end_update.strip(), "%m/%d/%Y")

                leads = leads.filter(updated_at__range=(start_update, end_update))

            # telecallerassignedleads = LeadAssignedUser.objects.filter(user_id=telecaller_id).exclude(lead__lead_status_id=25).values('lead_id')
            # telecallertransferleads = LeadTransferUser.objects.filter(user_id=telecaller_id).exclude(lead__lead_status_id=25).values('lead_id')
            # telecallerleads_arr = set(telecallerassignedleads.values_list('lead_id', flat=True)) | set(telecallertransferleads.values_list('lead_id', flat=True))

            # leads = leads.filter(id__in=telecallerleads_arr)

            selected_lead_ids = []

            # Check if 'selected_lead_ids' is provided in the AJAX request data
            # if 'leadtransferarray' in request.GET:
            # # if request.GET.get('lead_check[]'):
            #     print('working', request.GET)
            #     selected_lead_ids = request.GET.getlist('leadtransferarray[]')
            # print('selected lead',selected_lead_ids )

            # print('leadtransferarray:', request.GET.get('leadtransferarray'))

            leadtransferarray = request.POST.getlist('leadtransferarray[]')
            print('Received leadtransferarray:', leadtransferarray)


            total_leads_count = leads.count()
            lead_list = []

            start = int(request.GET.get('start'))
            length = int(request.GET.get('length'))
            # is_selected = ''
            for lead in leads[start:start+length]:
            # for lead in leads:




                is_selected = ''
                # is_selected = str(lead.id) in selected_lead_ids if selected_lead_ids else False
                # print(is_selected, '--------')

                is_selected = f'<td class="sorting_1"><input type="checkbox" name="lead_check[]" id="lead_check_{lead.id}" class="select-checkbox" onclick="checktransferlead({lead.id})" {"checked" if is_selected else ""}></td>'
                # if str(lead.id) in selected_lead_ids:
                #      print(is_selected, '----is_selected----')

                # print("Received leadtransferarray:", selected_lead_ids)

                # is_selected = str(lead.id) in selected_lead_ids
                # print(is_selected, '--------')
                # # is_selected += f'<td class="sorting_1"><input type="checkbox" name="lead_check[]" id="lead_check_{lead.id}" class="select-checkbox" onclick="checktransferlead({lead.id})"></td>'
                # # is_selected = f'<td class="sorting_1"><input type="checkbox" name="checkbox" id="lead_check_{lead.id}" class="select-checkbox" onclick="checktransferlead({lead.id})"></td>'
                # is_selected = f'<td class="sorting_1"><input type="checkbox" name="lead_check[]" id="lead_check_{lead.id}" class="select-checkbox" onclick="checktransferlead({lead.id})"></td>'




                # source = ''
                # if lead.lead_source_id:
                #     sourcedata = get_source_by_id(lead.lead_source_id)
                #     if sourcedata:
                #         source = f'{sourcedata.name}<a href="#" data-toggle="tooltip" title="{get_source_by_id(lead.lead_source_id)}"><i class="fa fa-info-circle"></i></a>'

                leadid = ''
                if lead.is_transfer == 1 and lead.transfer_to == user_id:
                    # transferred_user = get_transferred_user(lead.id)
                    transferred_user = lead.transfer_to
                    leadid += f'<span class="taglabel"><i class="fa fa-exclamation-circle" title="Transferred by {transferred_user}" aria-hidden="true"></i></span>'

                source = ''
                if lead.lead_source_id:
                    # sourcedata = get_source_by_id(lead.lead_source_id)
                    sourcedata = lead.lead_source_id

                    if sourcedata:
                        source = f'{sourcedata.name}<a href="#" data-toggle="tooltip" title="{sourcedata.name}"><i class="fa fa-info-circle"></i></a>'
                # print(source, '----------')

                actions = ''
                # leadid = ''
                # print('-------------', get_transferred_user(lead.id))
                if lead.is_transfer == 1 and lead.transfer_to != user_id:
                    transferred_by = LeadTransferUser.objects.filter(lead_id=lead.id, transferred=1).values('transferred_by').first()
                    if transferred_by:
                        transfer_by = transferred_by['transferred_by']
                        transfer_data = User.objects.filter(id=transfer_by).values('username').first()
                        if transfer_data:
                            transferred_by = transfer_data['username']

                    # tuser = lead.filter(lead.transfer_to == user_id)
                    actions += f'<span>Transferred to {transferred_by}</span>'
                    # actions += f'<span>Transferred to {sourcedata}</span>'
                else:
                    actions += ' <a href="javascript:void(0);" onclick="ivrcall({lead.phone},{lead.id})" style="color:red" class="clicktocall" title="click2call"><i class="fa fa-volume-control-phone"></i></a>'
                    # actions += f' <a href="{url}" title="Edit"><i class="fas fa-edit"></i></a>'.format(url=reverse('leads.edit', kwargs={'id': lead.id}))
                    actions += ' <a href="{url}" title="Edit"><i class="fas fa-edit"></i></a>'.format(url=reverse('leads.edit', kwargs={'id': lead.id}))

                    if user_department != 'telecaller':
                        # actions += f'<a href="{lead.get_delete_url()}" style="color:red" onclick="return confirm("Do you really want to delete this lead?")" title="Delete"><i class="fa fa-trash"></i></a>'
                        actions += ' <a onclick="return confirm(`Do you really want to delete this lead?`)" style="color:red" href="{url}" title="Delete"><i class="fa fa-trash"></i></a>'.format(url=reverse('leads.delete', kwargs={'id': lead.id}))

                    actions += ' <a href="#" data-lead_id="{lead.id}" data-toggle="modal" data-target="#attachmentModal" title="Add attachment" class="openAttachmentModal"><i class="fas fa-list"></i></a>'

                    if user_department == 'telecaller':
                        actions += f' <a onclick="openlead_transfermodal({lead.id})" href="#" class = "openlead_transfer_modal"  data-lead_id="{lead.id}" title="Add lead transfer"><i class="fas fa-exchange-alt"></i></a>'

                        # actions += f' <a onclick="openlead_transfermodal({lead.id})" title="Add lead transfer"><i class="fas fa-exchange-alt"></i></a>'

                        # actions += ' <a href="{url}" onclick="openlead_transfermodal({lead.id})" title="Add lead transfer"><i class="fas fa-exchange-alt"></i></a>'.format(url=reverse('lead_transfer', kwargs={'id': lead.id}))
                        # leadid += f'<span class="taglabel"><i class="fa fa-exclamation-circle" title="Transferred by {get_transferred_user(lead.id)}" aria-hidden="true"></i></span>'
                # print(actions, '----------')

                lead_entry = {
                    'checkbox': is_selected,
                    'leadid': lead.id,
                    'date': lead.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'city': lead.city,
                    'phone': lead.phone,
                    'name': lead.name,
                    # 'product': lead.product_id,
                    'product': lead.product_id,

                    'updated_date': lead.updated_at.strftime("%d-%m-%Y"),
                    # 'source': lead.lead_source_id,
                    'stage': lead.lead_status_id,
                    # 'keyword': lead.gkeyword,
                    'source': source,
                    'actions': actions,

                    # ... (other columns)
                }
                lead_list.append(lead_entry)
                # print(lead_entry)


            # data = {
            #     'data': lead_list,
            #     # 'draw': 1,  # Draw count for DataTables
            #     "draw": int(request.GET.get('draw')),
            #     'recordsTotal': total_leads_count,
            #     'recordsFiltered': total_leads_count,
            # }
            # print(lead_list, 'lead_list----------')
            return JsonResponse({
                    "draw": int(request.GET.get('draw')),
                    "recordsTotal": total_leads_count,
                    "recordsFiltered": total_leads_count,
                    "data": lead_list
                }, encoder=CustomJSONEncoder)
    except Exception as e:
       print("Exception:", e)
        # return render(request, 'leads/telecaller_leads.html', {'leads': leads, 'statuses': statuses, 'types': types, 'products': products, 'sources': sources, 'leaddata': leaddata, 'telecaller_users': telecaller_users, 'pagerest': pagerest})

    return render(request, 'lead/telecaller_index.html', {'leads': leads, 'statuses': statuses, 'types': types, 'products': products, 'sources': sources, 'leaddata': leaddata, 'telecaller_users': telecallers,  'pagerest': pagerest, 'user_department':user_department})
    # return render(request, "lead/telecaller_leads.html", context)




@login_required
def lead_add(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    udetail = UserDetails.objects.get(user_id=request.user.id)
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
    context.update({'leadform': upload})
    return render(request, 'lead/add.html', context)

@login_required
def lead_update(request, id):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    udetail = UserDetails.objects.get(user_id=request.user.id)
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

    context.update({'leadform': upload, 'lead_id': id, 'lead_comment': lead_comment, 'leads': lead_logs})
    return render(request, 'lead/edit.html', context)

@login_required
def lead_delete(request, id):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)


    userid = request.user.id

    udetail = UserDetails.objects.get(user_id=request.user.id)
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
    udetail = UserDetails.objects.get(user_id=request.user.id)
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


def my_view(request):

    admin_site: AdminSite = site

    if request.session.get('loggedin') == 'djangoo':
        form = StageCreate()
        return render(request, 'lead/my_form.html', {'form': form})
    else:
        return render(request, 'lead/my_form.html')


@login_required
def lead_export(request):
    telecaller_id = None
    userid = UserDetails.objects.get(user_id=request.user.id)
    # client_id = udetail.uniqueid
    # user_department = udetail.department
    user_department = userid.department
    user_data = request.user
    # user_department = user_data.UserDetails.department_id

    # leads = Leads.objects.filter(lead_status_id__ne='25')
    leads = Leads.objects.all()
    search_text = request.GET.get('searchTextnew', '')

    type_id = request.GET.get('type', '')
    source_id = request.GET.get('source', '')
    product_id = request.GET.get('product', '')
    status_id = request.GET.get('status', '')
    telecaller = request.GET.get('telecaller', '')

    if user_department == 'telecaller':
        telecaller_id = user_data.id
    # print('telecaller_id-----------', telecaller_id)
    creation_date_sort = request.GET.get('creation_date_sort', '')
    filter_date_range = request.GET.get('filter_date_range', '')
    filter_created_date = request.GET.get('filter_created_date', '')
    filter_update_range = request.GET.get('filter_update_range', '')
    filter_updated_date = request.GET.get('filter_updated_date', '')

    if search_text:
        leads = leads.filter(
            Q(name__icontains=search_text) |
            Q(id__icontains=search_text) |
            Q(email__icontains=search_text) |
            Q(phone__icontains=search_text)
        )

    if type_id:
        leads = leads.filter(lead_type_id=type_id)

    if source_id:
        leads = leads.filter(lead_source_id=source_id)

    if product_id:
        leads = leads.filter(product_id=product_id)

    if status_id:
        leads = leads.filter(lead_status_id=status_id)

    status_array = []
    source_array = []

    if telecaller_id != None:
        # related_sources_data = LeadSourceUser.objects.filter(user_id=telecaller_id)
        # related_sources = [data.lead_source_id for data in related_sources_data]
        related_sources_data = Sources.objects.filter(assign_user=user_data)
        related_sources = [data.id for data in related_sources_data]

        for value in related_sources:
            # related_status_data = LeadStatusesUsers.objects.filter(user_id=telecaller_id, lead_source_id=value)
            related_status_data = Stage.objects.filter(user_id=telecaller_id, lead_source_id=value)


            if related_status_data:
                for stage in related_status_data:
                    new_leads = Leads.objects.filter(lead_status_id=stage.lead_status_id, lead_source_id=value)
                    status_array.extend([lead.id for lead in new_leads])
            else:
                # source_data = Leads.objects.filter(lead_source_id=value, lead_status_id__ne='25')
                source_data = Leads.objects.filter(lead_source_id=value)
                source_array.extend([status_lead.id for status_lead in source_data])

        status_array = list(set(status_array))
        source_array = list(set(source_array))

        assign_leads_arr = []
        transfer_leads_arr = []
        telecaller_leads_arr = []

        # telecaller_assigned_leads = LeadAssignedUser.objects.filter(user_id=telecaller_id).filter(lead__lead_status_id__ne='25')
        telecaller_assigned_leads = LeadAssignedUser.objects.filter(user_id=telecaller_id).filter(lead__lead_status_id__ne='25')

        assign_leads_arr = [assign_lead.lead_id for assign_lead in telecaller_assigned_leads]

        telecaller_transfer_leads = LeadTransferUser.objects.filter(user_id=telecaller_id).filter(lead__lead_status_id__ne='25')
        transfer_leads_arr = [transfer_lead.lead_id for transfer_lead in telecaller_transfer_leads]

        telecaller_leads_arr = source_array + assign_leads_arr + transfer_leads_arr + status_array
        telecaller_leads_arr = list(set(telecaller_leads_arr))

        leads = leads.filter(id__in=telecaller_leads_arr)

    if filter_created_date:
        lead_from = timezone.make_aware(filter_created_date, timezone.get_current_timezone()).replace(hour=0, minute=0, second=0)
        lead_to = lead_from + timezone.timedelta(days=1)
        leads = leads.filter(created_at__gte=lead_from, created_at__lt=lead_to)

    if filter_updated_date:
        lead_from = timezone.make_aware(filter_updated_date, timezone.get_current_timezone()).replace(hour=0, minute=0, second=0)
        lead_to = lead_from + timezone.timedelta(days=1)
        leads = leads.filter(updated_at__gte=lead_from, updated_at__lt=lead_to)

    if filter_date_range:
        date_range = filter_date_range.split('-')
        lead_from = timezone.make_aware(date_range[0], timezone.get_current_timezone()).replace(hour=0, minute=0, second=0)
        lead_to = timezone.make_aware(date_range[1], timezone.get_current_timezone()).replace(hour=0, minute=0, second=0) + timezone.timedelta(days=1)
        leads = leads.filter(created_at__gte=lead_from, created_at__lt=lead_to)

    locationq = request.GET.get('locationq', '')
    if locationq:
        leads = leads.filter(centre_name=locationq)

    star_sort = request.GET.get('star_sort', '')
    if star_sort:
        leads = leads.filter(star_patient=star_sort)

    leads = leads.order_by('-id')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Export-Leads.csv"'

    writer = csv.writer(response)
    writer.writerow(['Lead ID', 'Name', 'Phone', 'Email', 'Product', 'Source', 'Status', 'Keyword', 'Added on', 'Last Comment', 'Last Comment Date'])

    for lead in leads:
        product = Product.objects.get(id=lead.product_id.id) if lead.product_id else None
        lead_status = Stage.objects.get(id=lead.lead_status_id.id) if lead.lead_status_id else None
        lead_source = Sources.objects.get(id=lead.lead_source_id.id) if lead.lead_source_id else None

        phone = lead.phone.replace("+91", "")
        lead_type = 'N/A'
        gkeyword = lead.gkeyword if lead.gkeyword else ''

        last_comment = LeadComments.objects.filter(lead_id=lead.id).order_by('-id').first()
        comment = last_comment.comment if last_comment else ''
        comment_date = last_comment.created_at.strftime('%Y-%m-%d %H:%M:%S') if last_comment else ''

        writer.writerow([lead.id, lead.name, phone, lead.email, product.name if product else '', lead_source.name if lead_source else '', lead_status.name if lead_status else '', gkeyword, lead.created_at.strftime('%Y-%m-%d %H:%M:%S'), comment, comment_date])

    return response



from random import randrange
@login_required
def import_lead(request):
    udetail = UserDetails.objects.get(user_id=request.user.id)
    clientId = udetail.uniqueid
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']

        # File Details
        filename = file.name
        extension = filename.split('.')[-1].lower()
        file_size = file.size

        # Valid File Extensions
        valid_extension = ["csv"]

        # 2MB in Bytes
        max_file_size = 2097152

        if extension in valid_extension:
            # Check file size
            if file_size <= max_file_size:
                # Import CSV to Database
                import_data = []
                for row in file.read().decode('utf-8').splitlines():
                    import_data.append(row.split(','))

                successfully_imported_leads = 0
                # print('import data --------------', import_data)
                for data in import_data:
                    name = data[0] if data[0] else "lead" + str(randrange(10000))
                    phone = data[1]
                    email = data[2] if data[2] else 'ichelon@gamil.com'
                    product_code = data[3]
                    source_token = data[4]
                    type_slug = data[5]
                    status_slug = data[6]
                    center = data[11]


                    # Look up Product, Source, Type, and Status based on provided codes/slugs
                    product = Product.objects.filter(product_code=product_code).first()
                    source = Sources.objects.filter(token=source_token).first()
                    lead_type = LeadType.objects.filter(name=type_slug).first()
                    lead_status = Stage.objects.filter(slug=status_slug).first()
                    city = Location.objects.filter(name=center).first()

                    if not lead_status:
                        lead_status = Stage.objects.get(id=1)
                    if not product:
                        product = Product.objects.get(id=1)
                    if not source:
                        source = Sources.objects.get(id=1)
                    if not lead_type:
                        lead_type = LeadType.objects.get(id=5)
                    if not city:
                        city = Location.objects.get(id=3)

                    print( '----------', product, source, lead_type, lead_status)
                    if phone:
                        duplicate_lead = Leads.objects.filter(phone__contains=phone).count()
                        if not duplicate_lead:
                            if not phone.startswith("+91"):
                                phone = "+91" + phone

                            lead_data = {
                                "salutation": "mr",
                                "name": name,
                                "phone": phone,
                                "email": email,
                                "product_id": product if product else None,
                                "lead_type_id": lead_type if lead_type else None,
                                "lead_source_id": source if source else None,
                                "lead_status_id": lead_status if lead_status else None,
                                "created_at": timezone.now(),
                                "updated_at": timezone.now(),
                                "created_by": "system" if udetail else None,
                                "is_potential": "no",
                                "centre_name": city if city else None,  #
                                "star_patient": "no",
                                "client_id": clientId,
                            }

                            lead = Leads(**lead_data)
                            try:
                                lead.full_clean()
                                lead.save()

                                # Create StatusLog
                                status_log = LeadStatusLOG(
                                    lead_id=lead,
                                    user_id=request.user,
                                    lead_status_id=lead_status,
                                )
                                status_log.save()

                                # Increment the counter for successfully imported leads
                                successfully_imported_leads += 1

                                # Send Welcome Email
                                # welcome_template = Template.objects.get(id=1)
                                # send_mail(email, welcome_template)

                                # Check and send email/sms based on lead status
                                # if lead_status and lead_status.email_template:
                                #     send_email_based_on_template(lead.email, lead_status.email_template, lead.name)

                                # if lead_status and lead_status.sms_template:
                                #     send_sms_based_on_template(lead.phone, lead_status.sms_template, lead.name)
                            except ValidationError as e:
                                # Handle validation error, if any
                                print("Found error: ", e)

                # Display success message with the count of successfully imported leads
                messages.success(request, f"{successfully_imported_leads} Leads have been imported successfully")
            else:
                messages.error(request, "File too large. File must be less than 2MB.")
        else:
            messages.error(request, "Invalid File Extension.")

        return redirect("leadlisting")
    else:
        messages.error(request, "Please select a file to import leads")
        return redirect("leadlisting")



# @login_required
# def import_lead(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']

#         # File Details
#         filename = file.name
#         extension = filename.split('.')[-1].lower()
#         file_size = file.size

#         # Valid File Extensions
#         valid_extension = ["csv"]

#         # 2MB in Bytes
#         max_file_size = 2097152

#         if extension in valid_extension:
#             # Check file size
#             if file_size <= max_file_size:
#                 # Import CSV to Database
#                 import_data = []
#                 for row in file.read().decode('utf-8').splitlines():
#                     import_data.append(row.split(','))

#                 for data in import_data:
#                     name = data[0] if data[0] else "lead" + str(randrange(10000))
#                     phone = data[1]
#                     email = data[2] if data[2] else 'ichelon@gamil.com'
#                     product_code = data[3]
#                     source_token = data[4]
#                     type_slug = data[5]
#                     status_slug = data[6]

#                     # Look up Product, Source, Type, and Status based on provided codes/slugs
#                     product = Product.objects.filter(product_code=product_code).first()
#                     source = Sources.objects.filter(token=source_token).first()
#                     lead_type = LeadType.objects.filter(name=type_slug).first()
#                     lead_status = Stage.objects.filter(slug=status_slug).first()

#                     if not lead_status:
#                         lead_status = Stage.objects.get(id=1)

#                     if phone:
#                         duplicate_lead = Leads.objects.filter(phone__contains=phone).count()
#                         if not duplicate_lead:
#                             if not phone.startswith("+91"):
#                                 phone = "+91" + phone

#                             lead_data = {
#                                 "name": name,
#                                 "phone": phone,
#                                 "email": email,
#                                 "product_id": product.id if product else None,
#                                 "lead_type_id": lead_type.id if lead_type else None,
#                                 "lead_source_id": source.id if source else None,
#                                 "lead_status_id": lead_status if lead_status else None,  # Assign the Stage instance
#                                 "created_at": timezone.now(),
#                                 "updated_at": timezone.now(),
#                             }


#                             lead = Leads(**lead_data)
#                             try:
#                                 lead.full_clean()
#                                 lead.save()

#                                 # Create StatusLog
#                                 status_log = LeadStatusLOG(
#                                     lead=lead,
#                                     user=request.user,
#                                     lead_status=lead_status,
#                                 )
#                                 status_log.save()

#                                 # Send Welcome Email
#                                 # welcome_template = Template.objects.get(id=1)
#                                 # send_mail(email, welcome_template)

#                                 # Check and send email/sms based on lead status
#                                 # if lead_status and lead_status.email_template:
#                                 #     send_email_based_on_template(lead.email, lead_status.email_template, lead.name)

#                                 # if lead_status and lead_status.sms_template:
#                                 #     send_sms_based_on_template(lead.phone, lead_status.sms_template, lead.name)
#                             except ValidationError as e:
#                                 # Handle validation error, if any
#                                 print("Found error: ", e)

#                 messages.success(request, "Leads have been imported successfully")
#             else:
#                 messages.error(request, "File too large. File must be less than 2MB.")
#         else:
#             messages.error(request, "Invalid File Extension.")
#         print('lead_data----------', lead_data)

#         return redirect("leadlisting")
#     else:
#         messages.error(request, "Please select a file to import leads")
#         return redirect("leadlisting")

# @login_required
# def findslot(request):
#     try:
#         udetail = UserDetails.objects.get(user=request.user)
#         user_department = udetail.department
#         userid = request.user.id

#         slot_options = ""

#         if request.method == 'POST':
#             date = request.POST.get('date')
#             source_id = request.POST.get('lead_source_id')


#             print("Date:", date)
#             print("Source ID:", source_id)

#             # if not date:
#             #     return JsonResponse({'html': ""})

#             if user_department == 'telecaller':
#                 home_leads = Leads.objects.all()

#                 related_sources_data = Sources.objects.filter(assign_user= userid)
#                 if related_sources_data.exists():
#                     related_sources = related_sources_data.values_list("lead_source_id", flat=True)
#                     home_leads = home_leads.filter(lead_source_id__in=related_sources)

#                 assign_leads_arr = LeadAssignedUser.objects.filter(user_id= userid).values_list("lead_id", flat=True)
#                 transfer_leads_arr = LeadTransferUser.objects.filter(user_id= userid).values_list("lead_id", flat=True)

#                 telecaller_leads_arr = list(set(list(assign_leads_arr) + list(transfer_leads_arr)))
#                 home_leads = home_leads.filter(id__in=telecaller_leads_arr)

#                 telecaller_leads_record = home_leads.values_list('id', flat=True)

#                 callbacksarr = Leads.objects.filter(calls__date__icontains=date,
#                                                 calls__status=1,
#                                                 calls__telecallerid=udetail) \
#                                         .values('id', 'name', 'calls__slot') \
#                                         .order_by('calls__date') \
#                                         .distinct()
#             else:
#                 telecallerId = None
#                 if source_id:
#                     try:
#                         # Assuming `assign_user` is a ManyToManyField to the `User` model in the Sources model
#                         # source_data = Sources.objects.filter(assign_user=userid, lead_source_id=source_id)
#                         # source_data = Sources.objects.filter(lead_source_id=source_id)
#                         # Assuming the correct field name for lead_source_id is "leads"
#                         source_data = Sources.objects.filter(leads__id=source_id)
#                         # Assuming you want to get the assign_user for each instance in source_data
#                         for source_instance in source_data:
#                             user_instance = source_instance.assign_user.first()
#                             if user_instance:
#                                 telecallerId = user_instance.id
#                 # Do something with telecallerId if needed
#                     except ObjectDoesNotExist:
#                         pass

#                 # callbacksarr = Leads.objects.filter(calls__date__icontains=date, calls__status=1)
#                 # callbacksarr = Leads.objects.filter(created_at__icontains=date, calls__status=1)
#                 callbacksarr = Leads.objects.filter(created_at__icontains=date, calls__status=1)


#                 print('callbackArray', callbacksarr)
#                 if telecallerId:
#                     callbacksarr = callbacksarr.filter(calls__telecallerid=telecallerId)

#                 callbacksarr = callbacksarr.values('id', 'name', 'calls__slot') \
#                                         .order_by('calls__date') \
#                                         .distinct()

#                 print('callbackArray2', callbacksarr)

#             slotarr = timeslot.objects.exclude(slot_time__isnull=True).values_list('slot_time', flat=True)
#             allslot = list(slotarr)

#             bookslot = [callback['calls__slot'] for callback in callbacksarr]

#             result = list(set(allslot) - set(bookslot))

#             # print('result', result)
#             # slot_options = ""
#             # if result:
#             #     slot_options += "<select class='form-control select2' name='slot' id='slot' required onchange='checkslot()'>"
#             #     slot_options += "<option value=''>Select Slot</option>"
#             #     for rvalue in result:
#             #         slot_options += f"<option value='{rvalue}'>{rvalue}</option>"
#             #     slot_options += "</select><span id='sloterror'></span>"
#             # print(slot_options,'-----')
#             # return JsonResponse({'html': slot_options})
#             # return JsonResponse(slot_options)

#             if result:
#                 slot_options += "<select class='form-control select2' name='slot' id='slot' required onchange='checkSlot()'>"
#                 slot_options += "<option value=''>Select Slot</option>"
#                 for rvalue in result:
#                     slot_options += f"<option value='{rvalue}'>{rvalue}</option>"
#                 slot_options += "</select><span id='sloterror'></span>"
#             print({'html': slot_options})
#             return JsonResponse({'html': slot_options})
#     except UserDetails.DoesNotExist:
#         return JsonResponse({'html': ''})



@login_required
def findslot(request):
    try:
        udetail = UserDetails.objects.get(user=request.user)
        user_department = udetail.department
        userid = request.user.id

        slot_options = ""

        if request.method == 'POST':
            date = request.POST.get('date')
            source_id = request.POST.get('lead_source_id')

            callbacksarr = Leads.objects.filter(calls__date__icontains=date, calls__status=1)

            if user_department == 'telecaller':
                # callbacksarr = callbacksarr.filter(calls__telecallerid=udetail.user)
                callbacksarr = callbacksarr.filter(calls__telecallerid=udetail.user.id)

                assign_leads_arr = LeadAssignedUser.objects.filter(user_id=userid).values_list("lead_id", flat=True)
                transfer_leads_arr = LeadTransferUser.objects.filter(user_id=userid).values_list("lead_id", flat=True)

                telecaller_leads_arr = list(set(assign_leads_arr) | set(transfer_leads_arr))
                callbacksarr = callbacksarr.filter(id__in=telecaller_leads_arr)
            else:
                telecallerId = None
                if source_id:
                    try:
                        source_data = Sources.objects.filter(leads__id=source_id).first()
                        if source_data:
                            telecallerId = source_data.assign_user.first().id
                    except ObjectDoesNotExist:
                        pass

                if telecallerId:
                    callbacksarr = callbacksarr.filter(calls__telecallerid=telecallerId)


            slotarr = Timeslots.objects.exclude(slot_time__isnull=True).values_list('slot_time', flat=True)
            allslot = list(slotarr)

            bookslot = [callback.calls.slot for callback in callbacksarr if callback.calls.slot]

            result = list(set(allslot) - set(bookslot))

            if result:
                slot_options += "<select class='form-control select2' name='slot' id='slot' required onchange='checkSlot()'>"
                slot_options += "<option value=''>Select Slot</option>"
                for rvalue in result:
                    slot_options += f"<option value='{rvalue}'>{rvalue}</option>"
                slot_options += "</select><span id='sloterror'></span>"

            return JsonResponse({'html': slot_options})
        else:
            return JsonResponse({'html': ''})
    except UserDetails.DoesNotExist:
        return JsonResponse({'html': ''})


@login_required
def checkslot(request):
    udetail = UserDetails.objects.get(user=request.user)
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
        transferred_by_name=F('transferred_by__username')
    ).values('lead_id', 'user_id', 'transferred', 'created_at', 'transferred_by', 'transferred_by_name')

    # transferred_lead = LeadTransferUser.objects.filter(lead_id=lead_id).order_by('-id').select_related('transferred_by').values('lead_id', 'user_id', 'transferred', 'created_at', 'transferred_by__name')
    # transferred_lead = LeadTransferUser.objects \
    # .values('lead_id', 'user_id', 'transferred', 'created_at', 'transferred_by__name') \
    # .annotate(name=F('transferred_by__name')) \
    # .filter(lead_id=lead_id) \
    # .order_by('-id')

    print(lead_id, transferred_lead, '--------')
    if transferred_lead:
        for transferred in transferred_lead:
            transfer = "NO"
            if transferred['transferred'] == 1:
                transfer = "YES"
                current_assigned = "Lead currently assigned to {}.".format(transferred['transferred_by_name'])

            transferred_by = User.objects.filter(id=transferred['transferred_by']).values('id', 'username').first()

            table_html += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(transferred['transferred_by_name'], transferred['created_at'], transferred_by['username'])

    # return JsonResponse({"message": table_html, "current_assigned": current_assigned, "assign": 1})
    return JsonResponse({"message": table_html, "current_assigned": current_assigned, "assign": 1})




# @login_required
# def update_lead_transfer(request):
#     udetail = UserDetails.objects.get(user=request.user)
#     userdata = request.user
#     # print(udetail, userdata, '$$$$$$')
#     user_department = udetail.department

#     if request.method == 'POST':
#         data = request.POST
#         lead_id = data.get('transfer_lead_id')
#         user_id = data.get('telecaller')

#         # print('Transfer', lead_id, user_id)

#         try:
#             lead = Leads.objects.get(pk=lead_id)
#             lead.is_transfer = 1
#             lead.transfer_to = user_id
#             lead.save()

#             user_data = request.user
#             user_id = user_data.id

#             transferred_lead = LeadTransferUser.objects.filter(lead_id=lead_id)
#             if transferred_lead.exists():
#                 transferred_lead.update(transferred=0)

#             lead_transfer = LeadTransferUser(
#                 lead_id=lead_id,
#                 user_id=user_id,
#                 transferred=1,
#                 transferred_by= userdata,
#             )
#             lead_transfer.save()

#             messages.success(request, "Lead transferred successfully")
#         except Exception as e:
#             messages.error(request, f"Unable to transferred Lead :( Please try again later {e}")

#         if user_department ==  'telecaller':
#             return redirect('telecaller-lead')
#         else:
#             return redirect('telecaller-leads')
#     else:
#         return JsonResponse({'error': 'Invalid request method'})



@login_required
def update_lead_transfer(request):
    udetail = UserDetails.objects.get(user=request.user)
    userdata = request.user
    user_department = udetail.department
    print('POST',request.POST)
    if request.method == 'POST':
        data = request.POST
        transfer_lead_id = data.get('transfer_lead_id')
        leadtransferarray = data.getlist('leadtransferarray')
        user_id = data.get('telecaller')

        print(data)

        if not transfer_lead_id and not leadtransferarray:
            messages.error(request, "Please select at least one lead to transfer.")
            return redirect('telecaller-lead')

        try:
            if transfer_lead_id:
                lead_ids = [transfer_lead_id]
            else:
                lead_ids = leadtransferarray

            for lead_id in lead_ids:
                lead = Leads.objects.get(pk=lead_id)
                lead.is_transfer = 1
                lead.transfer_to = user_id
                lead.save()

                user_data = request.user
                user_id = user_data.id

                transferred_lead = LeadTransferUser.objects.filter(lead_id=lead_id)
                if transferred_lead.exists():
                    transferred_lead.update(transferred=0)

                lead_transfer = LeadTransferUser(
                    lead_id=lead_id,
                    user_id=user_id,
                    transferred=1,
                    transferred_by=userdata,
                )
                lead_transfer.save()

            messages.success(request, "Leads transferred successfully")
        except Exception as e:
            messages.error(request, f"Unable to transfer leads: {e}")

        if user_department == 'telecaller':
            return redirect('telecaller-lead')
        else:
            return redirect('telecaller-lead')
    else:
        return JsonResponse({'error': 'Invalid request method'})

# @login_required
# def update_lead_transfer(request):
#     udetail = UserDetails.objects.get(user=request.user)
#     userdata = request.user
#     user_department = udetail.department

#     if request.method == 'POST':
#         data = request.POST
#         transfer_lead_id = data.get('transfer_lead_id')
#         leadtransferarray = data.getlist('leadtransferarray')
#         user_id = data.get('telecaller')

#         print(data, transfer_lead_id, leadtransferarray, user_id)

#         if not transfer_lead_id and not leadtransferarray:
#             messages.error(request, "Please select at least one lead to transfer.")
#             return redirect('telecaller-lead')

#         try:
#             if transfer_lead_id:
#                 lead_ids = [transfer_lead_id]
#             else:
#                 lead_ids = leadtransferarray

#             for lead_id in lead_ids:
#                 lead = Leads.objects.get(pk=lead_id)
#                 lead.is_transfer = 1
#                 lead.transfer_to = user_id
#                 lead.save()

#                 user_data = request.user
#                 user_id = user_data.id

#                 transferred_lead = LeadTransferUser.objects.filter(lead_id=lead_id)
#                 if transferred_lead.exists():
#                     transferred_lead.update(transferred=0)

#                 lead_transfer = LeadTransferUser(
#                     lead_id=lead_id,
#                     user_id=user_id,
#                     transferred=1,
#                     transferred_by=userdata,
#                 )
#                 lead_transfer.save()

#             messages.success(request, "Leads transferred successfully")
#         except Exception as e:
#             messages.error(request, f"Unable to transfer leads: {e}")

#         if user_department == 'telecaller':
#             return redirect('telecaller-lead')
#         else:
#             return redirect('telecaller-lead')
#     else:
#         return JsonResponse({'error': 'Invalid request method'})



@csrf_exempt
def lead_assigned_user(request):
    # lead_id = request.GET.get('lead_id')  # Use 'lead_id' instead of 'assigning_lead_id'
    lead_id = request.POST.get('lead_id')
    # print(lead_id)

    multipleassign = request.POST.get('multipleassign')
    leadassignarray = request.POST.getlist('leadassignarray[]') #leadassignarray[]
    # Handle the case when no leads are selected
    if multipleassign == '1' and not leadassignarray:
        return JsonResponse({"message": "Please select lead(s) to assign.", "success": 0})



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




# @login_required
# def update_lead_assigning(request):
#     udetail = UserDetails.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid

#     lead_id = request.POST.get('assigning_lead_id') #assigning_lead_id
#     user_id = request.POST.get('telecaller')

#     # if not lead_id:
#     #     return JsonResponse({"message": "No Selected lead ID .", "assign": 0})

#     print(lead_id, user_id)

#     # Retrieve the User object based on user_id
#     user = get_object_or_404(User, id=user_id)

#     lead = get_object_or_404(Leads, id=lead_id)


#     leadassign = LeadAssignedUser(
#         lead_id=lead.id,
#         user_id=user,  # Assign the User object instead of user_id
#         assigned=1,
#         client_id=client_id
#     )

#     try:
#         leadassign.save()  # No need for the if statement

#         messages.success(request, "Lead assigned successfully")
#     except Exception as e:
#         messages.error(request, f"An error occurred while updating the lead: {str(e)}")

#     return redirect('leadlisting')



@login_required
def update_lead_assigning(request):
    udetail = UserDetails.objects.get(user_id=request.user.id)
    client_id = udetail.uniqueid
    print('request.POST--------', request.POST.get)

    # print(json.loads(request.body.decode('utf-8')))
    # print('leadassignarray:', leadassignarray)

    assigning_lead_id = request.POST.get('assigning_lead_id')
    telecaller = request.POST.get('telecaller')
    multipleassign = request.POST.get('multipleassign')
    # leadassignarray = request.POST.getlist('leadassignarray') #leadassignarray[]
    # leadassignarray = request.POST.get('leadassignarray')
    leadassignarray = request.POST.getlist('leadassignarray')
    print('leadassignarray-----',  leadassignarray)
    # data = json.loads(request.body.decode('utf-8'))
    # leadassignarray = data.get('leadassignarray', [])
    # print('request.POST.getlist',request.POST.getlist('leadassignarray'))
    print(leadassignarray, multipleassign, assigning_lead_id, telecaller, '-------------------')

    # print(json.loads(request.body.decode('utf-8')))
    # print('leadassignarray:', leadassignarray)


    # Handle the case when no leads are selected
    if multipleassign == '1' and not leadassignarray:
        return JsonResponse({"message": "Please select lead(s) to assign.", "success": 0})
        # messages.error(request, "Please select lead(s) to assign.")
        # return redirect('leadlisting')

    try:
        if assigning_lead_id:
            lead = get_object_or_404(Leads, id=assigning_lead_id)
            user = get_object_or_404(User, id=telecaller)
            print('telecaller: ', user)
            leadassign = LeadAssignedUser(
                lead_id=lead.id,
                user_id=user,
                assigned=1,
                client_id=client_id
            )
            leadassign.save()

        # Assign the selected leads to the specified telecaller
        if leadassignarray:
            for lead_id in leadassignarray:
                lead = get_object_or_404(Leads, id=lead_id)
                user = get_object_or_404(User, id=telecaller)
                print('telecaller: ', user)
                leadassign = LeadAssignedUser(
                    lead_id=lead.id,
                    user_id=user,
                    assigned=1,
                    client_id=client_id
                )
                leadassign.save()

        # Provide a success message
        # return JsonResponse({"message": "Leads assigned to successfully.", "success": 1})
        messages.success(request, f"Leads assigned to {user} successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        # return JsonResponse({"message": f"An error occurred: {str(e)}", "success": 0})
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
#     udetail = UserDetails.objects.get(user_id=request.user.id)
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



#     telecallers = UserDetails.objects.filter(uniqueid=clientid, department='telecaller').values('user_id', 'user__username')
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
        context = {}
        template_layout = TemplateLayout()
        context = template_layout.init(context)
        udetail = UserDetails.objects.get(user_id=request.user.id)
        clientid = udetail.uniqueid

        telecallers = UserDetails.objects.filter(uniqueid=clientid, department='telecaller').values('user_id', 'user__username')
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
    context.update({
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
        })
    return render(request,"lead/leadlogs.html",context)


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
        context = {}
        template_layout = TemplateLayout()
        context = template_layout.init(context)

        udetail = UserDetails.objects.get(user_id=request.user.id)
        shelf = LeadType.objects.filter(
            client_id=udetail.uniqueid).all().order_by('-id')
        # shelf = Sources.objects.all().order_by('-id')
        paginator = Paginator(shelf, 3)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # print(page_obj)
    except LeadType.DoesNotExist:
        page_obj = None
    context.update({'page_obj': page_obj})
    return render(request, 'leadType/index.html', context)


@login_required
def leadType_add(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)


    udetail = UserDetails.objects.get(user_id=request.user.id)
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
    context.update({'leadform': upload})
    return render(request, 'leadType/add.html', context)


@login_required
def leadType_update(request, pk):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    udetail = UserDetails.objects.get(user_id=request.user.id)
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
    context.update({'leadform': upload})
    return render(request, 'leadType/edit.html', context)


@login_required
def leadType_delete(request, pk):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)
    leadType = get_object_or_404(LeadType, pk=pk)
    if request.method == 'POST':
        leadType.delete()
        messages.success(request, 'LeadType deleted successfully.')
        return redirect('leadTypes')
    context.update({'leadType': leadType})
    return render(request, 'leadType/delete.html', context)


@login_required
def sources(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)
    try:
        udetail = UserDetails.objects.get(user_id=request.user.id)
        shelf = Sources.objects.filter(
            client_id=udetail.uniqueid).all().order_by('-id')
        # shelf = Sources.objects.all().order_by('-id')
        paginator = Paginator(shelf, 3)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # print(page_obj)
    except Sources.DoesNotExist:
        page_obj = None
    context.update({'page_obj': page_obj})
    return render(request, 'source/index.html', context)


@login_required
def source_add(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)
    udetail = UserDetails.objects.get(user_id=request.user.id)
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
    context.update({'leadform': upload, 'user_department': udetail.department})
    return render(request, 'source/add.html', context)


@login_required
def source_update(request, id):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)
    udetail = UserDetails.objects.get(user_id=request.user.id)
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
    context.update({'leadform': upload, 'user_department': udetail.department, 'id': id})
    return render(request, 'source/edit.html', context)


def stages(request):
    try:
        context = {}
        template_layout = TemplateLayout()
        context = template_layout.init(context)
        udetail = UserDetails.objects.get(user_id=request.user.id)
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
    context.update({'page_obj': page_obj})
    return render(request, 'stage/index.html', context)


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
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)
    udetail = UserDetails.objects.get(user_id=request.user.id)
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
    context.update({'form': upload})
    return render(request, 'stage/add.html', context)


@login_required
def stage_update(request, id):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)
    udetail = UserDetails.objects.get(user_id=request.user.id)
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
    context.update({'form': upload, 'stage': stage})
    return render(request, 'stage/edit.html', context)
