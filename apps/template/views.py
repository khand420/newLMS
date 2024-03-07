from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect
from .models import Template
from django.contrib import messages
from  apps.authentication.models import UserDetails
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage
from web_project import TemplateLayout


@login_required
def templates(request):
    context = {}

    try:
        udetail = UserDetails.objects.get(user_id=request.user.id)
        page_obj = Template.objects.filter(client_id=udetail.uniqueid).all().order_by('-id')
        paginator = Paginator(page_obj, 5)  # Show 10 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        template_layout = TemplateLayout()

        # Call the init method with the context
        context = template_layout.init(context)

        # Update the context with page_obj
        context.update({'page_obj': page_obj})

        # Render the template using the updated context
        return render(request, 'template/index.html', context)
    except Template.DoesNotExist:
        page_obj = None

    return render(request, 'template/index.html', context)





@login_required
def template_add(request):
    context = {}
    template_layout = TemplateLayout()
    # Call the init method with the context
    context = template_layout.init(context)
    whatsappmedia = None

    if request.method == 'POST':
        udetail = UserDetails.objects.get(user_id=request.user.id)
        name = request.POST.get('name')
        type = request.POST.get('type')
        smstype = template_id = parameters = whatsapptype = subject = ''



        if not type:
            messages.error(request, "Please select a template type.")
            return redirect('templates')

        if type.lower() == "sms":
            smstype = request.POST.get('smstype')
            template_id = request.POST.get('template_id')

        if type.lower() == "whatsapp":
            parameters = request.POST.get('parameters')
            template_id = request.POST.get('template_id')
            whatsapptype = request.POST.get('whatsapptype')
            whatsappmedia = request.FILES.get('whatsappmedia')

        if type.lower() == "email":
            message = request.POST.get('message')
            subject = request.POST.get('subject')
        else:
            message = strip_tags(request.POST.get('message'))

        client_id = udetail.uniqueid
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        try:
            savetemplate = Template(name=name, subject=subject, type=type, message=message, template_id=template_id,
                                    parameters=parameters, created_at=created_at, updated_at=updated_at, smstype=smstype,
                                    whatsapptype=whatsapptype, whatsappmedia=whatsappmedia, client_id=client_id, created_by=request.user.username,
                                    updated_by=request.user.username)
            savetemplate.save()
            messages.success(request, "Template has been added successfully.")
            return redirect('templates')
        except IntegrityError:
            messages.error(request, f"{name} already exists. Please choose a different name.")
            return redirect('templates')

    return render(request, 'template/add.html', context)


@login_required
def template_update(request, id):
    context = {}
    template_layout = TemplateLayout()
    # Call the init method with the context
    context = template_layout.init(context)

    template_obj = get_object_or_404(Template, id=id)

    if request.method == 'POST':
        name = request.POST['name']
        subject = request.POST['subject']
        type = request.POST['type']
        message = request.POST['message']


        # Handle WhatsApp media file
        whatsappmedia = request.FILES.get('whatsappmedia')
        if whatsappmedia:
            # Delete previous media file if exists
            if template_obj.whatsappmedia:
                template_obj.whatsappmedia.delete(save=False)
            # Save the new media file
            fs = FileSystemStorage()
            filename = fs.save(whatsappmedia.name, whatsappmedia)
            template_obj.whatsappmedia = fs.url(filename)


        if not type:
            messages.error(request, "Please select a template type.")
            return redirect('templates')
        try:
            template_obj.name = name
            template_obj.subject = subject
            template_obj.type = type
            template_obj.message = message
            template_obj.save()
            messages.success(request, "Template has been added successfully.")
            return redirect('templates')
        except IntegrityError:
            messages.error(request, f"{name} already exists. Please choose a different name.")
            return redirect('templates')
        # messages.success(request, "Template has been updated successfully.")
        # return redirect('templates')
    context.update({'template': template_obj})
    return render(request, 'template/edit.html', context)



@login_required
def template_delete(request, id):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)
    template_obj = get_object_or_404(Template, id=id)

    if request.method == 'POST':
        template_obj.delete()
        messages.success(request, "Template has been deleted successfully.")
        return redirect('templates')
    context.update({'template': template_obj})
    return render(request, 'template/delete.html', context)
