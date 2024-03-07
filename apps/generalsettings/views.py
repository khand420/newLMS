from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect
from .models import generalsettings
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib import messages
from .forms import SettingsCreate
# from datetime import datetime, date, time, timedelta
from datetime import datetime, timedelta
import ast



from django.contrib.auth.decorators import login_required
from .forms import SettingsCreate
from apps.authentication.models import UserDetails
# from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import MyPasswordChangeForm

from django.http import JsonResponse
from django.utils import timezone

from .models import generalsettings
from apps.leads.models import Leads, Sources,LeadAssignedUser,LeadTransferUser, Stage
from apps.calls.models import Calls, Timeslots
from apps.calls.forms import Slotform
from django.db.models import Q

from .models import TellyCommSettings
from .forms import TellyCommForm, OutgoingCallFormset
from web_project import TemplateLayout

@login_required
def change_password(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = MyPasswordChangeForm(request.user)
    context.update({'form': form})
    return render(request, 'password/change_password.html', context)


# @login_required
# def settings(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     alldata = generalsettings.objects.all()

#     user_data = request.user

#     home_leads = Leads.objects.all()
#     related_sources_data = Sources.objects.filter(assign_user=user_data).values_list('id', flat=True)
#     print(related_sources_data)
#     if related_sources_data:
#         home_leads = home_leads.filter(lead_source_id__in=related_sources_data)
#     print(home_leads)


#     # telecaller_assigned_leads = home_leads.filter(telecaller_assigned_users__user=user_data).values_list('id', flat=True)
#     # telecaller_assigned_leads = home_leads.filter(telecaller_assigned_users=user_data).values_list('id', flat=True)
#     # telecaller_assigned_leads = home_leads.filter(telecaller_assigned_user=user_data).values_list('id', flat=True)
#     telecaller_assigned_leads = home_leads.filter(telecaller_assigned=user_data).values_list('id', flat=True)




#     print(telecaller_assigned_leads)
#     telecaller_leads = set(list(telecaller_assigned_leads))
#     home_leads = home_leads.filter(Q(id__in=telecaller_leads) | Q(lead_source_id__in=related_sources_data))

#     telecaller_leads_record = home_leads.values_list('id', flat=True)
#     telecaller_leads_record = set(telecaller_leads_record)

#     callbacks_arr = Leads.objects.filter(
#         calls__date__icontains=date,
#         calls__status=1,
#         calls__telecallerid=user_data.id
#     ).values('id', 'name', 'calls__slot').order_by('calls__date').distinct()

#     slot_arr = timeslot.objects.exclude(slot_time__isnull=True).values_list('slot_time', flat=True)
#     all_slot = list(slot_arr)

#     book_slot = callbacks_arr.values_list('calls__slot', flat=True)
#     book_slot = list(book_slot)

#     result = list(set(all_slot) - set(book_slot))

#     print(result)






#     # sources = Leads.objects.filter(leds=source_id)
#     # user_ids = sources.values_list('assign_user__user_id', flat=True)
#     # print(user_ids)
#     # related_sources_data = Leads.objects.filter(client_id=client_id).values_list('lead_source_id', flat=True).last()
#     # related_sources_data = Leads.objects.filter(client_id=client_id).values_list('lead_source__user_id', flat=True).first()
#     # sources = Sources.objects.filter(assign_user__source_id=related_sources_data)
#     # sources = Sources.objects.filter(assign_user__source_id=related_sources_data)
#     # sources = Sources.objects.filter(assign_user__id=related_sources_data)
#     # print(related_sources_data)
#     # print(sources)


#     # date = request.POST['date']
#     # client_id = request.POST['lead_source_id']

#     # print(f"Date: {date}")
#     # print(f"Client ID: {client_id}")

#     # # Querying leads to get related source IDs
#     # related_sources_data = Leads.objects.filter(client_id=client_id).values_list('lead_source_id', flat=True)

#     # print(f"Related Sources: {related_sources_data}")

#     # # Querying calls based on status, date, and user_id
#     # callbacks_arr = calls.objects.filter(status='1', date=date, user_id__in=related_sources_data)

#     # print(f"Callbacks Array: {callbacks_arr}")

#     # # Saving data to the calls table
#     # for source_id in related_sources_data:
#     #     call = calls()
#     #     call.status = '1'
#     #     call.date = date
#     #     call.user_id = source_id
#     #     call.save()

#     # return JsonResponse({'message': 'Data saved successfully'})



#     save = 0
#     if request.method == 'POST':
#         start_time = request.POST.get('start_time', '')
#         end_time = request.POST.get('end_time', '')
#         totalminutes = findminutes(start_time, end_time)

#         reqdata = list(request.POST.items())

#         for field_name, value in reqdata:
#             form = SettingsCreate(request.POST)
#             if form.is_valid():
#                 if field_name != 'csrfmiddlewaretoken':
#                     delrecord = generalsettings.objects.filter(meta_key=field_name).delete()
#                     form.instance.meta_key = field_name
#                     form.instance.meta_value = value
#                     form.instance.created_by = request.user
#                     form.instance.client_id = client_id

#                     form.save()
#                     save = 1
#         end = ''
#         if save == 1:
#             if totalminutes:
#                 print('totalminutes:', totalminutes)
#                 delete = timeslot.objects.all().delete()
#                 for i in range(1, round(totalminutes), 5):
#                     if i == 1:
#                         start = start_time
#                     else:
#                         start1 = datetime.strptime(end, "%H:%M") + timedelta(minutes=1)
#                         hour = start1.hour
#                         minute = start1.minute
#                         start = str(hour) + ":" + str(minute)

#                     end1 = datetime.strptime(start, "%H:%M") + timedelta(minutes=5)
#                     ehour = end1.hour
#                     eminute = end1.minute
#                     end = str(ehour) + ":" + str(eminute)
#                     sform = Slotform(request.POST)

#                     if sform.is_valid():
#                         sform.instance.slot_time = start + " - " + end
#                         sform.instance.created_by = request.user
#                         sform.instance.client_id = client_id
#                         sform.save()
#                     else:
#                         print('TEST')

#         messages.success(request, "General setting has been updated successfully.")
#         return redirect("/general-settings")

#     return render(request, 'generalsettings/index.html', {'alldata': alldata})



# def settings_index(request):
#     settings = generalsettings.objects.all()
#     return render(request, 'generalsettings/index.html', {'settings': settings})

# def settings_store(request):
#     if request.method == 'POST':
#         form = SettingsCreate(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             for key, value in cleaned_data.items():
#                 generalsettings.objects.filter(key=key).delete()
#                 generalsettings.objects.create(key=key, value=value)

#             request.session['message'] = "Settings have been saved successfully"
#             return redirect('generalsettings')
#         else:
#             request.session['error'] = "Unable to save settings. Please try again later"
#     else:
#         form = SettingsCreate()

#     settings = generalsettings.objects.all()
#     return render(request, 'generalsettings/index.html', {'form': form, 'settings': settings})


# def update_general_settings(request):
#     if request.method == 'POST':
#         form = SettingsCreate(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             start_time = cleaned_data['start_time']
#             end_time = cleaned_data['end_time']
#             totalminutes = findminutes(start_time, end_time)
#             del cleaned_data['start_time']
#             del cleaned_data['end_time']
#             generalsettings.objects.all().delete()
#             timeslot.objects.exclude(slot_time__isnull=True).delete()

#             data = [{'meta_key': key, 'meta_value': value, 'created_by': request.user.id, 'created_at': timezone.now()} for key, value in cleaned_data.items()]
#             generalsettings.objects.bulk_create([generalsettings(**item) for item in data])

#             if totalminutes:
#                 for i in range(1, totalminutes, 5):
#                     start = start_time if i == 1 else (timezone.datetime.strptime(end, "%H:%M") + timezone.timedelta(minutes=1)).strftime("%H:%M")
#                     end = (timezone.datetime.strptime(start, "%H:%M") + timezone.timedelta(minutes=5)).strftime("%H:%M")
#                     timeslot.objects.create(slot_time=f"{start}-{end}", created_by=request.user.id, created_at=timezone.now())

#             request.session['message'] = "General setting has been updated successfully"
#             return redirect("generalsettings")
#         else:
#             request.session['error'] = "Unable to update general settings. Please try again later"
#     else:
#         form = SettingsCreate()

#     return render(request, 'generalsettings/index.html', {'form': form})


@login_required
def Genearalsettings(request):
    context = {}
    template_layout = TemplateLayout()
    # Call the init method with the context
    context = template_layout.init(context)
    general_settings = generalsettings.objects.all()
    path = '/images/logo/'  # Replace this with the correct path for your Django project
    context.update({"general_settings": general_settings, "path": path})
    return render(request, "generalsettings/gsettings.html", context)



@login_required
def update_general_settings(request):
    context = {}
    template_layout = TemplateLayout()
    # Call the init method with the context
    context = template_layout.init(context)
    udetail = UserDetails.objects.get(user_id=request.user.id)
    client_id = udetail.uniqueid
    data = []
    inputs = request.POST.dict()

    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')

    totalminutes = 0

    if start_time and end_time:
        try:
            start_time = datetime.strptime(start_time, "%H:%M")
            end_time = datetime.strptime(end_time, "%H:%M")
            totalminutes = int(findminutes(start_time, end_time))
            print(totalminutes)
        except ValueError:
            print("start_time or end_time is not in the correct format")  # Handle the case if start_time or end_time is not in the correct format

    for key, input_value in inputs.items():
        generalsettings.objects.filter(meta_key=key).delete()
        meta_value = ""

        if input_value != '':
            data.append({"meta_key": key, "meta_value": input_value, "created_at": timezone.now(), "created_by": request.user,  "client_id": client_id})

    if generalsettings.objects.bulk_create([generalsettings(**item) for item in data]):
        if totalminutes:
            Timeslots.objects.exclude(slot_time=None).delete()
            for i in range(1, int(totalminutes) + 1, 5):
                start = start_time if i == 1 else (start + timedelta(minutes=1))
                end = (start + timedelta(minutes=5))
                Timeslots.objects.create(slot_time=start.strftime('%H:%M') + '-' + end.strftime('%H:%M'), created_by=request.user, created_at=timezone.now(), client_id= client_id)

        messages.success(request, "General setting has been updated successfully")
    else:
        messages.error(request, "Unable to update user. Please try again later")

    return redirect("general-settings")




# @login_required
# def update_telly_Communication(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     if request.method == 'POST':
#         # form = TellyCommForm(request.POST)
#         form = TellyCommForm(request.POST, instance=request.user)
#         if form.is_valid():
#             # Split the input into a list of phone numbers
#             multiplephone = form.cleaned_data['phones']
#             phone_numbers = [phone.strip() for phone in multiplephone.split(',')]
#             print(phone_numbers)

#             # Save the form with the list of phone numbers
#             tellycomm = form.save(commit=False)
#             tellycomm.phones = phone_numbers
#             tellycomm.client_id = client_id
#             tellycomm.created_by = request.user
#             tellycomm.save()
#             print(tellycomm, '----------')
#             messages.success(request, 'Your Telly Communication has been updated successfully.')
#             return redirect('update_telly_Communication_settings')
#     else:
#         # form = TellyCommForm()
#         form = TellyCommForm(instance=request.user)
#     return render(request, 'tellyComm/settings.html', {'form': form})



@login_required
def update_telly_Communication(request):
    context = {}
    template_layout = TemplateLayout()
    # Call the init method with the context
    context = template_layout.init(context)
    udetail = UserDetails.objects.get(user_id=request.user.id)
    client_id = udetail.uniqueid
    general_settings = TellyCommSettings.objects.all()

    # data = TellyCommSettings.objects.all().first()
    # phone = data.phones
    # source_id  = data.source_id.id
    # client_id = data.client_id
    # phone  = data.phones

    # print('=>',source_id, client_id, phone, '===============')


    try:
        tellycomm = TellyCommSettings.objects.get(client_id=client_id)
    except TellyCommSettings.DoesNotExist:
        tellycomm = None

    if request.method == 'POST':
        if tellycomm is not None:
            form = TellyCommForm(request.POST, instance=tellycomm)
        else:
            form = TellyCommForm(request.POST)

        if form.is_valid():
            multiplephone = form.cleaned_data['phones']
            # phone_numbers = [phone.strip() for phone in multiplephone.split(',')]

            tellycomm = form.save(commit=False)
            tellycomm.phones = multiplephone
            tellycomm.client_id = client_id
            tellycomm.created_by = request.user
            tellycomm.save()
            messages.success(request, 'Your Telly Communication has been updated successfully.')
            return redirect('update_telly_Communication_settings')
    else:
        if tellycomm is not None:
            form = TellyCommForm(instance=tellycomm)
        else:
            form = TellyCommForm()
    context.update({'form': form,'general_settings':general_settings })
    return render(request, 'tellyComm/settings.html',context)


# Lead Types
def communications_list(request):
    context = {}
    template_layout = TemplateLayout()
    # Call the init method with the context
    context = template_layout.init(context)
    try:
        udetail = UserDetails.objects.get(user_id=request.user.id)
        shelf  = TellyCommSettings.objects.filter(
            client_id=udetail.uniqueid).all().order_by('-id')
        # shelf = Sources.objects.all().order_by('-id')
        paginator = Paginator(shelf, 5)

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

            print(userdata)

            names_list = userdata[0]['name']
            uuids_list = userdata[0]['uuid']

            # Create a list of dictionaries in the desired format
            user_arr = [{'user_id': uuid, 'name': name} for name, uuid in zip(names_list, uuids_list)]

            # Print the resulting list
            print(user_arr)



        # userdata = [
        #         {'uuid': '1111111111', 'name': 'aman'},
        #         {'uuid': '2222222222', 'name': 'saif'}
        #     ]

        # user_arr = [{'user_id': val['uuid'], 'name': val['name']} for val in userdata]
        # print(user_arr)


        # names_str = mydata.outgoing_call_name[0]
        # uuids_str = mydata.outgoing_call_phone[0]

        # # Extracting names and UUIDs from the strings
        # names = [name.strip("[]'") for name in names_str.split(", ")]
        # uuids = [uuid.strip("[]'") for uuid in uuids_str.split(", ")]

        # # Creating the desired format
        # userdata = [{'name': name, 'uuid': uuid} for name, uuid in zip(names, uuids)]

        # print(userdata)



        # leads = TellyCommSettings.objects.filter(phones = '222222222')
        # if leads.exists():
        #     source_id = leads[0].source_id.id
        #     client_id2 = leads[0].client_id
        #     # print(source_id,client_id2 ,'----------------')
        # else:
        #     # Handle the case where no records match the filter
        #     print("No records found for phones='222222222'")
        # username = userdetail.objects.filter(uniqueid = client_id2, department = 'client').values('user__username')
        # print(username, '++++++ ')


        # source_id  = leads.source_id
        # print(leads)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # print(page_obj)
    except LeadAssignedUser.DoesNotExist:
        page_obj = None
    context.update({'page_obj': page_obj})
    return render(request, 'tellyComm/index.html', context)


# @login_required
# def add_commu(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     upload = TellyCommForm(request=request)
#     if request.method == 'POST':
#         upload = TellyCommForm(request.POST, request.FILES, request=request)
#         if upload.is_valid():
#             commu = upload.save(commit=False)
#             commu.client_id = udetail.uniqueid
#             commu.created_by = request.user

#             # Check uniqueness of name field
#             phone = upload.cleaned_data['phones']
#             if TellyCommSettings.objects.filter(phones=phone).exists():
#                 messages.error(request, 'Phone Number must be unique.')
#             else:
#                 upload.save()
#                 messages.success(request, 'TellyComms added successfully.')
#                 return redirect('communication_list')
#         else:
#             errors = upload.errors.as_data()
#             for field, field_errors in errors.items():
#                 for error in field_errors:
#                     messages.error(request, f'{field}: {error}')

#     return render(request, 'tellyComm/add.html', {'leadform': upload})

# @login_required
# def add_commu(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     upload = TellyCommForm(request=request)

#     if request.method == 'POST':
#         upload = TellyCommForm(request.POST, request.FILES, request=request)
#         if upload.is_valid():
#             commu = upload.save(commit=False)
#             commu.client_id = udetail.uniqueid
#             commu.created_by = request.user

#             # Check uniqueness of phones field
#             phone = upload.cleaned_data['phones']
#             if TellyCommSettings.objects.filter(phones=phone).exists():
#                 messages.error(request, 'Phone Number must be unique.')
#             else:
#                 upload.save()

#                 # Handle multiple name and phone fields
#                 outgoing_field = request.POST.get('outgoingcall')
#                 name_fields = request.POST.getlist('outgname')
#                 phone_fields = request.POST.getlist('outgphone')

#                 print('n_name........', name_fields, phone_fields)

#                 for i in range(len(name_fields)):
#                     outgname = name_fields[i]
#                     outgphone = phone_fields[i]

#                     # Create a new TellyCommSettings record for each name and phone
#                     TellyCommSettings.objects.create(
#                         phones=phone,
#                         outgoing_call=commu.outgoing_field,
#                         outgoing_call_name = commu.outhgname,
#                         outgoing_call_phone = commu.outhgphone,

#                     )

#                 messages.success(request, 'TellyComms added successfully.')
#                 return redirect('communication_list')
#         else:
#             errors = upload.errors.as_data()
#             for field, field_errors in errors.items():
#                 for error in field_errors:
#                     messages.error(request, f'{field}: {error}')

#     return render(request, 'tellyComm/add.html', {'leadform': upload})


@login_required
def add_commu(request):
    context = {}
    template_layout = TemplateLayout()
    # Call the init method with the context
    context = template_layout.init(context)
    udetail = UserDetails.objects.get(user_id=request.user.id)
    upload = TellyCommForm(request=request)

    if request.method == 'POST':
        upload = TellyCommForm(request.POST, request.FILES, request=request)
        if upload.is_valid():
            commu = upload.save(commit=False)
            commu.client_id = udetail.uniqueid
            commu.created_by = request.user

            # Check uniqueness of phones field
            phone = upload.cleaned_data['phones']
            outgoing_field = request.POST.get('outgoingcall')
            name_fields = request.POST.getlist('otgname')
            phone_fields = request.POST.getlist('otgphone')
            outgphone = []
            outgname = []

            for i in range(len(name_fields)):
                otgname = name_fields[i]
                otgphone = phone_fields[i]

                outgname.append(otgname)
                outgphone.append(otgphone)


            commu.outgoing_call=outgoing_field,
            commu.outgoing_call_name=outgname,
            commu.outgoing_call_phone=outgphone,

            if TellyCommSettings.objects.filter(phones=phone).exists():
                messages.error(request, 'Phone Number must be unique.')
            else:
                upload.save()

                # for i in range(len(name_fields)):
                #     otgname = name_fields[i]
                #     otgphone = phone_fields[i]

                #     outgname.append(otgname)
                #     outgphone.append(otgphone)

                # TellyCommSettings.objects.create(
                #     outgoing_call=outgoing_field,  # Set the outgoing call value
                #     outgoing_call_name=outgname,
                #     outgoing_call_phone=outgphone,
                # )

                messages.success(request, 'TellyComms added successfully.')
                return redirect('communication_list')
        else:
            errors = upload.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'{field}: {error}')
    # print(upload, 'upload')
    context.update({'leadform': upload})
    return render(request, 'tellyComm/add.html', context)


