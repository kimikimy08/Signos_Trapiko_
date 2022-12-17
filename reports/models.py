from django.db import models

from accounts.models import UserProfile
from django.urls import reverse

# Create your models here.
class Report(models.Model):
    name = models.CharField(max_length=120)
    image_pie = models.ImageField(upload_to='reports', blank=True)
    image_bar = models.ImageField(upload_to='reports', blank=True)
    image_dot = models.ImageField(upload_to='reports', blank=True)
    image_heat = models.ImageField(upload_to='reports', blank=True)
    image_map = models.ImageField(upload_to='reports', blank=True)
    remarks = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def get_absolute_url(self):
    #     return reverse('reports:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.name)

    # class Meta:
    #     ordering = ('-created',)