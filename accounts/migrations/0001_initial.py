# Generated by Django 4.1.2 on 2022-12-20 15:46

import accounts.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(default='Some String', max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('mobile_number', models.CharField(db_index=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must not consist of space and requires country code. eg : +639171234567', regex='^(\\+\\d{1,3})?,?\\s?\\d{8,13}')])),
                ('password', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(8)])),
                ('role', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Member'), (2, 'Admin'), (3, 'Super Admin')], null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Active'), (2, 'Deleted'), (3, 'Deactivated')], null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superadmin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('profile_picture', models.FileField(blank=True, null=True, upload_to=accounts.models.user_image_upload_path)),
                ('upload_id', models.FileField(blank=True, null=True, upload_to=accounts.models.user_image_upload_path)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