def update_communication(request, pk):
    context = {}
    template_layout = TemplateLayout()
    # Call the init method with the context
    context = template_layout.init(context)

    udetail = UserDetails.objects.get(user_id=request.user.id)
    commu = get_object_or_404(TellyCommSettings, id=pk)

    outgoing_call_formset = OutgoingCallFormset(request.POST or None, prefix='outgoing_call')

    if request.method == 'POST':
        form = TellyCommForm(request.POST, request.FILES, instance=commu)
        # if form.is_valid():
        if form.is_valid() and outgoing_call_formset.is_valid():
            updated_commu = form.save(commit=False)
            updated_commu.client_id = udetail.uniqueid
            updated_commu.created_by = request.user

            # Check uniqueness of phones field
            phone = form.cleaned_data['phones']
            if TellyCommSettings.objects.filter(phones=phone).exclude(id=pk).exists():
                messages.error(request, 'Phone Number must be unique.')
            else:
                updated_commu.save()

                # Handle multiple name and phone fields
                # outgoing_field = request.POST.get('outgoingcall')
                # name_fields = request.POST.getlist('otgname')
                # phone_fields = request.POST.getlist('otgphone')

                # # Delete existing related TellyCommSettings records
                # # TellyCommSettings.objects.filter(telly_comm=commu).delete()

                # for i in range(len(name_fields)):
                #     otgname = name_fields[i]
                #     otgphone = phone_fields[i]

                                    # # Create a new TellyCommSettings record for each name and phone
                    # TellyCommSettings.objects.create(
                    #     telly_comm=updated_commu,
                    #     phones=phone,
                    #     outgoing_call=outgoing_field,
                    #     outgoing_call_name=otgname,
                    #     outgoing_call_phone=otgphone,
                    # )



                outgoing_field = form.cleaned_data['outgoing_call']

                for outgoing_call_form in outgoing_call_formset:
                    otgname = outgoing_call_form.cleaned_data.get('outgoing_call_name')
                    otgphone = outgoing_call_form.cleaned_data.get('outgoing_call_phone')

                    if otgname and otgphone:
                        TellyCommSettings.objects.create(
                            telly_comm=updated_commu,
                            phones=phone,
                            outgoing_call=outgoing_field,
                            outgoing_call_name=otgname,
                            outgoing_call_phone=otgphone,
                        )


                messages.success(request, 'TellyComms updated successfully.')
                return redirect('communication_list')
        else:
            errors = form.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = TellyCommForm(instance=commu)
    context.update({'leadform': form, 'commu': commu})
    return render(request, 'tellyComm/edit.html',context)



