from django.urls import path
from . import views

urlpatterns = [
    path('lead-reports/type', views.types, name = 'lead_reports_type'),
    path('lead-reports/products', views.products, name = 'lead_reports_products'),
    path('lead-reports/sources', views.sources, name = 'lead_reports_sources'),
    path('lead-reports/stages', views.stages, name = 'lead_reports_stages'),


]