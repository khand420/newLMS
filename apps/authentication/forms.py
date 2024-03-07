from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Industry, Department

class NewUserForm(UserCreationForm):
    username = forms.CharField(
        label='Username*',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        label='Email*',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput (attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput (attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {'email': 'Email'}

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class IndustrySelectionForm(forms.Form):
    industry_id = forms.ModelChoiceField(queryset=Industry.objects.all(), empty_label="Select Industry", widget=forms.Select(attrs={'class': 'form-control select2'}))



class Departmentform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        paginate_by = 2
        model = Department
        exclude = ('created_by','slug')
