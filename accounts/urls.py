from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
    path('profile/', views.member_dashboard, name='member_dashboard'),
    
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_validate/<uidb64>/<token>/', views.reset_validate, name='reset_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    
    path('autologout/', views.AutoLogoutUser, name='autologout'),
    
]