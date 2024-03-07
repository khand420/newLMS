from .models import Product
# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

from .forms import ProductCreate
from django.http import HttpResponse
from django.core.paginator import Paginator

# from django.contrib.admin.sites import site
from apps.authentication.models import UserDetails
from django.contrib import messages
from django.views.generic import TemplateView
from django.views import View  
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# import datetime



# def product(request):
#     shelf = Product.objects.all()
#     paginator = Paginator(shelf, 10) # Show 25 contacts per page.

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'product/index.html', {'page_obj': page_obj})


# def product(request):
#     # context = {}  # Initialize an empty context
#     # template_layout = TemplateLayout()
#     # context = template_layout.init({})
#     context = TemplateLayout.init(self, super().get_context_data())
#     if request.user.is_authenticated:
#         try:
#             udetail = UserDetails.objects.get(user_id=request.user.id)
#             shelf = Product.objects.filter(client=udetail.uniqueid).order_by('-id')  # Filter products by client_id
#             paginator = Paginator(shelf, 2)  # Show 2 products per page

#             page_number = request.GET.get('page')
#             page_obj = paginator.get_page(page_number)

#             # Initialize TemplateLayout and update the context
#             # context.update(TemplateLayout.init(context))

#             # Update the context with page_obj
#             context.update({'page_obj': page_obj})

#             # Render the template using the updated context
#             return render(request, context['layout_path'], context)
#         except UserDetails.DoesNotExist:
#             udetail = None
#     else:
#         return HttpResponse('Please log in to access this page.')


# class ProductView(TemplateView):
#     template_name = 'product/index.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         if self.request.user.is_authenticated:
#             try:
#                 udetail = UserDetails.objects.get(user_id=self.request.user.id)
#                 shelf = Product.objects.filter(client=udetail.uniqueid).order_by('-id')
#                 paginator = Paginator(shelf, 2)

#                 page_number = self.request.GET.get('page')
#                 page_obj = paginator.get_page(page_number)

#                 # Initialize TemplateLayout and update the context
#                 context.update(TemplateLayout.init(context))

#                 # Update the context with page_obj
#                 context.update({'page_obj': page_obj})
#             except UserDetails.DoesNotExist:
#                 udetail = None
#         else:
#             return HttpResponse('Please log in to access this page.')

#         return context



class ProductView(TemplateView):
    template_name = 'product/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            try:
                udetail = UserDetails.objects.get(user_id=self.request.user.id)
                shelf = Product.objects.filter(client=udetail.uniqueid).order_by('-id')
                paginator = Paginator(shelf, 5)

                page_number = self.request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                # Create an instance of TemplateLayout
                template_layout = TemplateLayout()

                # Call the init method with the context
                context = template_layout.init(context)

                # Update the context with page_obj
                context.update({'page_obj': page_obj})
            except UserDetails.DoesNotExist:
                udetail = None
        else:
            return HttpResponse('Please log in to access this page.')

        return context



@method_decorator(login_required, name='dispatch')
class ProductAddView(View):
    template_name = 'product/add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        # Create an instance of TemplateLayout
        template_layout = TemplateLayout()
        # Call the init method with an empty context
        context = template_layout.init({})

        udetail = UserDetails.objects.get(user_id=request.user.id)
        upload = ProductCreate(initial={'client': udetail})

        context['leadform'] = upload

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        udetail = UserDetails.objects.get(user_id=request.user.id)
        upload = ProductCreate(request.POST, request.FILES)

        if upload.is_valid():
            product = upload.save(commit=False)
            product.client = udetail.uniqueid

            if Product.objects.filter(name=product.name, client=product.client).exists():
                messages.error(request, 'Product with this name already exists.')
                return redirect('product_add')
            else:
                product.save()
                messages.success(request, 'Product added successfully.')
                return redirect('products')
        else:
            print(upload.errors)
            return HttpResponse('Your form is incorrect. Please go back and try again.')




@method_decorator(login_required, name='dispatch')
class ProductUpdateView(View):
    template_name = 'product/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, pk, *args, **kwargs):
        # Create an instance of TemplateLayout
        template_layout = TemplateLayout()
        # Call the init method with an empty context
        context = template_layout.init({})

        udetail = UserDetails.objects.get(user_id=request.user.id)
        product = get_object_or_404(Product, pk=pk)
        upload = ProductCreate(instance=product)

        context['leadform'] = upload

        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        udetail = UserDetails.objects.get(user_id=request.user.id)
        product = get_object_or_404(Product, pk=pk)
        upload = ProductCreate(request.POST, request.FILES, instance=product)

        if upload.is_valid():
            updated_product = upload.save(commit=False)

            if Product.objects.exclude(id=pk).filter(name=updated_product.name, client=product.client).exists():
                messages.error(request, 'Product with this name already exists.')
                return redirect('product_update', pk=pk)
            else:
                updated_product.save()
                messages.success(request, 'Product updated successfully.')
                return redirect('products')
        else:
            print(upload.errors)
            return HttpResponse('Your form is incorrect. Please go back and try again.')


# @method_decorator(login_required, name='dispatch')
# class ProductAddView(View):
#     template_name = 'product/add.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)


