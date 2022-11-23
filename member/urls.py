from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    #path('', AccountViews.member_dashboard, name='member_dashboard'),
    path('profile/', views.member_profile, name='member_profile'),
    path('profiles/edit/', views.member_profile_edit, name='member_profile_edit'),
    
    path('profile/pending/', views.member_profile_pending, name='member_profile_pending'),
    path('profile/approved/', views.member_profile_approved, name='member_profile_approved'),
    path('profile/rejected/', views.member_profile_rejected, name='member_profile_rejected'),
]
