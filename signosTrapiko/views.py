from django.shortcuts import render
from incidentreport.models import IncidentGeneral
from accounts.models import UserProfile, User

def home(request):
    user = User.objects.filter(is_deleted=False)
    incident_general = IncidentGeneral.objects.all()
    context = {
        'user': user,
        'incident_general': incident_general,
    }
    return render(request, 'home.html', context)

def error_404(request, exception):
   context = {}
   return render(request,'404.html', context)

def error_500(request):
    context = {}
    return render(request,'500.html', context)