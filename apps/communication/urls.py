from django.urls import path
from . import views


urlpatterns = [


    #source route
    path('communications', views.communication, name = 'communications'),
    path('communication_add/', views.communication_add, name='communication_add'),
    path('communication_update/<int:pk>/', views.communication_update, name='communication_update'),
    path('communication_delete/<int:pk>/', views.communication_delete, name='communication_delete'),
    # path('product_delete/<int:pk>/', views.product_delete, name='product_delete'),


]

