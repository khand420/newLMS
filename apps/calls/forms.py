from django import forms
from .models import Timeslots
from django.views.generic import ListView

class Slotform(forms.ModelForm):
    class Meta:
        model = Timeslots
        exclude = ('slot_time','created_at','created_by','updated_at', 'client_id')
