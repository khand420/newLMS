

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404

from .forms import CommunicationCreate
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Communication
from django.contrib.admin.sites import site
from userdetail.models import userdetail
from django.contrib import messages
import datetime
from django.db.models import Q

   


def communication(request):
    try:
        udetail = userdetail.objects.get(user_id=request.user.id)
        client_idid = udetail.uniqueid
        leads = Communication.objects.filter(client_id=udetail.uniqueid).all().order_by('-id')
       

        search_text = request.GET.get('searchText', '')
        if search_text:
            leads = leads.filter(Q(title__icontains=search_text) | Q(email__icontains=search_text))

        paginator = Paginator(leads, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except Communication.DoesNotExist:
        page_obj = None

    return render(request, 'communication/index.html', {'page_obj': page_obj})



 
def communication_add(request):
    if request.user.is_authenticated:
        udetail = userdetail.objects.get(user_id=request.user.id)
        print(udetail)
        upload = CommunicationCreate(initial={'client_id': udetail})
        
        if request.method == 'POST':
            upload = CommunicationCreate(request.POST, request.FILES)
            
            if upload.is_valid():            
                communication = upload.save(commit=False)
                communication.client_id = udetail.uniqueid  

                # Check if a communication with the same title already exists for the user
                if Communication.objects.filter(title=communication.title, client_id=communication.client_id).exists():
                    messages.error(request, 'communication with this title already exists.')
                    return redirect('communication_add')
                else:
                    communication.save()
                    messages.success(request, 'communication added successfully.')
                    return redirect('communications')
            else:
                print(upload.errors)
                return HttpResponse('Your form is incorrect. Please go back and try again.')
        
        return render(request, 'communication/add.html', {'leadform': upload})
    else:
        return HttpResponse('Please log in to access this page.')



# def communication_update(request, pk):
#     if request.user.is_authenticated:
#         udetail = userdetail.objects.get(user_id=request.user.id)
#         communication = get_object_or_404(communication, pk = pk)

#         if request.method == 'POST':
#             upload = CommunicationCreate(request.POST, request.FILES, instance=communication)
#             if upload.is_valid():
#                 updated_communication = upload.save(commit=False)

#                 # Check if a communication with the same title already exists for the user
#                 if Communication.objects.exclude(id=pk).filter(title=updated_communication.title, client_id=communication.client_id).exists():
#                     messages.error(request, 'communication with this title already exists.')
#                     return redirect('communication_update', pk=pk)
#                 else:
#                     updated_communication.save()
#                     messages.success(request, 'communication updated successfully.')
#                     return redirect('communications')
#             else:
#                 print(upload.errors)
#                 return HttpResponse('Your form is incorrect. Please go back and try again.')
#         else:
#             upload = CommunicationCreate(instance=communication)
        
#         return render(request, 'communication/edit.html', {'leadform': upload})
#     else:
#         return HttpResponse('Please log in to access this page.')


def communication_update(request, pk):
    try:
        if request.user.is_authenticated:
            udetail = userdetail.objects.get(user_id=request.user.id)
            communication_obj = get_object_or_404(Communication, pk=pk)

            if request.method == 'POST':
                upload = CommunicationCreate(request.POST, request.FILES, instance=communication_obj)
                if upload.is_valid():
                    updated_communication = upload.save(commit=False)

                    # Check if a communication with the same title already exists for the user
                    if Communication.objects.exclude(id=pk).filter(title=updated_communication.title, client_id=communication_obj.client_id).exists():
                        messages.error(request, 'A communication with this title already exists.')
                        return redirect('communication_update', pk=pk)
                    else:
                        updated_communication.save()
                        messages.success(request, 'Communication updated successfully.')
                        return redirect('communications')
                else:
                    # print(upload.errors)
                    return HttpResponse('Your form is incorrect. Please go back and try again.')
            else:
                upload = CommunicationCreate(instance=communication_obj)

            return render(request, 'communication/edit.html', {'leadform': upload})
        else:
            return HttpResponse('Please log in to access this page.')
    except Communication.DoesNotExist:
        return HttpResponse('Communication not found.')


# def communication_delete(request, id):
#     communication = get_object_or_404(communication, id=id)

#     if request.method == 'POST':
#         communication.delete()
#         return redirect('communications')

#     return render(request, 'communication/delete.html', {'communication': communication})



def communication_delete(request, pk):
    try:
        if request.user.is_authenticated:
            udetail = userdetail.objects.get(user_id=request.user.id)
            communication = get_object_or_404(Communication, pk=pk)

            if request.method == 'POST':
                # Delete the communication object
                communication.delete()
                messages.success(request, 'Communication deleted successfully.')
                return redirect('communications')

            return render(request, 'communication/delete.html', {'communication': communication})
        else:
            return HttpResponse('Please log in to access this page.')
    except Communication.DoesNotExist:
        return HttpResponse('Communication not found.')