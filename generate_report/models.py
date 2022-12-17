import os
from django.db import models
from accounts.models import User
from .utils import generate_code
from uuid import uuid4
# Create your models here.

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(uuid4().hex, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper

incident_image_upload_path = path_and_rename('uploadfile/')
incident_image_upload_path.__qualname__ = 'incident_image_upload_path'
class GenerateReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fromdate = models.DateField(blank=True, null=True)
    todate = models.DateField(blank=True, null=True)
    report = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.report

class UploadFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    upload_id = models.CharField(max_length=12, blank=True)
    csv_file = models.FileField(upload_to=incident_image_upload_path, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.upload_id
    
    # def save(self, *args, **kwargs):
    #     if self.upload_id == "":
    #         self.upload_id = generate_code()
    #     return super().save(*args, **kwargs)
    
