from django.contrib import admin
from .models import Job, Application
import csv
from django.db.models import ForeignKey
from django.http import HttpResponse

# reusable method for building a csv for given objects but computing model fields at runtime instead of hardcoding
def export_as_csv(modeladmin, request, queryset):
    fields = queryset.model._meta.fields # row fields

    # get fields with foreign keys to do a join operation to avoid separate db calls
    foreignkeys = [f.name for f in fields if isinstance(f, ForeignKey)]
    if foreignkeys:
        queryset = queryset.select_related(*foreignkeys) # unpacks foreign keys list into string arguments

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{queryset.model._meta.model_name}.csv"'

    writer = csv.writer(response)
    writer.writerow([f.name for f in fields]) # set fields as the header row in csv
    
    # append each object as a row in csv
    for x in queryset:
        writer.writerow(getattr(x, f.name) for f in fields) # get attr to get x's 'f.name' field
    
    return response

export_as_csv.short_description = "Export selected as CSV"

# register Application and Job in sites and then add the export_csv action
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    actions = [export_as_csv]

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    actions = [export_as_csv]