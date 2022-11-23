from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.superadmin_dashboard, name='superadmin'),
    path('profiles/', views.super_profile, name='super_profile'),
    path('profiles/edit/', views.super_profile_edit, name='super_profile_edit'),
    
    path('profiles/pending/', views.super_profile_pending, name='super_profile_pending'),
    path('profiles/approved/', views.super_profile_approved, name='super_profile_approved'),
    path('profiles/rejected/', views.super_profile_rejected, name='super_profile_rejected'),
    
    #path('userReports/', views.sa_userReport, name='sa_userReport'),
    #path('userReports/pending/', views.sa_userReport_pending, name='sa_userReport_pending'),
    #path('userReports/approved/', views.sa_userReport_approved, name='sa_userReport_approved'),
    #path('userReports/rejected/', views.sa_userReport_rejected, name='sa_userReport_rejected'),
    
    path('userAccounts/', views.super_user_account, name='super_user_account'),
    path('userAccounts/member/', views.super_user_account_member, name='super_user_account_member'),
    path('userAccounts/admin/', views.super_user_account_admin, name='super_user_account_admin'),
    path('userAccounts/superadmin/', views.super_user_account_superadmin, name='super_user_account_superadmin'),
    path('userAccounts/add/', views.super_user_account_add, name='super_user_account_add'),
    path('userAccounts/view/<int:id>/', views.super_user_account_view, name='super_user_account_view'),
    path('userAccounts/edit/<int:id>/', views.super_user_account_edit, name='super_user_account_edit'),
    path('userAccounts/delete/<int:id>/', views.super_user_account_delete, name='super_user_account_delete'),
    path('userAccounts/recycle_bin/', views.sa_recycle_bin_user, name='sa_recycle_bin_user'),
]