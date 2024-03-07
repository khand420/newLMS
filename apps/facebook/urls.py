from django.urls import path
from . import views

urlpatterns = [
    path('facebookSubscriptions', views.facebookSubscriptions, name = 'facebookSubscriptions'),
    # path('communication/', views.communication_list, name='communication'),
    path('facebookSubscriptions/add/', views.facebookSubscriptions_add, name='facebookSubscriptions.add'),
    path('facebookSubscriptions/delete/<int:id>/', views.facebookSubscriptions_delete, name='facebookSubscriptions.delete'),
    path('fb/save-subscription/', views.fb_save_subscription, name='fb-save-subscription'),

    # path('fb/subscriptions/', fb_subscriptions, name='leads.fb-subscriptions'),
    # path('fb/add-subscription/', fb_add_subscription, name='leads.fb-add-subscription'),
    # path('fb/delete/<int:id>/', fb_delete_subscription, name='leads.fb-delete-subscription'),

    # path('facebookSubscriptions/edit/<int:id>/', views.facebookSubscriptions_edit, name='facebookSubscriptions.edit'),


    path('facebookProducts', views.facebookProducts, name = 'facebookProducts'),
    path('facebookProducts/add/', views.facebookProducts_add, name='facebookProducts.add'),
    path('facebookProducts/edit/<int:id>/', views.facebookProducts_edit, name='facebookProducts.edit'),

    path('facebookTelecaller', views.facebookTelecallers, name = 'facebookTelecaller'),
    path('facebookTelecaller/add/', views.facebookTelecallers_add, name='facebookTelecaller.add'),
    path('facebookTelecaller/edit/<int:id>/', views.facebookTelecallers_edit, name='facebookTelecaller.edit'),

    path('fb/telecaller-page-form/', views.telecaller_fb_page_form, name='leads.telecaller-page-form'),
    path('fb/multiple-fb-forms/<str:fbpage_id>/<str:fbform_id>/', views.multiple_fb_forms, name='leads.multiple-fb-forms'),


    path('facebookCommunication', views.facebookCommunication, name = 'facebookCommunication'),
    path('facebookCommunication/add/', views.facebookCommunication_add, name='facebookCommunication.add'),
    path('facebookCommunication/edit/<int:id>/', views.facebookCommunication_edit, name='facebookCommunication.edit'),
    

]