# @login_required
# def update_communication(request, pk):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     TellyComm = get_object_or_404(TellyCommSettings, pk=pk)
#     if request.method == 'POST':
#         upload = TellyCommForm(
#             request.POST, request.FILES, instance=TellyComm, request=request)
#         if upload.is_valid():
#             TellyComm = upload.save(commit=False)
#             TellyComm.client_id = udetail.uniqueid

#             # Check uniqueness of name field
#             phones = upload.cleaned_data['phones']
#             if TellyCommSettings.objects.exclude(pk=pk).filter(phones=phones).exists():
#                 messages.error(request, 'Phones must be unique.')
#             else:
#                 upload.save()
#                 messages.success(request, 'TellyComm updated successfully.')
#                 return redirect('communication_list')
#         else:
#             errors = upload.errors.as_data()
#             for field, field_errors in errors.items():
#                 for error in field_errors:
#                     messages.error(request, f'{field}: {error}')
#     else:
#         upload = TellyCommForm(instance=TellyComm, request=request)


#     return render(request, 'tellyComm/edit.html', {'leadform': upload})


@login_required
def delete_communication(request, pk):
    context = {}
    template_layout = TemplateLayout()
    # Call the init method with the context
    context = template_layout.init(context)
    TellyComm = get_object_or_404(TellyCommSettings, pk=pk)
    if request.method == 'POST':
        TellyComm.delete()
        messages.success(request, 'TellyComm deleted successfully.')
        return redirect('communication_list')

    return render(request, 'tellyComm/delete.html', context.update({'TellyComm': TellyComm}))





