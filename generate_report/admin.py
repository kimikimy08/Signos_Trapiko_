from django.contrib import admin
from .models import GenerateReport, UploadFile
# Register your models here.
admin.site.register(GenerateReport)
admin.site.register(UploadFile)