from django.urls import path
from .views import DashboardsView
from . import views

urlpatterns = [
    path(
        "dashboard2", DashboardsView.as_view(template_name="dashboard_analytics.html"),
        name="index",
    ),


    path('dashboard/', views.index, name='dashboard'),

    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('leadstatusgraph/', views.lead_status_graph, name='leadstatusgraph'),
    path('leadsourcegraph/', views.lead_source_graph, name='leadsourcegraph'),
    # path('leadtypegraph/', views.lead_type_graph, name='leadtypegraph'),
    path('weeklyleadgraph/', views.weekly_leads, name='weeklyleadgraph'),
    # path('monthlyleadgraph/', views.monthly_leads, name='monthlyleadgraph'), leadlogfilter
    path('dashboardCount/', views.dashboardCount, name='dashboardCount'),

    path('leadlogfilter/', views.lead_log_filter, name='leadlogfilter'),
    path('prevcallbackfilter/', views.prev_callback_filter, name='prevcallbackfilter'),
    path('callbackfilter/', views.callback_filter, name='callbackfilter'),
    path('updateleadfilter/', views.update_lead_filter, name='updateleadfilter'),


]