# @login_required
# def update_general_settings(request):
#     data = []
#     inputs = request.POST.dict()
#     print(inputs)
#     start_time = request.POST.get('start_time')
#     end_time = request.POST.get('end_time')
#     print(start_time, end_time)

#     totalminutes = 0

#     if start_time and end_time:
#         try:
#             # start_time = datetime.datetime.strptime(start_time, "%H:%M")
#             # end_time = datetime.datetime.strptime(end_time, "%H:%M")
#             # start_time = datetime.strptime(start_time, "%H:%M")
#             # end_time = datetime.strptime(end_time, "%H:%M")
#             # totalminutes = findminutes(start_time, end_time)
#             # totalminutes = findminutes(start_time, end_time)
#             totalminutes = int(findminutes(start_time, end_time))
#             print(totalminutes)
#         except ValueError:
#             print("start_time or end_time is not in the correct format")  # Handle the case if start_time or end_time is not in the correct format

#     for key, input_value in inputs.items():
#         generalsettings.objects.filter(meta_key=key).delete()
#         meta_value = ""

#         if input_value != '':
#             data.append({"meta_key": key, "meta_value": input_value, "created_at": timezone.now(), "created_by": request.user})

#     if generalsettings.objects.bulk_create([generalsettings(**item) for item in data]):
#         if totalminutes:
#             timeslot.objects.exclude(slot_time=None).delete()
#             # for i in range(1, totalminutes + 1, 5):
#             for i in range(1, int(totalminutes) + 1, 5):
#                 start = start_time if i == 1 else (end_time + timezone.timedelta(minutes=1))
#                 end = (start + timezone.timedelta(minutes=5))
#                 timeslot.objects.create(slot_time=start.strftime('%H:%M') + '-' + end.strftime('%H:%M'), created_by=request.user, created_at=timezone.now())

