from django.contrib import admin
from .models import Notification
# # Register your models here.

class CustomIncidentGeneralAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    
admin.site.register(Notification, CustomIncidentGeneralAdmin)
