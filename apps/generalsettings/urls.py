from django.urls import path
# from django.conf.urls import url
from django.urls import re_path as url
from . import views

urlpatterns = [
    path('general-settings', views.Genearalsettings, name = 'general-settings'),
    path('update_general_settings', views.update_general_settings, name = 'update_general_settings'),

    path('tellycommunication_list', views.communications_list, name = 'communication_list'),
    path('add_tellycommunication/', views.add_commu, name='add_communication'),
    path('update_tellycommunication/<int:pk>/', views.update_communication, name='update_communication'),
    path('delete_tellycommunication/<int:pk>/', views.delete_communication, name='delete_communication'),
    # path('update_telly_Communication_settings', views.update_telly_Communication, name = 'update_telly_Communication_settings'),
    # path('tellycommunication_list', views.update_telly_Communication, name = 'communication_list'),



    url(r'^password/$', views.change_password, name='change_password'),
    # path('checkslot/', views.checkslot, name='checkslot'),
    # path('findslot/', views.findslot, name='findslot'),

]