#         messages.success(request, "General setting has been updated successfully")
#     else:
#         messages.error(request, "Unable to update user. Please try again later")

#     return redirect("general-settings")



# def findminutes(start_time, end_time):
#     diff = end_time - start_time
#     return diff.total_seconds() // 60

# def findminutes(start_time, end_time):
#     # start time and end time
#     start_time = datetime.strptime(start_time, "%H:%M")
#     end_time = datetime.strptime(end_time, "%H:%M")

#     # get difference
#     delta = end_time - start_time

#     sec = delta.total_seconds()
#     min = sec / 60
#     return min

# def findminutes(start_time,end_time):
#     # start time and end time
#     start_time = datetime.strptime(start_time, "%H:%M")
#     end_time = datetime.strptime(end_time, "%H:%M")

#     # get difference
#     delta = end_time - start_time

#     sec = delta.total_seconds()
#     # print('difference in seconds:', sec)

#     min = sec / 60
#     # print('difference in minutes:', min)

#     # get difference in hours
#     hours = sec / (60 * 60)
#     # print('difference in hours:', hours)
#     return min


def findminutes(start_time, end_time):
    # get difference
    delta = end_time - start_time

    sec = delta.total_seconds()
    min = sec / 60

    return min





# @login_required
# def findslot(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     user_department = udetail.department
#     userid = request.user

#     if request.method == 'POST':
#         date = request.POST.get('date')
#         source_id = request.POST.get('source_id')

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



# @login_required
# def checkslot(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     user_department = udetail.department
#     userid = request.user

#     msg = ""
#     if request.method == 'POST':
#         date = request.POST.get('date')
#         source_id = request.POST.get('source_id')
#         slot = request.POST.get('slot')

#         # user_data = request.user
#         # user_department = user_data.department_id
#         if user_department != 'telecaller':
#         # if user_department != 1:
#             telecallerId = None
#             if source_id:
#                 # source_data = LeadSourceUser.objects.filter(lead_source_id=source_id).first()
#                 # source_data = Sources.objects.filter(assign_user=udetail, lead_source_id=source_id).first()
#                 source_data = Sources.objects.filter(assign_user=request.user, leads__id=source.id).first()


#                 if source_data:
#                    telecallerId = source_data.user_id

#             callbacksarr = Leads.objects.filter(calls__date__icontains=date,
#                                                calls__slot__icontains=slot,
#                                                calls__status=1,
#                                                calls__telecallerid=telecallerId) \
#                                       .values('id', 'calls__slot') \
#                                       .order_by('calls__date') \
#                                       .distinct()

#             if callbacksarr.exists():
#                 msg = 'Slot is not available please select another slot'

#         return JsonResponse({'msg': msg})


from django.core.exceptions import ObjectDoesNotExist


# @login_required
# def findslot(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     user_department = udetail.department

#     if request.method == 'POST':
#         date = request.POST.get('date')
#         source_id = request.POST.get('source_id')

#         if user_department == 'telecaller':
#             # Get the leads for the telecaller
#             # home_leads = Leads.objects.filter(calls__telecallerid=udetail, calls__status=1)
#             # Assuming 'calls' is a ForeignKey or OneToOneField on the Leads model
#             home_leads = Leads.objects.filter(calls__date__icontains=date, calls__status=1)

#         else:
#             # Get the leads based on the source and user department
#             if source_id:
#                 try:
#                     source_data = Sources.objects.get(assign_user=udetail, lead_source_id=source_id)
#                     telecaller_id = source_data.user_id
#                     # home_leads = Leads.objects.filter(calls__telecallerid=telecaller_id, calls__status=1)
#                     # Assuming 'calls' is a ForeignKey or OneToOneField on the Leads model
#                     home_leads = Leads.objects.filter(calls__date__icontains=date, calls__status=1)

#                 except ObjectDoesNotExist:
#                     home_leads = Leads.objects.none()
#             else:
#                 home_leads = Leads.objects.none()

#         # Get the leads that have a callback on the specified date
#         callbacksarr = home_leads.filter(calls__date__icontains=date).values('id', 'name', 'calls__slot').order_by('calls__date').distinct()

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
# def findslot(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     user_department = udetail.department

#     if request.method == 'POST':
#         date = request.POST.get('date')
#         source_id = request.POST.get('source_id')

#         if user_department == 'telecaller':
#             # Get the leads for the telecaller
#             home_leads = Leads.objects.filter(calls__telecallerid=udetail, calls__status=1)
#         else:
#             # Get the leads based on the source and user department
#             if source_id:
#                 try:
#                     source_data = Sources.objects.get(assign_user=udetail, lead_source_id=source_id)
#                     telecaller_id = source_data.user_id
#                     home_leads = Leads.objects.filter(calls__telecallerid=telecaller_id, calls__status=1)
#                 except ObjectDoesNotExist:
#                     home_leads = Leads.objects.none()
#             else:
#                 home_leads = Leads.objects.none()

#         # Get the leads that have a callback on the specified date
#         callbacksarr = home_leads.filter(call__date__icontains=date).values('id', 'name', 'call__slot').order_by('call__date').distinct()

