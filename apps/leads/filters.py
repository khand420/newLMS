from django.contrib import admin
from django.db import models
from .models import Sources
from django.contrib.admin import SimpleListFilter

class SourceFilter(SimpleListFilter):
    title = "Select Source"  # a label for our filter
    parameter_name = "lead_source_id"  # you can put anything here

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have two:
        allmat = Sources.objects.all()
        return [(c.id, c.name) for c in allmat]

    def queryset(self, request, queryset):
       
        if self.value():
            return queryset.filter(lead_source_id=self.value())
        