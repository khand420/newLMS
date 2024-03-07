from django import forms
from .models import Stage
from django.views.generic import ListView
from .models import Leads,Sources, LeadType, Stage, Category

from django.contrib.auth.models import User
from apps.authentication.models import UserDetails
from apps.template.models import Template

from apps.product.models import Product
from apps.location.models import Location







class LeadCreate(forms.ModelForm):
    product_id = forms.ModelChoiceField(
        queryset=None,
        label='Product',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    lead_source_id = forms.ModelChoiceField(
        queryset=None,
        label='Lead Source',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    lead_status_id = forms.ModelChoiceField(
        queryset=None,
        label='Lead Stage',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    lead_type_id = forms.ModelChoiceField(
        queryset=None,
        label='Lead Type',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    centre_name = forms.ModelChoiceField(
        queryset=None,
        label='Lead Center',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    def __init__(self, *args, client_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_id'].queryset = Product.objects.filter(status = 'active', client=client_id)
        self.fields['lead_source_id'].queryset = Sources.objects.filter(status = 'active',client_id=client_id)
        # self.fields['lead_status_id'].queryset = Stage.objects.filter(status = 'active',client_id=client_id)
        self.fields['centre_name'].queryset = Location.objects.filter(status = 'active',client_id=client_id)
        self.fields['lead_type_id'].queryset = LeadType.objects.filter(status = 'active',client_id=client_id)


          # Retrieve filtered queryset for lead_status_id
        lead_status_queryset = Stage.objects.filter(status='active', client_id=client_id)
        self.fields['lead_status_id'].queryset = lead_status_queryset

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

                # Set initial value for center_name field
        # if self.instance.center_name:
        #     self.initial['center_name'] = self.instance.center_name.id
        # if self.instance.location:
        #     self.initial['center_name'] = self.instance.location.id

    class Meta:
        model = Leads
        exclude = ('is_potential','star_patient','created_by','primary_lead_source_id', 'company', 'ringing_date', 'ivr_virtual_number', 'fbform_id', 'fbpage_id', 'is_transfer', 'transfer_to', 'other_data', 'lead_data', 'gcampaignid', 'gadgroupid', 'gdata', 'gkeyword', 'gdevice', 'communication_id', 'last_mesage_time', 'client_id',)


class StageCreate(forms.ModelForm):

    # question = forms.CharField(label="Question", widget=forms.TextInput(attrs={'placeholder': 'Enter Question'}), required=False)
    # answers = forms.CharField(label="Answers", widget=forms.TextInput(attrs={'placeholder': 'Enter answer'}), required=False)
    # scores = forms.IntegerField(label="Scores", widget=forms.NumberInput(attrs={'placeholder': 'Enter score', 'class': 'sum_boxes'}), required=False)

    # STATUS_CHOICES = [
    #         (Status.active, 'Active'),
    #         (Status.inactive, 'Inactive'),
    #     ]
    # POTENTIAL_CHOICES = [
    #     (Potencialenum.no, 'No'),
    #     (Potencialenum.yes, 'Yes'),
    # ]
    # STAGE_STATUS_CHOICES = [
    #     (StageStatus.Not_Knows, 'Not Knows'),
    #     (StageStatus.Qualified, 'Qualified'),
    #     (StageStatus.Disqualified, 'Disqualified'),
    # ]

    # status = forms.ChoiceField(
    #     choices=STATUS_CHOICES,
    #     widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    #     label='Status'
    # )
    # is_potential = forms.ChoiceField(
    #     choices=POTENTIAL_CHOICES,
    #     widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    #     label='Is Potential'
    # )
    # stage_status = forms.ChoiceField(
    #     choices=STAGE_STATUS_CHOICES,
    #     widget=forms.Select(attrs={'class': 'form-select'}),
    #     label='Stage Status'
    # )

    # is_main = forms.ChoiceField(
    #     choices=POTENTIAL_CHOICES,
    #     widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    #     label='Is Main'
    # )

    # is_recurring = forms.ChoiceField(
    #     choices=POTENTIAL_CHOICES,
    #     widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    #     label='Is Recurring',
    #     required=False
    # )

    # is_pre_stage = forms.ChoiceField(
    #     choices=POTENTIAL_CHOICES,
    #     widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    #     label='Is Pre Stage',
    #     required=False
    # )

    # is_thankyou_stage = forms.ChoiceField(
    #     choices=POTENTIAL_CHOICES,
    #     widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    #     label='Is Thank You Stage',
    #     required=False
    # )



    # categeory_id = forms.ModelChoiceField(
    #     queryset=category.objects.all(),
    #     label='Category',
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     required=False
    # )

    sms_template_id = forms.ModelChoiceField(
        queryset=None,
        label='SMS Template',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    whatsapp_template_id = forms.ModelChoiceField(
        queryset=None,
        label='WhatsApp Template',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    email_template_id = forms.ModelChoiceField(
        queryset=None,
        label='Email Template',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )



    recurring_sms_template_id = forms.ModelChoiceField(
        queryset=None,
        label='Recurring SMS Template',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    recurring_email_template_id = forms.ModelChoiceField(
        queryset=None,
        label='Recurring Email Template',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    recurring_whatsapp_template_id = forms.ModelChoiceField(
        queryset=None,
        label='Recurring WhatsApp Template',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    pre_sms_template_id = forms.ModelChoiceField(
        queryset=None,
        label='Pre SMS Template',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    pre_email_template_id = forms.ModelChoiceField(
        queryset=None,
        label='Pre Email Template',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    pre_whatsapp_template_id = forms.ModelChoiceField(
        queryset=None,
        label='Pre WhatsApp Template',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    thankyou_sms_template_id = forms.ModelChoiceField(
        queryset=None,
        label='Thank You SMS Template',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    thankyou_email_template_id = forms.ModelChoiceField(
        queryset=None,
        label='Thank You Email Template',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    thankyou_whatsapp_template_id = forms.ModelChoiceField(
        queryset=None,
        label='Thank You WhatsApp Template',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )




    def __init__(self, *args, **kwargs):
        client_id = kwargs.pop('client_id', None)
        super().__init__(*args, **kwargs)
        self.fields['sms_template_id'].queryset = Template.objects.filter(type='sms', client_id=client_id)
        self.fields['whatsapp_template_id'].queryset = Template.objects.filter(type='whatsapp', client_id=client_id)
        self.fields['email_template_id'].queryset = Template.objects.filter(type='email', client_id=client_id)

        self.fields['recurring_sms_template_id'].queryset = Template.objects.filter(type='sms', client_id=client_id)
        self.fields['recurring_whatsapp_template_id'].queryset = Template.objects.filter(type='whatsapp', client_id=client_id)
        self.fields['recurring_email_template_id'].queryset = Template.objects.filter(type='email', client_id=client_id)

        self.fields['pre_sms_template_id'].queryset = Template.objects.filter(type='sms', client_id=client_id)
        self.fields['pre_whatsapp_template_id'].queryset = Template.objects.filter(type='whatsapp', client_id=client_id)
        self.fields['pre_email_template_id'].queryset = Template.objects.filter(type='email', client_id=client_id)

        self.fields['thankyou_sms_template_id'].queryset = Template.objects.filter(type='sms', client_id=client_id)
        self.fields['thankyou_whatsapp_template_id'].queryset = Template.objects.filter(type='whatsapp', client_id=client_id)
        self.fields['thankyou_email_template_id'].queryset = Template.objects.filter(type='email', client_id=client_id)

        for field_name in self.fields:
            field = self.fields[field_name]
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    # def clean(self):
    #     cleaned_data = super().clean()

    #     # Get the parent stage ID
    #     parent_id = self.data.get('parent_id')

    #     # Get the answers and scores
    #     answers = self.data.getlist('answers')
    #     scores = self.data.getlist('scores')

    #     # Create a list to store the answers and scores
    #     answers_scores = []

    #     # Iterate over the answers and scores to create a list of tuples
    #     for answer, score in zip(answers, scores):
    #         if answer and score:
    #             answers_scores.append((answer, score))
    #     print(answers_scores)

    #     # Set the parent_id, answers, and scores in the cleaned_data
    #     cleaned_data['parent_id'] = parent_id
    #     cleaned_data['answers_scores'] = answers_scores

    #     return cleaned_data

    # class Meta:
    #     model = Stage
    #     fields = '__all__'
    #     exclude = ('updated_at', 'created_at', 'client_id', 'slug', 'categeory_id', 'is_potential', 'primary_slug')

    def clean(self):
        cleaned_data = super().clean()

        # Set empty fields to None
        for field_name in self.fields:
            if field_name in cleaned_data and not cleaned_data[field_name]:
                cleaned_data[field_name] = None

        return cleaned_data

    class Meta:
        model = Stage
        fields = '__all__'
        exclude = ('updated_at', 'created_at', 'client_id', 'slug', 'categeory_id', 'is_potential', 'primary_slug')






class LeadTypeCreate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LeadTypeCreate, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
    class Meta:
        model = LeadType
        fields = '__all__'
        exclude = ('updated_at', 'created_at', 'client_id','Date')






class SourceCreate(forms.ModelForm):
    # assign_user = forms.ModelChoiceField(queryset=User.objects.none(),  widget=forms.SelectMultiple)
    assign_user = forms.ModelMultipleChoiceField(queryset=User.objects.none(),widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'})),
    # assign_user = forms.ModelMultipleChoiceField(
    #     queryset=User.objects.none(),
    #     widget=EasySelectMultipleWidget(),
    # )

    class Meta:
        model = Sources
        fields = '__all__'
        exclude = ('updated_at', 'created_at', 'client_id', 'token')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Store the request object
        super().__init__(*args, **kwargs)
        self.fields['assign_user'].queryset = self.get_assign_user_queryset()

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label


    def get_assign_user_queryset(self):
        udetail = UserDetails.objects.get(user_id=self.request.user.id)
        clientid = udetail.uniqueid
        telecallers = UserDetails.objects.filter(uniqueid=clientid, department='telecaller').values_list('user_id', flat=True)
        # return User.objects.filter(id__in=telecallers)
        return User.objects.filter(id__in=telecallers)
