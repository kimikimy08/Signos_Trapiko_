from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    #path('', AccountViews.admin_dashboard, name='admin_dashboard'),
    path('profile/', views.admin_profile, name='admin_profile'),
    path('profiles/edit/', views.admin_profile_edit, name='admin_profile_edit'),
    
    path('profile/pending/', views.admin_profile_pending, name='admin_profile_pending'),
    path('profile/approved/', views.admin_profile_approved, name='admin_profile_approved'),
    path('profile/rejected/', views.admin_profile_rejected, name='admin_profile_rejected'),
    
    #path('userReport/', views.a_userReport, name='a_userReport'),
    #path('userReport/pending/', views.a_userReport_pending, name='a_userReport_pending'),
    #path('userReport/approved/', views.a_userReport_approved, name='a_userReport_approved'),
    #path('userReport/rejected/', views.a_userReport_rejected, name='a_userReport_rejected'),
    
    path('userAccount/delete/<user_id>/', views.admin_user_account_delete, name="admin_user_account_delete"),
    path('userAccount/', views.admin_user_account, name='admin_user_account'),
    path('userAccount/member/', views.admin_user_account_member, name='admin_user_account_member'),
    path('userAccount/admin/', views.admin_user_account_admin, name='admin_user_account_admin'),
    path('userAccount/superadmin/', views.admin_user_account_superadmin, name='admin_user_account_superadmin'),
    path('userAccounts/view/<int:id>/', views.admin_user_account_view, name='admin_user_account_view'),
    path('userAccounts/edit/<int:id>/', views.admin_user_account_edit, name='admin_user_account_edit'),
    path('userAccounts/delete/<int:id>/', views.admin_user_account_delete, name='admin_user_account_delete'),
    path('userAccounts/recycle_bin/', views.a_recycle_bin_user, name='a_recycle_bin_user'),
]