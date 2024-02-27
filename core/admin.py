from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import PropertyResource  # Assuming you have defined PropertyResource in a separate file

class PropertyAdmin(ImportExportModelAdmin):
    resource_class = PropertyResource
    # Customize further if needed

admin.site.register(Property, PropertyAdmin)
# admin.site.register(Property)
admin.site.register(Contact)
admin.site.register(BookProperty)
admin.site.register(Phone)