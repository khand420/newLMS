from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect
from .models import Department, UserDetails, Industry
from .forms import Departmentform
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import site
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from web_project import TemplateLayout


def clients(request):
    # shelf = User.objects.select_related('userdetail.userdetail.user_id').all()
    page_obj = UserDetails.objects.select_related('user','industry').all()
    # print(page_obj)


    return render(request, 'clients/index.html', {'page_obj': page_obj})

def client_add(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        email = request.POST['email']
        password = make_password(request.POST['password'])
        Saveuser = User(username=username, first_name=first_name, email=email, password=password)
        Saveuser.save()


        industryid = request.POST['industry_id']
        department_id = request.POST['department_id']
        phone = request.POST['phone']
        userid = Saveuser.id
        detail = UserDetails(industry_id=industryid, department=department_id, phone=phone, user_id=userid)
        detail.save()
        messages.success(request, "Client has been added successfully.")
        return redirect('clients')
    else:
        industrydata = Industry.objects.all()
        departmentdata = Department.objects.all()

        context = {
            'industrydata': industrydata,
            'departmentdata': departmentdata

        }
        return render(request, 'clients/add.html', context)

def client_update(request, id):
    upload ={}
    if request.method == 'POST':
        Saveuser = User.objects.get(id=id)
        Saveuser.first_name = request.POST['first_name']
        Saveuser.email = request.POST['email']
        Saveuser.password = make_password(request.POST['password'])
        Saveuser.username = request.POST['username']
        Saveuser.save()


        # industryid = request.POST['industry_id']
        # department_id = request.POST['department_id']
        # phone = request.POST['phone']
        # userid = Saveuser.id
        # detail = userdetail.userdetail(industry_id=industryid, department=department_id, phone=phone, user_id=userid)
        # detail.save()
        messages.success(request, "Client has been edited successfully.")
        return redirect('clients')
    else:
        userform = get_object_or_404(User, id = id)
        detail = UserDetails.objects.get(user_id=id)

        industrydata = Industry.objects.all()
        departmentdata = Department.objects.all()

        context = {
            'industrydata': industrydata,
            'departmentdata': departmentdata,
            'userform':userform,
            'detail':detail

        }
        return render(request, 'clients/edit.html', context)




# def telecaller_list(request):
#     # # Get the userdetail object based on the login unique ID
#     # user_detail = get_object_or_404(userdetail, uniqueid=request.user.id)

#     # # Retrieve the telecallers associated with the userdetail
#     # telecallers = user_detail

#     # context = {
#     #     'telecallers': telecallers,
#     # }

#     try:
#         client = userdetail.objects.get(id=request.user.id)  # Replace with the appropriate client ID
#         telecallers = client.telecaller_set.all()
#     except userdetail.DoesNotExist:
#         telecallers = []
#     print(telecallers, client)

#     context = {
#         'client': client,
#         'telecallers': telecallers
#     }

#     return render(request, 'telecaller/telecaller_list.html', context)

def telecaller_list(request):
    context = {}
    template_layout = TemplateLayout()
    # Call the init method with the context
    context = template_layout.init(context)
    try:
        udetail = UserDetails.objects.get(user_id=request.user.id)
        clientid= udetail.uniqueid
        telecallers = UserDetails.objects.select_related('user').filter(uniqueid=clientid,department='telecaller').all()
    except UserDetails.DoesNotExist:
        telecallers = None


    # print(telecallers.all())
    # context = {
    #     # 'client': client,
    #     'telecallers': telecallers
    # }
    context.update({'telecallers': telecallers})
    return render(request, 'telecaller/index.html', context)




# def set_plaintext_password(plaintext_password):
#     user_id = 61
#     plaintext_password = "your_plaintext_password"

#     # Fetch the user object
#     user = User.objects.get(id=user_id)

#     # Set the plaintext password without hashing
#     user.set_unusable_password()
#     user.set_password(plaintext_password)
#     user.save()

# set_plaintext_password()



def telecaller_add(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)
    if request.method == 'POST':
        # Get the form data
        username = request.POST['username']
        first_name = request.POST['first_name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        department_name = 'telecaller'

        # try:
        #     # Get the department object
        #     department_obj = department.objects.get(name=department_name)
        # except department.DoesNotExist:
        #     # Handle the case when the department does not exist
        #     messages.error(request, "Department 'telecaller' does not exist.")
        #     return redirect('telecallers')

        # Create the User object

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('clients-user')
        # user = User.objects.create_user(username=username, first_name=first_name, email=email, password=password)

        user = User(username=username, first_name=first_name, email=email)
        # user.set_unusable_password()
        # user.save()
        # # Now, set the actual password (plaintext) without hashing
        # user.set_password(password)
        # user.save()

        user.set_unusable_password()
        user.password = password
        user.save()

        udetail = UserDetails.objects.get(user_id=request.user.id)

        client_id = udetail.uniqueid
        user_detail = UserDetails(user=user, phone=phone, department=department_name,uniqueid=client_id)
        user_detail.save()



        messages.success(request, "User has been added successfully.")
        return redirect('clients-user')
    else:
        # Fetch departments for dropdown
        departments = Department.objects.all()

        # context = {
        #     'departments': departments
        # }
        context.update({'departments': departments})
        return render(request, 'telecaller/add.html', context)




# def telecaller_add(request):
#     if request.method == 'POST':
#         # Get the form data
#         username = request.POST['username']
#         first_name = request.POST['first_name']
#         email = request.POST['email']
#         password = request.POST['password']
#         phone = request.POST['phone']
#         department_name = 'telecaller'

#         # try:
#         #     # Get the department object
#         #     department_obj = department.objects.get(name=department_name)
#         # except department.DoesNotExist:
#         #     # Handle the case when the department does not exist
#         #     messages.error(request, "Department 'telecaller' does not exist.")
#         #     return redirect('telecallers')

#         # Create the User object
#         user = User.objects.create_user(username=username, first_name=first_name, email=email, password=password)
#         # print(user)
#         # Create the UserDetail object
#         # udetail = userdetail.userdetail.objects.get(user_id=request.user.id)
#         udetail = userdetail.userdetail.objects.get(user_id=request.user.id)
#         # print(udetail)
#         # clientid= udetail.uniqueid
#         client_id = udetail.uniqueid
#         user_detail = userdetail.userdetail(user=user, phone=phone, department=department_name,uniqueid=client_id)
#         user_detail.save()



#         messages.success(request, "Telecaller has been added successfully.")
#         return redirect('telecallers')
#     else:
#         # Fetch departments for dropdown
#         departments = department.objects.all()

#         context = {
#             'departments': departments
#         }
#         return render(request, 'telecaller/add.html', context)



def telecaller_update(request, id):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)
    print(request.user)
    if request.method == 'POST':
        save_user = User.objects.get(id=id)
        save_user.first_name = request.POST['first_name']
        save_user.email = request.POST['email']
        save_user.password = request.POST['password'] #make_password(request.POST['password'])
        save_user.username = request.POST['username']
        # if User.objects.filter(username=save_user.username).exists():
        #     messages.error(request, "Username already exists. Please choose a different username.")
        #     return redirect('telecallers')
        save_user.save()


        save_telecaller = UserDetails.objects.get(user_id=id)
        save_telecaller.phone = request.POST['phone']
        save_telecaller.save()


        messages.success(request, "User has been edited successfully.")
        return redirect('clients-user')
    else:
        user_form = get_object_or_404(User, id=id)
        telecaller = UserDetails.objects.get(user_id=id)
        print(user_form, telecaller)


        # context = {
        #     'user_form': user_form,
        #     'telecaller': telecaller,
        # }
        context.update({'user_form': user_form,'telecaller': telecaller})
        return render(request, 'telecaller/edit.html', context)


def telecaller_delete(request, id):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    telecaller = get_object_or_404(User, id=id)
    messages.success(request, "Telecaller has been deleted successfully.", context)
    telecaller.delete()
    return redirect('telecallers')




def departments(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    shelf = Department.objects.all()
    paginator = Paginator(shelf, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context.update({'page_obj': page_obj})
    return render(request, 'department/index.html', context)

def department_add(request):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    upload = Departmentform()
    if request.method == 'POST':
        upload = Departmentform(request.POST, request.FILES)
        if upload.is_valid():
            upload.instance.created_by = request.user
            upload.instance.slug = slugify(upload.cleaned_data.get('name'))
            upload.save()
            messages.success(request, "Department has been added successfully.")
            return redirect('departments')
        else:
            messages.error(request, "Unable to add Department. Please try again later.")
            return redirect('department_add')
    else:
        context.update({'leadform':upload})
        return render(request, 'department/add.html', context)

def department_update(request, id):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    obj = get_object_or_404(Department, id = id)
    form = Departmentform(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Department has been updated successfully")
        return redirect('departments')
    context.update({'leadform':form})
    return render(request, 'department/edit.html', context)

def department_delete(request,id):
    context = {}
    template_layout = TemplateLayout()
    context = template_layout.init(context)

    dept = Department.objects.get(id=id)
    dept.delete()
    messages.success(request, "Department has been deleted successfully", context)
    return redirect("departments")
