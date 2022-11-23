from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('id','username', 'first_name', 'last_name', 'email', 'role', 'status', 'is_active', 'created_at')
    list_display_links = ('username', 'first_name', )
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class CustomProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birthdate')
    list_display_links = ('user', 'birthdate')

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, CustomProfileAdmin)

