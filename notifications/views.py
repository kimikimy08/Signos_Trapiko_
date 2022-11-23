from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.http import HttpResponse

from notifications.models import Notification
from accounts.models import User, UserProfile

# Create your views here.

def ShowNotifications(request):
    
    profile = get_object_or_404(UserProfile, user=request.user)
    notifications = Notification.objects.filter(user=request.user).order_by('-date')
    notifications_default = Notification.objects.all().order_by('-date')
    notifications_create = notifications_default.exclude(user=request.user)
    notifications_member = Notification.objects.filter(sender=request.user).order_by('-date')
    context = {
        'profile': profile,
        'notifications': notifications,
        'notifications_create': notifications_create,
        'notifications_member': notifications_member
    }
    return render(request, 'notifications.html', context)


def DeleteNotification(request, noti_id):
	user = request.user
	Notification.objects.filter(id=noti_id, user=user).delete()
	return redirect('show-notifications')


def CountNotifications(request):
	count_notifications = 0
	if request.user.is_authenticated:
		count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

	return {'count_notifications':count_notifications}