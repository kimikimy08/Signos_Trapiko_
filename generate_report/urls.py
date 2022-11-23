from django.contrib import admin  
from django.urls import path  
from generate_report import views  
 
urlpatterns = [  
    path('generate_reports/', views.generate_reports, name='generate_reports'),
    # path('generate_report/export_users_xls', views.export_users_xls, name='export_users_xls'),
    # path('generate_report/export_accidentcausation_xls', views.export_accidentcausation_xls, name='export_accidentcausation_xls'),
    # path('generate_report/export_classification_xls', views.export_classification_xls, name='export_classification_xls'),
    # path('generate_report/export_collision_xls', views.export_collision_xls, name='export_collision_xls'),
    # path('generateinvoice/', views.GenerateInvoiceAccident.as_view(), name = 'generateinvoice_accident'),
    # path('generateinvoicecollision/', views.GenerateInvoiceCollision.as_view(), name = 'generateinvoice_collision'),
    # path('generateinvoicevehicle/', views.GenerateInvoiceVehicle.as_view(), name = 'generateinvoice_vehicle'),
    # path('generateinvoicecollisioni/', views.GenerateInvoiceCollision_i.as_view(), name = 'generateinvoice_collision_i'),
    
    path('generate_reports/accident/', views.GenerateInvoiceAccident, name = 'sa_generateinvoice_accident'),
    path('generate_reports/collision/', views.GenerateInvoiceCollision,name='sa_generateinvoice_collision'),
    path('generate_reports/vehicle/', views.GenerateInvoiceVehicle, name = 'sa_generateinvoice_vehicle'),
    
    path('generate_report/', views.generate_report, name='generate_report'),
    path('generate_report/accident/', views.A_GenerateInvoiceAccident, name = 'a_generateinvoice_accident'),
    path('generate_report/collision/', views.A_GenerateInvoiceCollision,name='a_generateinvoice_collision'),
]  