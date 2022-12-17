from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.http import HttpResponse

from notifications.models import Notification
from accounts.models import User, UserProfile
from incidentreport.models import  IncidentGeneral, IncidentRemark, IncidentMedia, IncidentPerson, IncidentVehicle, AccidentCausation, CollisionType, CrashType, IncidentOTP
from generate_report.models import UploadFile
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.

def sa_reportslist(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    
    incidentReports_gen = IncidentGeneral.objects.all()
    incidentReports = IncidentGeneral.objects.all()
    incidentReports_gen = IncidentGeneral.objects.all().order_by('-updated_at')
    notifications = Notification.objects.filter(incident_report__in=incidentReports_gen).order_by('-date')
    report_list = UploadFile.objects.all().order_by('-created')
    # incidentReports_gen = IncidentGeneral.objects.filter(upload_id__in=report_list)
    # report_list_table = IncidentGeneral.objects.filter(upload_id__in=report_list).order_by('-updated_at')
    paginator = Paginator(incidentReports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    # paginator = Paginator(incidentReports, 10)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
        'notifications': notifications,
        'report_list':report_list,
        # 'report_list_table': report_list_table,
        'incidentReports_gen': incidentReports_gen
        # 'IncidentGeneral': IncidentGeneral
    }
    return render(request, 'pages/super/super_report.html', context)

def sa_reportslist_table(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    incidentReports = IncidentGeneral.objects.filter(upload_id__pk = id).order_by('-updated_at')
    incidentReports_gen = IncidentGeneral.objects.filter(upload_id__pk = id)
    notifications = Notification.objects.filter(incident_report__in=incidentReports_gen).order_by('-date')
    report_list = UploadFile.objects.all().order_by('-created')
    report_list_table = IncidentGeneral.objects.filter(upload_id__in=report_list).order_by('-updated_at')
    paginator = Paginator(incidentReports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
            # if request.POST.get('Restore') == 'Restore':
        for i in incidentReports:
            x = request.POST.get(str(i.id))
            print(x)
            
            if str(x) == 'on':
                b = IncidentGeneral.objects.get(id=i.id)
                b.soft_delete()
                # b.is_deleted = True
                # b.deleted_at = timezone.now()
                messages.success(request, 'User Report successfully deleted')
    context = {
        'profile': profile,
        'incidentReports': page_obj,
        'notifications': notifications,
        'report_list':report_list,
        'report_list_table': report_list_table,
        'incidentReports_gen': incidentReports_gen
        # 'IncidentGeneral': IncidentGeneral
    }
    return render(request, 'pages/super/super_report_table.html', context)

def sa_generate_visual_report(request):
    return render(request, 'pages/super/generate_v_report.html')

