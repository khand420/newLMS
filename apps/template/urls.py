from django.urls import path
from . import views

urlpatterns = [
    path('templates', views.templates, name = 'templates'),
    path('template/add/', views.template_add, name='template_add'),
    path('template/update/<int:id>', views.template_update, name='template_update'),
    path('template/delete/<int:id>', views.template_delete, name='template_delete'),

]
