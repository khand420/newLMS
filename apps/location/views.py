from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect

from django.core.paginator import Paginator
from django.shortcuts import render

from apps.authentication.models import UserDetails
from django.contrib import messages
from web_project import TemplateLayout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Location
from .forms import LocationCreate



def locations(request):
    context = {}
    template_layout = TemplateLayout()
    # Call the init method with the context
    context = template_layout.init(context)
    try:
        udetail = UserDetails.objects.get(user_id=request.user.id)
        shelf = Location.objects.filter(client_id=udetail.uniqueid).all().order_by('-id')
        # shelf = Sources.objects.all().order_by('-id')
        search_text = request.GET.get('searchText', '')
        if search_text:
            shelf = shelf.filter(Q(name__icontains=search_text))

        paginator = Paginator(shelf, 5) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # print(page_obj)
    except Location.DoesNotExist:
        page_obj = None
    context.update({'page_obj': page_obj})
    return render(request, 'location/index.html', context)




@login_required
def add_location(request):
    try:
        context = {}
        template_layout = TemplateLayout()
        context = template_layout.init(context)

        udetail = UserDetails.objects.get(user_id=request.user.id)
        forms = LocationCreate(request = request)

    except Exception as e:
        udetail = None
        print("Error Found", str(e))


    if request.method == 'POST':
        forms = LocationCreate(request.POST, request = request)
        if forms.is_valid():
            location = forms.save(commit=False)
            location.client_id = udetail.uniqueid

            name = forms.cleaned_data['name']
            if Location.objects.filter(name=name).exists():
                messages.error(request, 'Name must be unique.')
            else:
                forms.save()
                messages.success(request, 'Location added successfully.')
                return redirect('locations')
        else:
            errors = forms.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'{field}: {error}')
    context.update({'forms': forms})
    return render(request, 'location/add.html', context)





@login_required
def update_location(request, id):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    location = get_object_or_404(Location, id=id)
    udetail = UserDetails.objects.get(user_id=request.user.id)
    client_id = udetail.uniqueid

    if request.method == 'POST':
        form = LocationCreate(request.POST, instance=location, request=request)
        if form.is_valid():
            location = form.save(commit=False)
            location.client_id = client_id

            name = form.cleaned_data['name']
            if Location.objects.filter(name=name).exclude(id=id).exists():
                messages.error(request, 'Name must be unique.')
            else:
                form.save()
                messages.success(request, 'Location updated successfully.')
                return redirect('locations')
        else:
            errors = form.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = LocationCreate(instance=location, request=request)
    context.update({'forms': form, 'location_id': id})
    return render(request, 'location/edit.html', context)


@login_required
def delete_location(request, id):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)
    location = get_object_or_404(Location, id=id)

    if request.method == 'POST':
        location.delete()
        messages.success(request, 'Location deleted successfully.')
        return redirect('locations')
    context.update({'location': location})
    return render(request, 'location/delete.html', context)