#     def get(self, request):
#         # udetail = request.user.userdetail
#         udetail = UserDetails.objects.get(user_id=request.user.id)
#         upload = ProductCreate(initial={'client': udetail})
#          # Create an instance of TemplateLayout
#         template_layout = TemplateLayout()
#         # Call the init method with the context
#         context = template_layout.init(context)
#         return render(request, self.template_name, {'leadform': upload})

#     def post(self, request):
#         udetail = UserDetails.objects.get(user_id=request.user.id)
#         upload = ProductCreate(request.POST, request.FILES)

#         if upload.is_valid():
#             product = upload.save(commit=False)
#             product.client = udetail.uniqueid

#             if Product.objects.filter(name=product.name, client=product.client).exists():
#                 messages.error(request, 'Product with this name already exists.')
#                 return redirect('product_add')
#             else:
#                 product.save()
#                 messages.success(request, 'Product added successfully.')
#                 return redirect('products')
#         else:
#             print(upload.errors)
#             return HttpResponse('Your form is incorrect. Please go back and try again.')


# @method_decorator(login_required, name='dispatch')
# class ProductUpdateView(View):
#     template_name = 'product/edit.html'

#     def get(self, request, pk):
#         udetail = request.user.userdetail
#         product = get_object_or_404(Product, pk=pk)
#         upload = ProductCreate(instance=product)
#         return render(request, self.template_name, {'leadform': upload})

#     def post(self, request, pk):
#         udetail = request.user.userdetail
#         product = get_object_or_404(Product, pk=pk)
#         upload = ProductCreate(request.POST, request.FILES, instance=product)

#         if upload.is_valid():
#             updated_product = upload.save(commit=False)

#             if Product.objects.exclude(id=pk).filter(name=updated_product.name, client=product.client).exists():
#                 messages.error(request, 'Product with this name already exists.')
#                 return redirect('product_update', pk=pk)
#             else:
#                 updated_product.save()
#                 messages.success(request, 'Product updated successfully.')
#                 return redirect('products')
#         else:
#             print(upload.errors)
#             return HttpResponse('Your form is incorrect. Please go back and try again.')


@method_decorator(login_required, name='dispatch')
class DeleteProductView(View):
    template_name = 'product/delete.html'

    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        return render(request, self.template_name, {'product': product})

    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return redirect('products')



# def product_add(request):
#     if request.user.is_authenticated:
#         udetail = UserDetails.objects.get(user_id=request.user.id)
#         print(udetail)
#         upload = ProductCreate(initial={'client': udetail})

#         if request.method == 'POST':
#             upload = ProductCreate(request.POST, request.FILES)

#             if upload.is_valid():
#                 product = upload.save(commit=False)
#                 product.client = udetail.uniqueid  # Set the client_id to the user's client_id

#                 # Check if a product with the same name already exists for the user
#                 if Product.objects.filter(name=product.name, client=product.client).exists():
#                     messages.error(request, 'Product with this name already exists.')
#                     return redirect('product_add')
#                 else:
#                     product.save()
#                     messages.success(request, 'Product added successfully.')
#                     return redirect('products')
#             else:
#                 print(upload.errors)
#                 return HttpResponse('Your form is incorrect. Please go back and try again.')

#         return render(request, 'product/add.html', {'leadform': upload})
#     else:
#         return HttpResponse('Please log in to access this page.')


# def product_update(request, pk):
#     if request.user.is_authenticated:
#         udetail = UserDetails.objects.get(user_id=request.user.id)
#         product = get_object_or_404(Product, pk = pk)

#         if request.method == 'POST':
#             upload = ProductCreate(request.POST, request.FILES, instance=product)
#             if upload.is_valid():
#                 updated_product = upload.save(commit=False)

#                 # Check if a product with the same name already exists for the user
#                 if Product.objects.exclude(id=pk).filter(name=updated_product.name, client=product.client).exists():
#                     messages.error(request, 'Product with this name already exists.')
#                     return redirect('product_update', pk=pk)
#                 else:
#                     updated_product.save()
#                     messages.success(request, 'Product updated successfully.')
#                     return redirect('products')
#             else:
#                 print(upload.errors)
#                 return HttpResponse('Your form is incorrect. Please go back and try again.')
#         else:
#             upload = ProductCreate(instance=product)

#         return render(request, 'product/edit.html', {'leadform': upload})
#     else:
#         return HttpResponse('Please log in to access this page.')



# def delete_product(request, id):
#     product = get_object_or_404(Product, id=id)

#     if request.method == 'POST':
#         product.delete()
#         return redirect('products')

#     return render(request, 'product/delete.html', {'product': product})



# def product_update(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         form = ProductCreate(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('products')
#         else:
#             print(form.errors)
#             return HttpResponse('Your form is incorrect. Please go back and try again.')
#     else:
#         form = ProductCreate(instance=product)
#         return render(request, 'product/edit.html', {'leadform': form, 'product': product})

# def product_delete(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         product.delete()
#         return redirect('products')
#     else:
#         return render(request, 'product/index.html',  {'product': product})
