from django import forms
from .models import generalsettings, TellyCommSettings
from django.views.generic import ListView
from apps.leads.models import Sources
from django.forms import formset_factory


from django.contrib.auth.forms import PasswordChangeForm


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        # other customization

#DataFlair
class SettingsCreate(forms.ModelForm):
    start_time = forms.TimeField(required=True)
    end_time = forms.TimeField(required=True)

    class Meta:
        model = generalsettings
        exclude = ('meta_key','meta_value','created_at','updated_at','created_by', 'client_id')




class TellyCommForm(forms.ModelForm):
    # phones = forms.CharField(
    #     max_length=255,
    #     required=False,  # You can set this to True if you want the field to be required
    #     widget=forms.TextInput(attrs={'placeholder': 'Enter multiple phone numbers, separated by commas','class': 'form-control'}),
    # )
    # provider = forms.CharField(
    #     max_length=255,
    #     required=False,  # You can set this to True if you want the field to be required
    #     widget=forms.TextInput(attrs={'placeholder': 'Enter Provider Name','class': 'form-control'}),
    # )
    # auth_token = forms.CharField(
    #     max_length=255,
    #     required=False,  # You can set this to True if you want the field to be required
    #     widget=forms.TextInput(attrs={'placeholder': 'Enter token','class': 'form-control'}),
    # )
    # source_id = forms.ModelChoiceField(
    #     queryset=None,
    #     label='Lead Source',
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     required=False
    # )
    # def __init__(self, *args, client_id=None, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['product_id'].queryset = Product.objects.filter(status = 'active', client=client_id)
        # self.fields['source_id'].queryset = Sources.objects.filter(status = 'active',client_id=client_id)

    class Meta:
        model = TellyCommSettings
        # fields = '__all__'
        exclude = ('created_at','updated_at','created_by', 'client_id')

    def __init__(self, *args, client_id=None, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TellyCommForm, self).__init__(*args, **kwargs)
        self.fields['source_id'].queryset = Sources.objects.filter(client_id=client_id)

        self.fields['phones'].required = False
        # self.fields['source_id'].required = False
        self.fields['auth_token'].required = False
        self.fields['ivr_token'].required = False
        self.fields['company_id'].required = False
        self.fields['secret_token'].required = False
        self.fields['public_ivr_id'].required = False

        self.fields['outgoing_call'].required = False
        self.fields['outgoing_call_name'].required = False
        self.fields['outgoing_call_phone'].required = False

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label



OutgoingCallFormset = formset_factory(
TellyCommForm,
extra=1,  # Set this to the number of initial name and phone pairs you want to display
can_delete=True  # Allow deleting pairs if needed
)
