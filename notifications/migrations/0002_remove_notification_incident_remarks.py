# Generated by Django 4.1.2 on 2022-12-09 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='incident_remarks',
        ),
    ]
