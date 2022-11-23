from django.urls import path
from . import views


urlpatterns = [
   	path('notifications/', views.ShowNotifications, name='show-notifications'),
   	# path('<noti_id>/delete', DeleteNotification, name='delete-notification'),

]