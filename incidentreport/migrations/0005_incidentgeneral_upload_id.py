# Generated by Django 4.1.2 on 2022-12-10 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generate_report', '0002_uploadfile'),
        ('incidentreport', '0004_remove_incidentotp_uid_alter_incidentotp_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentgeneral',
            name='upload_id',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='generate_report.uploadfile'),
        ),
    ]