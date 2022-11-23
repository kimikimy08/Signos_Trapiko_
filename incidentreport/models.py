import os
import uuid
from django.db import models
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.core.validators import FileExtensionValidator
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, fromstr
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from accounts.managers import SoftDeleteManager
from django.utils import timezone
from django.core.files.storage import default_storage as storage
from io import BytesIO
from django.core.files.base import ContentFile
from datetime import datetime
from uuid import uuid4
from notifications.models import Notification
from django.utils.deconstruct import deconstructible


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

incident_image_upload_path = path_and_rename('incident/')
incident_image_upload_path.__qualname__ = 'incident_image_upload_path'

# @deconstructible
# class PathRename(object):

#     def __init__(self, sub_path):
#         self.path = sub_path

#     def __call__(self, instance, filename):
#         ext = filename.split('.')[-1]
#         # set filename as random string
#         filename = '{}.{}'.format(uuid4().hex, ext)
#         # return the whole path to the file
#         return os.path.join(self.path, filename)

# path_and_rename = PathRename("/incident")

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
        
        

class AccidentCausation(SoftDeleteModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

class CollisionType(SoftDeleteModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category


class CrashType(SoftDeleteModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    crash_type = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.crash_type

class IncidentGeneral(SoftDeleteModel):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    STATUS = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected')
    )
    
    IF_DUPLICATE = (
        ('Duplicate', 'Duplicate'),
        ('Possible Duplicate', 'Possible Duplicate'),
        ('Not Duplicate', 'Not Duplicate')
    )
    
    WEATHER = (
        ('Clear Night', 'Clear Night'),
        ('Cloudy', 'Cloudy'),
        ('Day', 'Day'),
        ('Fog', 'Fog'),
        ('Hail', 'Hail'),
        ('Partially cloudy day', 'Partially cloudy day'),
        ('Partially cloudy night', 'Partially cloudy night'),
        ('Rain', 'Rain'),
        ('Rain', 'Rain'),
        ('Wind', 'Wind'),
    )
    
    LIGHT = (
        ('Dawn', 'Dawn'),
        ('Day', 'Day'),
        ('Dusk', 'Dusk'),
        ('Night', 'Night'),
    )
    
    SEVERITY = (
        ('Damage to Property', 'Damage to Property'),
        ('Fatal', 'Fatal'),
        ('Non-Fatal', 'Non-Fatal'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    generalid = models.CharField(max_length=250, unique=True, null=True, blank=True)
    description = models.TextField(max_length=250, blank=True)
    address = models.CharField(max_length=250)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.FloatField(max_length=20, blank=True, null=True)
    longitude = models.FloatField(max_length=20, blank=True, null=True)
    geo_location = gismodels.PointField(blank=True, null=True, srid=4326) # New field
    upload_photovideo = models.FileField(upload_to=incident_image_upload_path, blank=True, null=True)
    date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    time = models.TimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, blank=True, null=True)
    duplicate =  models.CharField(choices=IF_DUPLICATE,max_length=250, blank=True, null=True)
    duplicate_general =  models.ForeignKey('incidentreport.IncidentGeneral', on_delete=models.CASCADE, null=True, blank=True)
    accident_factor = models.ForeignKey(AccidentCausation, on_delete=models.SET_NULL, blank=True, null=True)
    collision_type = models.ForeignKey(CollisionType, on_delete=models.SET_NULL, blank=True, null=True)
    crash_type = models.ForeignKey(CrashType, on_delete=models.SET_NULL, blank=True, null=True)
    weather =  models.CharField(choices=WEATHER, max_length=250,blank=True, null=True)
    light =  models.CharField(choices=LIGHT,max_length=250, blank=True, null=True)
    severity = models.CharField(choices=SEVERITY, max_length=250, blank=True, null=True)
    movement_code = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_status(self):
        if self.status == 1:
            incident_status = 'Pending'
        elif self.status == 2:
            incident_status = 'Approved'
        elif self.status == 3:
            incident_status = 'Rejected'
        return incident_status
    
    
    def save(self, *args, **kwargs):
        # super(IncidentGeneral, self).save(*args, **kwargs)
        if self.latitude and self.longitude:
            self.geo_location = Point(float(self.longitude), float(self.latitude))
            super(IncidentGeneral, self).save(*args, **kwargs)

    # @receiver(post_save, sender=UserReport)
    # def create_user_report_general(sender, instance, created, **kwargs):
    #     if created:
    #         IncidentGeneral.objects.create(user_report=instance)
    
    # post_save.connect(create_user_report_general, sender=UserReport) 

class IncidentNotif(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_receiver')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sender')
    incident_general_report = models.ForeignKey(IncidentGeneral, on_delete=models.CASCADE, related_name='report_general')
    
    def user_report_incident (sender, instance, *args, **kwargs):
        incidentnotif = instance
        incident_report = incidentnotif.incident_general_report
        sender = incidentnotif.sender
        notify = Notification(incident_report=incident_report, sender=sender, user=incident_report.user, notification_type=1)
        notify.save()

class IncidentPerson(SoftDeleteModel):
    GENDER = (
        ('Female', 'Female'),
        ('Male', 'Male'),
    )
    
    INVOLVEMENT = (
        ('Pedestrian', 'Pedestrian'),
        ('Witness', 'Witness'),
        ('Passenger', 'Passenger'),
        ('Driver', 'Driver'),
    )
    
    ID_PRESENTED = (
        ("Driver's License", "Driver's License"),
        ('Government', 'Government'),
        ('Passport', 'Passport'),
        ('School Id', 'School Id'),
        ('Others', 'Others'),
    )
    
    INJURY = (
        ("Fatal", "Fatal"),
        ('Minor', 'Minor'),
        ('Not Injured', 'Not Injured'),
        ('Serious', 'Serious'),
    )
    
    DRIVER_ERROR = (
        ("Bad Overtaking", "Bad Overtaking"),
        ('Bad Turning', 'Bad Turning'),
        ('Fatigued / Asleep', 'Fatigued / Asleep'),
        ('Inattentive', 'Inattentive'),
        ('No Signal', 'No Signal'),
        ('Too Close', 'Too Close'),
        ('Too Fast', 'Too Fast'),
        ('Using Cellphone', 'Using Cellphone'),
    )
    
    ALCOHOL_DRUGS = (
        ("Alcohol Suspected", "Alcohol Suspected"),
        ('Drugs suspected', 'Drugs suspected'),
    )
    
    SEATBELT_HELMET = (
        ("Seat belt/Helmet Worn", "Seat belt/Helmet Worn"),
        ('Not worn', 'Not worn'),
        ('Not worn correctly', 'Not worn correctly'),
    )
    
    incident_general = models.ForeignKey(IncidentGeneral, on_delete=models.CASCADE, null=True, blank=True)
    incident_first_name = models.CharField(max_length=250, blank=True)
    incident_middle_name = models.CharField(max_length=250, blank=True)
    incident_last_name = models.CharField(max_length=250, blank=True)
    incident_age = models.CharField(max_length=250, blank=True)
    incident_gender =  models.CharField(choices=GENDER,max_length=250, blank=True, null=True)
    incident_address = models.CharField(max_length=250, blank=True)
    incident_involvement =  models.CharField(choices=INVOLVEMENT, max_length=250,blank=True, null=True)
    incident_id_presented =  models.CharField(choices=ID_PRESENTED, max_length=250,blank=True, null=True)
    incident_id_number = models.CharField(max_length=250, blank=True)
    incident_injury =  models.CharField(choices=INJURY, max_length=250,blank=True, null=True)
    incident_driver_error =  models.CharField(choices=DRIVER_ERROR,max_length=250, blank=True, null=True)
    incident_alcohol_drugs =  models.CharField(choices=ALCOHOL_DRUGS, max_length=250,blank=True, null=True)
    incident_seatbelt_helmet =  models.CharField(choices=SEATBELT_HELMET,max_length=250, blank=True, null=True)
    incident_photo_id = models.FileField(upload_to=incident_image_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class IncidentVehicle(SoftDeleteModel):
    CLASSIFICATION = (
        ('Diplomat', 'Diplomat'),
        ('Government', 'Government'),
        ('Private', 'Private'),
        ('Public / For Hire`', 'Public / For Hire`'),
    )
    
    VEHICLE_TYPE = (
        ('Ambulance', 'Ambulance'),
        ('Animal', 'Animal'),
        ('Armored Car', 'Armored Car'),
        ('Bicycle', 'Bicycle'),
        ('Bus', 'Bus'),
        ('Car', 'Car'),
        ('Electric Bike', 'Electric Bike'),
        ('Habal-habal', 'Habal-habal'),
        ('Heavy Equipment', 'Heavy Equipment'),
        ('Horse-Driven Carriage (Tartanilla)', 'Horse-Driven Carriage (Tartanilla)'),
        ('Jeepney', 'Jeepney'),
        ('Motorcycle', 'Motorcycle'),
        ('Pedestrian', 'Pedestrian'),
        ('Pedicab', 'Pedicab'),
        ('Push-Cart', 'Push-Cart'),
        ('SUV', 'SUV'),
        ('Taxi (metered)', 'Taxi (metered)'),
        ('Tricycle (Articulated)', 'Tricycle (Articulated)'),
        ('Truck (Fire)', 'Truck (Fire)'),
        ('Truck (Pick-up)', 'Truck (Pick-up)'),
        ('Truck (Rigid)', 'Truck (Rigid)'),
        ('Truck (Unknown)', 'Truck (Unknown)'),
        ('Van', 'Van'),
        ('Water Vessel', 'Water Vessel'),
        ('Others', 'Others'),
    )
    
    MANEUVER = (
        ("Left-turn", "Left-turn"),
        ('Right-turn', 'Right-turn'),
        ('U-turn', 'U-turn'),
        ('Cross Traffic', 'Cross Traffic'),
        ('Merging', 'Merging'),
        ('Diverging', 'Diverging'),
        ('Overtaking', 'Overtaking'),
        ('Going Ahead', 'Going Ahead'),
        ('Reversing', 'Reversing'),
        ('Sudden Start', 'Sudden Start'),
        ('Sudden Stop', 'Sudden Stop'),
        ('Parked Off Road', 'Parked Off Road'),
        ('Parked On Road', 'Parked On Road'),
    )
    
    DAMAGE = (
        ("None", "None"),
        ('Front', 'Front'),
        ('Left', 'Left'),
        ('Multiple', 'Multiple'),
        ('Rear', 'Rear'),
        ('Right', 'Right'),
        ('Roof', 'Roof'),
    )
    
    DEFECT = (
        ("None", "None"),
        ('Breaks', 'Breaks'),
        ('Lights', 'Lights'),
        ('Multiple', 'Multiple'),
        ('Steering', 'Steering'),
        ('Tires', 'Tires'),
    )
    
    LOADING = (
        ("Legal", "Legal"),
        ('Overloaded', 'Overloaded'),
        ('Unsafe Load', 'Unsafe Load'),
        ('Others', 'Others'),
    )
    
    incident_general = models.ForeignKey(IncidentGeneral, on_delete=models.CASCADE, null=True, blank=True)
    classification = models.CharField(choices=CLASSIFICATION, max_length=250, blank=True, null=True)
    vehicle_type = models.CharField(choices=VEHICLE_TYPE, max_length=250, blank=True, null=True)
    brand = models.CharField(max_length=250, blank=True)
    plate_number = models.CharField(max_length=250, blank=True)
    engine_number = models.CharField(max_length=250, blank=True)
    chassis_number = models.CharField(max_length=250, blank=True)
    insurance_details = models.TextField(max_length=250, blank=True)
    maneuver = models.CharField(choices=MANEUVER, max_length=250,blank=True, null=True)
    damage =models.CharField(choices=DAMAGE,max_length=250, blank=True, null=True)
    defect = models.CharField(choices=DEFECT,max_length=250, blank=True, null=True)
    loading = models.CharField(choices=LOADING,max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.id

class IncidentMedia(SoftDeleteModel):
    incident_general = models.ForeignKey(IncidentGeneral, on_delete=models.CASCADE, null=True, blank=True)
    media_description = models.TextField(max_length=250, blank=True)
    incident_upload_photovideo = models.FileField(upload_to=incident_image_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.id
    
    

class IncidentRemark(SoftDeleteModel):
    incident_general = models.OneToOneField(IncidentGeneral, on_delete=models.CASCADE, null=True, blank=True)
    responder =  models.CharField(max_length=250, blank=True)
    action_taken = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.responder
    
    # @receiver(post_save, sender=IncidentGeneral)
    # def create_user_report_remark(sender, instance, created, **kwargs):
    #     if created:
    #         IncidentRemark.objects.create(incident_general=instance)
    
    # post_save.connect(create_user_report_remark, sender=IncidentGeneral) 


class Incident(SoftDeleteModel):
    incident_general = models.OneToOneField(IncidentGeneral, on_delete=models.CASCADE)
    incident_general = models.ForeignKey(IncidentGeneral, on_delete=models.SET_NULL, blank=True, null=True)
    incident_person = models.ForeignKey(IncidentPerson, on_delete=models.SET_NULL, blank=True, null=True)
    incident_vehicle = models.ForeignKey(IncidentVehicle, on_delete=models.SET_NULL, blank=True, null=True)
    incident_media = models.ForeignKey(IncidentMedia, on_delete=models.SET_NULL, blank=True, null=True)
    incident_remark = models.ForeignKey(IncidentRemark, on_delete=models.SET_NULL, blank=True, null=True)
    
    
#Likes
post_save.connect(IncidentNotif.user_report_incident, sender=IncidentNotif)