#         slotarr = timeslot.objects.exclude(slot_time__isnull=True).values_list('slot_time', flat=True)
#         allslot = list(slotarr)

#         bookslot = [callback['call__slot'] for callback in callbacksarr]

#         result = list(set(allslot) - set(bookslot))

#         slot_options = "<select class='form-control select2' name='slot' id='slot' required onchange='checkslot()'>"
#         slot_options += "<option value=''>Select Slot</option>"
#         for rvalue in result:
#             slot_options += f"<option value='{rvalue}'>{rvalue}</option>"
#         slot_options += "</select><span id='sloterror'></span>"

#         return JsonResponse({'html': slot_options})

# @login_required
# def findslot(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     user_department = udetail.department

#     if request.method == 'POST':
#         date = request.POST.get('date')
#         source_id = request.POST.get('source_id', None)  # Use None as the default value
#         print("Date:", date)
#         print("Source ID:", source_id)

#         if user_department == 'telecaller':
#             # Get the leads for the telecaller
#             home_leads = Leads.objects.filter(calls__telecallerid=udetail.id, calls__status=1)
#         else:
#             # Get the leads based on the source and user department
#             if source_id is not None:  # Check if source_id is not None
#                 try:
#                     source_data = Sources.objects.get(assign_user=udetail, lead_source_id=source_id)
#                     telecaller_id = source_data.user_id
#                     home_leads = Leads.objects.filter(calls__telecallerid=telecaller_id, calls__status=1)
#                 except ObjectDoesNotExist:
#                     home_leads = Leads.objects.none()
#             else:
#                 home_leads = Leads.objects.none()
#         # source_id = request.POST.get('source_id')

#         # if user_department == 'telecaller':
#         #     # Get the leads for the telecaller
#         #     home_leads = Leads.objects.filter(calls__telecallerid=udetail.id, calls__status=1)
#         # else:
#         #     # Get the leads based on the source and user department
#         #     if source_id:
#         #         try:
#         #             source_data = Sources.objects.get(assign_user=udetail, lead_source_id=source_id)
#         #             telecaller_id = source_data.user_id
#         #             home_leads = Leads.objects.filter(calls__telecallerid=telecaller_id, calls__status=1)
#         #         except ObjectDoesNotExist:
#         #             home_leads = Leads.objects.none()
#         #     else:
#         #         home_leads = Leads.objects.none()

#         # Get the leads that have a callback on the specified date
#         callbacksarr = home_leads.filter(calls__date__icontains=date).values('id', 'name', 'calls__slot').order_by('calls__date').distinct()

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
#         date = request.POST.get('date')
#         source_id = request.POST.get('source_id')
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





# Note: Make sure to adjust the model names and field names according to your Django models.



# def find_minutes(start_time, end_time):
#     start_object = timezone.datetime.strptime(start_time, '%H:%M')
#     end_object = timezone.datetime.strptime(end_time, '%H:%M')

#     difference = end_object - start_object

#     minutes = difference.days * 24 * 60
#     minutes += difference.seconds // 60

#     return minutes




# @login_required
# def generalsetting(request):
#     general_settings = generalsettings.objects.all()
#     path = '/images/logo/'
#     return render(request, 'settings/general_settings.html', {'general_settings': general_settings, 'path': path})

# @login_required
# def update_general_settings(request):
#     data = []
#     inputs = request.POST.copy()
#     inputs.pop('csrfmiddlewaretoken')

#     start_time = inputs.get('start_time')
#     end_time = inputs.get('end_time')
#     end = ''
#     total_minutes = find_minutes(start_time, end_time)

#     for key, value in inputs.items():
#         generalsettings.objects.filter(meta_key=key).delete()
#         meta_value = ""

#         if value != '':
#             data.append({
#                 'meta_key': key,
#                 'meta_value': value,
#                 'created_at': timezone.now(),
#                 'created_by': request.user.id
#             })

#     if generalsettings.objects.bulk_create([generalsettings(**d) for d in data]):
#         if total_minutes:
#             timeslot.objects.exclude(slot_time=None).delete()
#             for i in range(1, total_minutes + 1, 5):
#                 start = start_time if i == 1 else (end + timezone.timedelta(minutes=1)).strftime('%H:%M')
#                 end = (timezone.datetime.strptime(start, '%H:%M') + timezone.timedelta(minutes=5)).strftime('%H:%M')
#                 timeslot.objects.create(slot_time=start + '-' + end, created_by=request.user.id, created_at=timezone.now())

#         request.session.flash("message", "General setting has been updated successfully")
#     else:
#         request.session.flash("error", "Unable to update user. Please try again later")

#     return redirect("generalsettings")





# from django.http import JsonResponse
# from django.db.models import Q


# from django.http import JsonResponse
# from django.db.models import Q

# def findslot(request, leadid):
#     date = request.POST.get('date')
#     source_id = request.POST.get('source_id')

#     user_data = request.user
#     user_department = getattr(user_data, 'department', None)
#     user_department_id = getattr(user_department, 'id', None) if user_department else None

#     if user_department_id and user_department_id != 1:
#         sources_data = leadid.assign_user.first()
#         telecaller_id = getattr(sources_data, 'id', None) if sources_data else None
#     else:
#         telecaller_id = None
#         if source_id:
#             sources_data = LeadSourceUser.objects.filter(lead_source_id=source_id).first()
#             if sources_data:
#                 telecaller_id = sources_data.user_id

#     callbacks_arr = Leads.objects.filter(
#         calls__date__contains=date,
#         calls__status=1,
#         calls__telecallerid=telecaller_id
#     ).values('id', 'name', 'calls__slot').distinct().order_by('calls__date')

#     slot_arr = timeslot.objects.exclude(slot_time__isnull=True).values_list('slot_time', flat=True)
#     all_slot = list(slot_arr)

#     book_slot = callbacks_arr.values_list('calls__slot', flat=True) if callbacks_arr else []

#     result = list(set(all_slot) - set(book_slot))

#     html = ""
#     if result:
#         html += "<select class='form-control select2' name='slot' id='slot' required onchange='checkslot()'>"
#         html += "<option value=''>Select Slot</option>"

