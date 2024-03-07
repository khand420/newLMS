from django.urls import path
from . import views

urlpatterns = [
    path('locations', views.locations, name = 'locations'),
    path('location/add', views.add_location, name='location_add'),
    path('location/update/<int:id>', views.update_location, name='location_update'),
    path('location/delete/<int:id>', views.delete_location, name='location_delete'),

]
