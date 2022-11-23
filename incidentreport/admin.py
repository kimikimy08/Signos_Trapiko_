from django.contrib import admin
from .models import  IncidentPerson, AccidentCausation, CollisionType, CrashType,IncidentGeneral, IncidentVehicle,IncidentMedia,IncidentRemark

class CustomIncidentGeneralAdmin(admin.ModelAdmin):
    list_display = ('id','address', 'latitude', 'longitude', 'created_at', 'accident_factor', 'severity')
    # list_display_links = ('user', 'birthdate')
    
    
# Register your models here.
admin.site.register(AccidentCausation)
admin.site.register(CollisionType)
admin.site.register(CrashType)
admin.site.register(IncidentGeneral, CustomIncidentGeneralAdmin)
admin.site.register(IncidentPerson)
admin.site.register(IncidentVehicle)
admin.site.register(IncidentMedia)
admin.site.register(IncidentRemark)

