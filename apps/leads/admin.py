from django.contrib import admin
from .models import Leads
from .models import Sources
from .models import Stage
from .filters import SourceFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter


# Register your models here.
#admin.site.register(Leads)
@admin.register(Leads)

class LeadsIndex(admin.ModelAdmin):
    # fields = (('salutation', 'name'), ('phone', 'email'))
    # fieldsets = (
    #     (None, {
    #         'fields': (('salutation', 'name'), 'phone', 'email'),
    #     }),
    #     ('Advanced options', {
    #         'fields': ('city', ('lead_status_id', 'lead_source_id'))
    #     }),
    # )
    exclude = ('company','ringing_date','ivr_virtual_number','fbform_id','fbpage_id','is_transfer','transfer_to','other_data','lead_data','gcampaignid','gadgroupid','gdata','gkeyword','gdevice','communication_id','last_mesage_time')
    list_display = ('name','email','phone','lead_source_id','lead_status_id')
    list_filter = (
        # for ordinary fields
        ('lead_source_id', RelatedDropdownFilter),
        ('salutation', DropdownFilter),
    )
@admin.register(Sources)
class Sourceadmin(admin.ModelAdmin):
    exclude = ('token',)
    list_display = ('name','token','status')
    search_fields = ["url"]

@admin.register(Stage)
class Stageadmin(admin.ModelAdmin):
    exclude = ('slug','primary_slug','created_by','updated_by')
    list_display = ('name','slug','is_potential','categeory_id','status')
    list_filter = (
        # for ordinary fields
        ('categeory_id', RelatedDropdownFilter),
        ('is_potential', DropdownFilter),
    )


