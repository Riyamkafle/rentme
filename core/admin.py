from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Property)
admin.site.register(Contact)
admin.site.register(BookProperty)
admin.site.register(Phone)