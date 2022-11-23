from django.urls import path, include
from . import views
from accounts import views as AccountViews
# from .views import GeneratePdf

urlpatterns = [
    #path('', AccountViews.member_dashboard, name='member_dashboard'),
    path('adashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('sdashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
    # path('dashboard', views.index,name='dashboard-index'),
    path('sdashboard/maps', views.index_map,name='dashboard-index-map'),
    path('adashboard/map', views.index_map_admin,name='dashboard-index-map-admin'),
    # path('sadashboard/export', GeneratePdf.as_view(),name='superadmin_dashboard_export'),
]