#         for slot in result:
#             html += f"<option value='{slot}'>{slot}</option>"

#         html += "</select><span id='sloterror'></span>"

#     return JsonResponse({'html': html})


# from django.http import JsonResponse
# from django.db.models import Q

# def findslot(request, leadid):
#     date = request.POST.get('date')
#     source_id = request.POST.get('source_id')

#     user_data = request.user
#     user_department = getattr(user_data, 'department', None)
#     user_department_id = getattr(user_department, 'id', None) if user_department else None

#     if user_department_id and user_department_id != 1:
#         sources_data = leadid.assign_user.first()
#         telecaller_id = getattr(sources_data, 'id', None) if sources_data else None
#     else:
#         telecaller_id = None
#         if source_id:
#             sources_data = Sources.objects.filter(id=source_id).first()
#             if sources_data:
#                 telecaller_id = sources_data.assign_user.first().id

#     callbacks_arr = Leads.objects.filter(
#         calls__date__contains=date,
#         calls__status=1,
#         calls__telecallerid=telecaller_id
#     ).values('id', 'name', 'calls__slot').distinct().order_by('calls__date')

#     slot_arr = timeslot.objects.exclude(slot_time__isnull=True).values_list('slot_time', flat=True)
#     all_slot = list(slot_arr)

#     book_slot = callbacks_arr.values_list('calls__slot', flat=True) if callbacks_arr else []

#     result = list(set(all_slot) - set(book_slot))

#     html = ""
#     if result:
#         html += "<select class='form-control select2' name='slot' id='slot' required onchange='checkslot()'>"
#         html += "<option value=''>Select Slot</option>"

#         for slot in result:
#             html += f"<option value='{slot}'>{slot}</option>"

#         html += "</select><span id='sloterror'></span>"

#     return JsonResponse({'html': html})




# def findslot(request):
#     date = request.POST['date']
#     source_id = request.POST['source_id']

#     user_data = request.user.id

#     home_leads = Leads.objects.all()
#     related_sources_data = Sources.objects.filter(assign_user=user_data).values_list('id', flat=True)

#     if related_sources_data:
#         home_leads = home_leads.filter(lead_source_id__in=related_sources_data)

#     # telecaller_assigned_leads = home_leads.filter(telecaller_assigned_users__user=user_data).values_list('id', flat=True)
#     # telecaller_leads = set(list(telecaller_assigned_leads))
#     # home_leads = home_leads.filter(Q(id__in=telecaller_leads) | Q(lead_source_id__in=related_sources_data))

#     # telecaller_leads_record = home_leads.values_list('id', flat=True)
#     # telecaller_leads_record = set(telecaller_leads_record)

#     callbacks_arr = Leads.objects.filter(
#         calls__date__icontains=date,
#         calls__status=1,
#         calls__telecallerid=user_data.id
#     ).values('id', 'name', 'calls__slot').order_by('calls__date').distinct()

#     slot_arr = timeslot.objects.exclude(slot_time__isnull=True).values_list('slot_time', flat=True)
#     all_slot = list(slot_arr)

#     book_slot = callbacks_arr.values_list('calls__slot', flat=True)
#     book_slot = list(book_slot)

#     result = list(set(all_slot) - set(book_slot))

#     html = ""
#     if result:
#         html += "<select class='form-control select2' name='slot' id='slot' required onchange='checkslot()'>"
#         html += "<option value=''>Select Slot</option>"

#         for rvalue in result:
#             html += f"<option value='{rvalue}'>{rvalue}</option>"

#         html += "</select><span id='sloterror'></span>"

#     return JsonResponse({'html': html})




# def findslot(request):
#     date = request.POST['date']
#     client_id = request.POST['lead_source_id']

#     print(f"Date: {date}")
#     print(f"Client ID: {client_id}")

#     # Querying leads to get related source IDs
#     related_sources_data = Leads.objects.filter(client_id=client_id).values_list('lead_source_id', flat=True)

#     print(f"Related Sources: {related_sources_data}")

#     # Querying calls based on status, date, and user_id
#     callbacks_arr = calls.objects.filter(status='1', date=date, user_id=related_sources_data)

#     # Filtering calls based on lead source IDs
#     if related_sources_data:
#         callbacks_arr = callbacks_arr.filter(lead__lead_source_id__in=related_sources_data)

#     # Retrieving slot information from calls
#     slot_arr = callbacks_arr.values_list('slot', flat=True)

#     print(f"Slot array: {slot_arr}")

#     # Generating HTML response
#     html = ""
#     if slot_arr:
#         html += "<option value=''>Select Slot</option>"
#         for slot in slot_arr:
#             html += f"<option value='{slot}'>{slot}</option>"

#     print(f"Generated HTML: {html}")

#     return JsonResponse({'html': html})

# def findslot(request):
#     date = request.POST['date_time_field']
#     client_id = request.POST['lead_source_id']

#     # Querying leads to get related source IDs
#     related_sources_data = Leads.objects.filter(client_id=client_id).values_list('lead_source_id', flat=True)

#     # Querying calls based on status, date, and user_id
#     callbacks_arr = calls.objects.filter(status='1', date=date, user_id=request.user.id)

#     # Filtering calls based on lead source IDs
#     if related_sources_data:
#         callbacks_arr = callbacks_arr.filter(lead__lead_source_id__in=related_sources_data)

#     # Retrieving slot information from calls
#     slot_arr = callbacks_arr.values_list('slot', flat=True)

#     # Generating HTML response
#     html = ""
#     if slot_arr:
#         html += "<option value=''>Select Slot</option>"
#         for slot in slot_arr:
#             html += f"<option value='{slot}'>{slot}</option>"

#     print(f"Slot array: {slot_arr}")
#     print(f"Generated HTML: {html}")

#     return JsonResponse({'html': html})




# def checkslot(request):

#     udetail = userdetail.objects.get(user=request.user.id)
#     client_id = udetail.uniqueid

