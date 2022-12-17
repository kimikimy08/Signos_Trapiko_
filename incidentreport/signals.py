from .models import IncidentOTP, IncidentGeneral
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=IncidentGeneral)
def post_save_generate_code(sender, instance, created, *args, **kwargs):
    if created:
        IncidentOTP.objects.create(incident_general=instance)