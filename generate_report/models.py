from django.db import models
from accounts.models import User
# Create your models here.
class GenerateReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fromdate = models.DateField(blank=True, null=True)
    todate = models.DateField(blank=True, null=True)
    report = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.report