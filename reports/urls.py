from django.urls import path
from . import views


urlpatterns = [
   	path('reports/', views.sa_reportslist, name='sa_reportslist'),
    path('reports/<int:id>', views.sa_reportslist_table, name='sa_reportslist_table'),
    path('generate_visual_report/', views.sa_generate_visual_report, name='sa_generate_visual_report'),
   	# path('<noti_id>/delete', DeleteNotification, name='delete-notification'),

]