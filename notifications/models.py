from django.db import models
from ckeditor.fields import RichTextField
from accounts.managers import SoftDeleteManager
from django.utils import timezone
from accounts.models import User
from django.db.models import Max
# Create your models here.

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True

class Notification(models.Model):
    TYPES = ((1, 'Reports'), (2, 'User Accounts'), (3, 'Inbox'), (4, 'Attributes Builder'))
    incident_report = models.ForeignKey('incidentreport.IncidentGeneral', on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey('accounts.User', on_delete=models.CASCADE, blank=True, null=True, related_name="noti_from_user")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_user")
    notification_type = models.IntegerField(choices=TYPES)
    remarks = models.CharField(max_length=90, blank=True)
    text_preview = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
