from django.urls import path
from . import views
from .views import ProductView, ProductAddView, ProductUpdateView, DeleteProductView
urlpatterns = [


    #source route
    path('products/', ProductView.as_view(), name='products'),
    path('product/add/', ProductAddView.as_view(), name='product_add'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:id>/', DeleteProductView.as_view(), name='product_delete'),
    # path('products', views.product, name = 'products'),
    # path('product_add/', views.product_add, name='product_add'),
    # path('product_update/<int:pk>/', views.product_update, name='product_update'),
    # path('product_delete/<int:id>/', views.delete_product, name='product_delete'),
    # path('product_delete/<int:pk>/', views.product_delete, name='product_delete'),


]
