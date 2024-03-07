

from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from django.contrib.auth.decorators import login_required


from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
# from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import Industry
from .models import UserDetails
from django.shortcuts import render




"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to auth/urls.py file for more pages.
"""




def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request,'Activation link is invalid!')
        return redirect('login')


class AuthView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
            }
        )

        return context


# class SignupView(TemplateView):
#     def get(self, request):
#         industrydata = Industry.objects.all()
#         form = NewUserForm()
#         return render(request, 'auth_register.html', {'register_form': form, 'industrydata': industrydata})

#     def post(self, request):
#         industrydata = Industry.objects.all()
#         form = NewUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()

#             current_site = get_current_site(request)
#             mail_subject = 'Activation link has been sent to your email id'
#             message = render_to_string('master/acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                 mail_subject, message, to=[to_email]
#             )
#             email.send()

#             industry_id = request.POST.get('industry_id', '')
#             industry_instance = get_object_or_404(Industry, id=industry_id)

#             userdata = UserDetails()
#             userdata.user_id = user.id
#             userdata.department = 'client'
#             userdata.industry = industry_instance
#             userdata.save()

#             messages.success(request, "Registration Successfully :) Please Contact with SuperAdmin for Account activation!")
#             return redirect("/login")

#         return render(request, 'auth_login.html', {'register_form': form, 'industrydata': industrydata})


# def login_request(request):
#     template_layout = TemplateLayout()
#     context = template_layout.init({})

#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         print(form, '--------')
#         if form.is_valid():
#             username = form.cleaned_data.get('email-username')
#             password = form.cleaned_data.get('password')
#             print(username, password, '----------')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "You are now logged in.")
#                 return redirect("index")
#             else:
#                 messages.error(request, "Invalid username or password.")
#         else:
#             messages.error(request, "Invalid username or password.")
#     else:
#         form = AuthenticationForm()

#     # Update the context with layout information
#     context.update({
#         "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
#         "login_form": form,
#     })

#     return render(request=request, template_name="auth_login.html", context=context)



# @login_required(login_url="/auth/login/")

def login_request(request):
    template_layout = TemplateLayout()
    context = template_layout.init({})

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("index")

        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    # Update the context with layout information
    context.update({
        "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
        "login_form": form,
    })

    return render(request=request, template_name="auth_login.html", context=context)


class SignupView(TemplateView):
    def get(self, request):
        template_layout = TemplateLayout()
        context = template_layout.init({})
        industrydata = Industry.objects.all()
        form = NewUserForm()
        context.update({'register_form': form, 'industrydata': industrydata})

        # Update the context with layout information
        context.update({
            "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
        })


        return render(request, 'auth_register.html', context)

    # def post(self, request):
    #     template_layout = TemplateLayout()
    #     context = template_layout.init({})
    #     industrydata = Industry.objects.all()
    #     form = NewUserForm(request.POST)
    #     print(form, '-------------')

    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.is_active = False
    #         user.save()

    #         current_site = get_current_site(request)
    #         mail_subject = 'Activation link has been sent to your email id'
    #         message = render_to_string('master/acc_active_email.html', {
    #             'user': user,
    #             'domain': current_site.domain,
    #             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #             'token': account_activation_token.make_token(user),
    #         })
    #         to_email = form.cleaned_data.get('email')
    #         email = EmailMessage(
    #             mail_subject, message, to=[to_email]
    #         )
    #         email.send()

    #         industry_id = request.POST.get('industry_id', '')
    #         industry_instance = get_object_or_404(Industry, id=industry_id)

    #         userdata = UserDetails()
    #         userdata.user_id = user.id
    #         userdata.department = 'client'
    #         userdata.industry = industry_instance
    #         userdata.save()

    #         messages.success(request, "Registration Successfully :) Please Contact with SuperAdmin for Account activation!")
    #         print("DEBUG: Registration Successfully message set!")
    #         # Update the context with layout information
    #         context.update({
    #             "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
    #         })

    #         context.update({'register_form': form, 'industrydata': industrydata})
    #         return redirect("/login")

    #     # Update the context with layout information
    #     context.update({
    #         "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
    #     })

    #     context.update({'register_form': form, 'industrydata': industrydata})
    #     return render(request, 'auth_register.html', context)


    def post(self, request):
        template_layout = TemplateLayout()
        context = template_layout.init({})
        industrydata = Industry.objects.all()
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            industry_id = request.POST.get('industry_id', '')
            industry_instance = get_object_or_404(Industry, id=industry_id)

            userdata = UserDetails()
            userdata.user_id = user.id
            userdata.department = 'client'
            userdata.industry = industry_instance
            userdata.save()

            messages.success(request, "Registration Successfully :) Please Contact with Ichelon Team for Account activation!")
            # print("DEBUG: Registration Successfully message set!")
            # Update the context with layout information
            context.update({
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
                'register_form': form,  # include the form in context for potential error display
                'industrydata': industrydata,
            })
            return redirect("login")

        # Handle form errors and include in context
        form_errors = {
            'non_field_errors': form.non_field_errors(),
            'field_errors': [(field.name, field.errors) for field in form],
        }
        print("DEBUG: Form has errors -", form_errors)

        # Update the context with layout information and form errors
        context.update({
            "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
            'register_form': form,
            'industrydata': industrydata,
            'form_errors': form_errors,
        })
        return render(request, 'auth_register.html', context)
