from django.urls import path
from . import views, ivr, telly_ivr_log_json
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.index, name='index'),          
    path('telecaller-leads', views.telecaller_leads, name = 'telecaller-lead'),
    path('leadlisting', views.leadlisting, name = 'leadlisting'),
    # path('lead_add/', views.lead_add, name='lead_add'),
    path('lead_delete/<int:id>/', views.lead_delete, name='lead_delete'),
    path('lead_update/<int:id>/', views.lead_update, name='lead_update'),
    # path('lead_update/<int:id>/', views.lead_update, name='lead_update'),

    path('leads/edit/<int:id>/', views.lead_edit, name='leads.edit'),
    path('update_lead/', views.update_lead, name='update_lead'),
    path('add_lead/', views.store_lead, name='add_lead'),

    # Route::patch("/leads/update", "LeadsController@update")->name("leads.update");

    path('leads/delete/<int:id>/', views.lead_delete, name='leads.delete'),

    # path('leads', views.LeadsView.as_view(), name='leads'),
    # path('leads/add', views.AddLeadView.as_view(), name='leads.add'),
    # path('leads/edit/<int:id>', views.EditLeadView.as_view(), name='leads.edit'),
    # path('leads/delete/<int:id>', views.DeleteLeadView.as_view(), name='leads.delete'),
    # path('leads/lead-transfer', views.UpdateLeadTransferView.as_view(), name='leads.lead-transfer'),
    # path('leads/lead-assigning', views.UpdateLeadAssigningView.as_view(), name='leads.lead-assigning'),
    # path('leads/import', views.ImportLeadsView.as_view(), name='leads.import'),
    # path('leads/upload-files', views.UploadFilesView.as_view(), name='leads.upload-files'),
    # path('leads/automation-emails', views.AutomationEmailsView.as_view(), name='leads.automation-emails'),
    # path('leads/lead-exports', views.LeadExportsView.as_view(), name='leads.export'),






    path('duplicateleads', views.duplicateleads, name = 'duplicateleads'),
    path('delete_duplicates/', views.delete_duplicates, name='delete_duplicates'),
    # path('duplicateleads/delete/<int:duplicate_id>/', views.delete_duplicate_lead, name='delete_duplicate_lead'),

    path('leadlogs', views.lead_log, name = 'leadlogs'),

    path('parkedleads', views.parkedleads, name= 'parkedleads'),




 
    path('get-questions/', views.get_questions, name='get-questions'),
    path('save-answers/', views.save_answers, name='save_answers'),
    # path('leads/lead-assigning/', views.lead_assigned_user, name='lead-assigning'), update_lead_assigning
    # path('leads/lead-assigning/<int:lead_id>/', views.update_lead_assigning, name='lead-assigning'),


    path('lead-assigning/', views.update_lead_assigning, name='lead-assigning'),
    path('lead-assigned-user/', views.lead_assigned_user, name='lead-assigned-user'), 
    path('lead-transfer/', views.update_lead_transfer, name='lead-transfer'),
    path('lead-transferred-user/', views.lead_transfer_user, name='lead-transferred-user'),

    path('lead-export/', views.lead_export, name='lead-export'),
    path('lead-import/', views.import_lead, name='lead-import'),


    path('upload/', views.upload_files, name='upload_files'),


    # path('findslot/', views.findslot, name='findslot'),
    path('findslot/', views.findslot, name='findslot'),
    path('checkslot/', views.checkslot, name='checkslot'),

    path('my_view/', views.my_view, name='my_view'),

    #LeadTypes route
    path('leadTypes', views.leadTypes, name = 'leadTypes'),
    path('leadType_add/', views.leadType_add, name='leadType_add'),
    path('leadType_update/<int:pk>/', views.leadType_update, name='leadType_update'),
    path('leadType_delete/<int:pk>/', views.leadType_delete, name='leadType_delete'),


    
    #source route
    path('sources', views.sources, name = 'sources'),
    path('source_add/', views.source_add, name='source_add'),
    path('source_update/<int:id>/', views.source_update, name='source_update'),


    path('stages', views.stages, name = 'stages'),
    path('stage_add/', views.stage_add, name='stage_add'),
    path('stage_update/<int:id>', views.stage_update, name='stage_update'),


    path('ivr_receiver/', telly_ivr_log_json.ivr_receiver, name='ivr_receiver'),
    path('ivr_logs/', ivr.ivr_logs, name='ivr_logs'),
    path('ivr_user/', ivr.ivr_user, name='ivr_user'),
    path('ivrinitiate/', ivr.ivrinitiate, name='ivrinitiate'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)