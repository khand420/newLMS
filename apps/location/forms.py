from django import forms
from .models import Location

class LocationCreate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LocationCreate, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
    class Meta:
        model = Location
        fields = '__all__'
        exclude = ('updated_at', 'created_at', 'client_id', 'created_by')