#     msg = ""
#     date = request.POST.get('date')
#     source_id = request.POST.get('source_id')
#     slot = request.POST.get('slot')
#     # user_department = userdetail.filter(client_id = udetail, department = 'T')
#     # user_department = userdetail.objects.filter(uniqueid=client_id, department='telecaller').values_list('user_id', flat=True)
#     user_department = userdetail.objects.filter(user_id=request.user.id, department='telecaller').values_list('user_id', flat=True)


#     if user_department:
#         telecallerId = None
#         if source_id:
#             sources_data = get_object_or_404(Sources, source_id=source_id)
#             telecallerId = sources_data.user_id

#         # callbacksarr = Leads.objects.filter(calls__date__contains=date, calls__slot__contains=slot, calls__status=1, calls__telecallerid=telecallerId).values('id', 'calls__slot').order_by('calls__date').distinct()
#         callbacksarr = Leads.objects.filter(calls__date__contains=date, calls__slot__contains=slot, calls__status=1, calls__telecallerid=telecallerId).values('id', 'calls__slot').order_by('calls__date').distinct()

#         if callbacksarr:
#             msg = 'Slot is not available. Please select another slot.'

#     return JsonResponse({'msg': msg})


# @login_required
# def findslot(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid

#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client = Leads.objects.filter(client_id=udetail.uniqueid)


#     date = request.POST.get('date')
#     source_id = request.POST.get('source_id')


#     # user_department = udetail.department
#     user_department =userdetail.objects.filter(uniqueid=client_id, department='telecaller').values_list('user_id', flat=True)

#     if user_department == True:
#         home_leads = Leads.objects.all()
#         related_sources_data = Leads.objects.filter(client_id=client_id).values_list('lead_source_id', flat=True)
#         if related_sources_data:
#             home_leads = home_leads.filter(lead_source_id__in=related_sources_data)

#         assignleads_arr = Sources.objects.filter(user_id=udetail.id).values_list('lead_id', flat=True)
#         transferleads_arr = Sources.objects.filter(user_id=udetail.id).values_list('lead_id', flat=True)
#         telecallerleads_arr = list(set().union(assignleads_arr, transferleads_arr))
#         home_leads = home_leads.filter(id__in=telecallerleads_arr)

#         telecaller_leads_record = home_leads.filter(calls__date__contains=date, calls__status=1, calls__telecallerid=udetail.id).order_by('calls__date').distinct()
#     else:
#         telecallerId = None
#         if source_id:
#             sources_data = Sources.objects.filter(lead_source_id=source_id).first()
#             if sources_data:
#                 telecallerId = sources_data.user_id

#         callbacksarr = Leads.objects.filter(calls__date__contains=date, calls__status=1, calls__telecallerid=telecallerId).values('id', 'calls__slot').order_by('calls__date').distinct()

#     slotarr = timeslot.objects.exclude(slot_time=None).values_list('slot_time', flat=True)
#     allslot = list(slotarr)

#     bookslot = [callback['calls__slot'] for callback in callbacksarr] if callbacksarr else []

#     result = list(set(allslot) - set(bookslot))

#     html = ""
#     if result:
#         html += "<select class='form-control select2' name='slot' id='slot' required onchange='checkslot()'>"
#         html += "<option value=''>Select Slot</option>"
#         for slot in result:
#             html += f"<option value='{slot}'>{slot}</option>"
#         html += "</select><span id='sloterror'></span>"

#     return JsonResponse({'html': html})


# def checkslot(request):
#     msg = ""
#     date = request.POST.get('date')
#     source_id = request.POST.get('source_id')
#     slot = request.POST.get('slot')
#     user_data = request.user
#     user_department = user_data.department_id

#     if user_department != 1:
#         telecallerId = None
#         if source_id:
#             sources_data = Sources.objects.filter(source_id=source_id).first()
#             if sources_data:
#                 telecallerId = sources_data.user_id
#         callbacksarr = Leads.objects.filter(calls__date__contains=date, calls__slot__contains=slot, calls__status=1, calls__telecallerid=telecallerId).values('id', 'calls__slot').order_by('calls__date').distinct()

#         if callbacksarr:
#             msg = 'Slot is not available. Please select another slot.'

#     return JsonResponse({'msg': msg})







# @login_required
# def settings(request):
#     udetail = userdetail.objects.get(user_id=request.user.id)
#     client_id = udetail.uniqueid
#     alldata = generalsettings.objects.all()

#     save = 0
#     if request.method == 'POST':
#         start_time = request.POST.get('start_time', '')
#         end_time = request.POST.get('end_time', '')
#         totalminutes = findminutes(start_time,end_time)

#         reqdata = list(request.POST.items())

#         for field_name, value in reqdata:
#             form = SettingsCreate(request.POST)
#             if form.is_valid():
#                 # print('field_name :', field_name)
#                 if field_name != 'csrfmiddlewaretoken':
#                     delrecord = generalsettings.objects.filter(meta_key = field_name).delete()
#                     form.instance.meta_key = field_name
#                     form.instance.meta_value = value
#                     form.instance.created_by = request.user
#                     form.instance.client_id = client_id

#                     form.save()
#                     save = 1
#         end = ''
#         if save == 1:
#             if totalminutes:
#                 print('totalminutes :',totalminutes)
#                 delete = timeslot.objects.all().delete()
#                 for i in range(1,round(totalminutes),5):
#                     if i==1:
#                         start = start_time
#                     else:
#                         start1 = datetime.strptime(end, "%H:%M") + timedelta(minutes=1)
#                         hour = start1.hour
#                         minute = start1.minute
#                         start = str(hour) + ":" + str(minute)


#                     end1 = datetime.strptime(start, "%H:%M") + timedelta(minutes=5)
#                     ehour = end1.hour
#                     eminute = end1.minute
#                     end = str(ehour) + ":" + str(eminute)
#                     sform = Slotform(request.POST)

#                     if sform.is_valid():
#                         sform.instance.slot_time = start + " - " + end
#                         sform.instance.created_by = request.user
#                         sform.instance.client_id = client_id
#                         print(sform.instance.client_id)
#                         sform.save()
#                     else:
#                         print('TEST')
#                     # i = i + 5

#         messages.success(request, "General setting has been updated successfully.")
#         return redirect("/general-settings")
#     return render(request, 'generalsettings/index.html', {'alldata':alldata})
