import datetime
from django.conf import settings
from django.shortcuts import render  
from django.http import HttpResponse 
from django.contrib.auth.models import User
from django.views import View
import xlwt
from accounts.models import UserProfile, User
from incidentreport.models import AccidentCausation,IncidentGeneral, IncidentVehicle
import pytz
from django.db.models import Count, Sum
from django.db.models import Q
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_admin, check_role_super, check_role_member, check_role_super_admin
from generate_report.models import GenerateReport
from django.views.decorators.cache import cache_control

# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_super)
def generate_reports(request):
    return render(request, 'pages/generate_report_sa.html')

# @login_required(login_url='login')
# @user_passes_test(check_role_super)
# def export_users_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="users.xls"'
 
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Users')
    
#     alignment = xlwt.Alignment()

#     alignment.horz = xlwt.Alignment.HORZ_LEFT
#     alignment.vert = xlwt.Alignment.VERT_TOP
#     alignment.CENTER = xlwt.Alignment.CENTER
#     style = xlwt.XFStyle() # Create Style
#     style.alignment = alignment # Add Alignment to Style
 
#     # Sheet header, first row
#     row_num = 0
 
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
    
#     header_font = xlwt.Font()

#     # Header font preferences
#     header_font.name = 'Times New Roman'
#     header_font.height = 20 * 15
#     header_font.bold = True

#     # Header Cells style definition
#     header_style = xlwt.XFStyle()
#     header_style.font = header_font 


#     body_font = xlwt.Font()

#     # Body font preferences
#     body_font.name = 'Arial'
#     body_font.italic = True


#     borders = xlwt.Borders()
#     borders.left = 1
#     borders.right = 1
#     borders.top = 1
#     borders.bottom = 1
#     header_style.borders = borders
    
#     # body cell name style definition
#     body_style = xlwt.XFStyle()
#     body_style.font = body_font
    
    
    
 
#     columns = ['Username', 'First name', 'Middle name', 'Last name', 'Email address', 'Mobile Number', 'Birthday', 'Role', 'Status', 'Last Login', 'Created At', 'Updated At']
 
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], header_style)
#         ws.col(col_num).width = 7000

        
 
#     # Sheet body, remaining rows
#     # font_style = xlwt.XFStyle()
 
#     rows = UserProfile.objects.all().values_list('user__username', 'user__first_name', "user__middle_name",'user__last_name', 'user__email', 'user__mobile_number', 'birthdate', 'user__role', 'user__status', 'user__last_login', 'created_at', 'updated_at').order_by('-user__last_login')
#     rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], body_style)
 
#     wb.save(response)
#     return response

# @login_required(login_url='login')
# @user_passes_test(check_role_super)
# def export_accidentcausation_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="accident_causation.xls"'
 
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Accident Causation')
    
#     alignment = xlwt.Alignment()

#     alignment.horz = xlwt.Alignment.HORZ_CENTER
#     alignment.vert = xlwt.Alignment.VERT_TOP
#     style = xlwt.XFStyle() # Create Style
#     style.alignment = alignment # Add Alignment to Style
 
#     # Sheet header, first row
#     row_num = 0
 
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
    
#     header_font = xlwt.Font()

#     # Header font preferences
#     header_font.name = 'Times New Roman'
#     header_font.height = 20 * 15
#     header_font.bold = True

#     # Header Cells style definition
#     header_style = xlwt.XFStyle()
#     header_style.font = header_font 


#     body_font = xlwt.Font()

#     # Body font preferences
#     body_font.name = 'Arial'
#     body_font.italic = True


#     borders = xlwt.Borders()
#     borders.left = 1
#     borders.right = 1
#     borders.top = 1
#     borders.bottom = 1
#     header_style.borders = borders
#     header_style.alignment = alignment
    
#     # body cell name style definition
#     body_style = xlwt.XFStyle()
#     body_style.font = body_font
#     body_style.alignment = alignment
    
    
 
#     columns = ['Accident Factor', 'Accident Factor Sub-Category', 'Damage to Property', 'Fatal', 'Non-Fatal Injury']
 
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], header_style)
#         ws.col(col_num).width = 10000
        
#     rows = IncidentGeneral.objects.all().values_list('accident_factor__category', 'accident_subcategory__sub_category')
#     rows = rows.annotate(
#         severity1=Count('severity', filter=Q(severity='Damage to Property')),
#         severity2=Count('severity', filter=Q(severity='Fatal')),
#         severity3=Count('severity', filter=Q(severity='Non-Fatal'))
#     )
    
#     # for item in rows:
#     #     print(item.accident_factor, item.severity1, item.severity2, item.severity3)
#     rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], body_style)
    
#     # queryset = IncidentGeneral.objects.all().values('accident_factor')
#     # queryset = queryset.annotate(
#     #     severity1=Count('severity', only=Q(severity=1)),
#     #     severity2=Count('severity', only=Q(severity=2)),
#     #     severity3=Count('severity', only=Q(severity=3))
#     # )

#     # for item in queryset:
#     #     print( item.severity1, item.severity2, item.severity3)
 
#     wb.save(response)
#     return response

# @login_required(login_url='login')
# @user_passes_test(check_role_super)
# def export_classification_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="vehicle_classification.xls"'
 
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Vehicle Classification')
    
#     alignment = xlwt.Alignment()

#     alignment.horz = xlwt.Alignment.HORZ_CENTER
#     alignment.vert = xlwt.Alignment.VERT_TOP
#     style = xlwt.XFStyle() # Create Style
#     style.alignment = alignment # Add Alignment to Style
 
#     # Sheet header, first row
#     row_num = 0
 
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
    
#     header_font = xlwt.Font()

#     # Header font preferences
#     header_font.name = 'Times New Roman'
#     header_font.height = 20 * 15
#     header_font.bold = True

#     # Header Cells style definition
#     header_style = xlwt.XFStyle()
#     header_style.font = header_font 


#     body_font = xlwt.Font()

#     # Body font preferences
#     body_font.name = 'Arial'
#     body_font.italic = True


#     borders = xlwt.Borders()
#     borders.left = 1
#     borders.right = 1
#     borders.top = 1
#     borders.bottom = 1
#     header_style.borders = borders
#     header_style.alignment = alignment
    
#     # body cell name style definition
#     body_style = xlwt.XFStyle()
#     body_style.font = body_font
#     body_style.alignment = alignment
    
    
 
#     columns = ['Vehicle Classification', 'Damage to Property', 'Fatal', 'Non-Fatal Injury']
 
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], header_style)
#         ws.col(col_num).width = 10000
        
#     rows = IncidentVehicle.objects.all().values_list('classification')
#     rows = rows.annotate(
#         severity1=Count('incident_general__severity', filter=Q(incident_general__severity='Damage to Property')),
#         severity2=Count('incident_general__severity', filter=Q(incident_general__severity='Fatal')),
#         severity3=Count('incident_general__severity', filter=Q(incident_general__severity='Non-Fatal'))
#     )
    
#     # for item in rows:
#     #     print(item.accident_factor, item.severity1, item.severity2, item.severity3)
#     rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], body_style)
    
#     # queryset = IncidentGeneral.objects.all().values('accident_factor')
#     # queryset = queryset.annotate(
#     #     severity1=Count('severity', only=Q(severity=1)),
#     #     severity2=Count('severity', only=Q(severity=2)),
#     #     severity3=Count('severity', only=Q(severity=3))
#     # )

#     # for item in queryset:
#     #     print( item.severity1, item.severity2, item.severity3)
 
#     wb.save(response)
#     return response

# @login_required(login_url='login')
# @user_passes_test(check_role_super)
# def export_collision_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="collision_type.xls"'
 
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Collision Type')
    
#     alignment = xlwt.Alignment()

#     alignment.horz = xlwt.Alignment.HORZ_CENTER
#     alignment.vert = xlwt.Alignment.VERT_TOP
#     style = xlwt.XFStyle() # Create Style
#     style.alignment = alignment # Add Alignment to Style
 
#     # Sheet header, first row
#     row_num = 0
 
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
    
#     header_font = xlwt.Font()

#     # Header font preferences
#     header_font.name = 'Times New Roman'
#     header_font.height = 20 * 15
#     header_font.bold = True

#     # Header Cells style definition
#     header_style = xlwt.XFStyle()
#     header_style.font = header_font 


#     body_font = xlwt.Font()

#     # Body font preferences
#     body_font.name = 'Arial'
#     body_font.italic = True


#     borders = xlwt.Borders()
#     borders.left = 1
#     borders.right = 1
#     borders.top = 1
#     borders.bottom = 1
#     header_style.borders = borders
#     header_style.alignment = alignment
    
#     # body cell name style definition
#     body_style = xlwt.XFStyle()
#     body_style.font = body_font
#     body_style.alignment = alignment
    
    
 
#     columns = ['Collision Type', 'Collision Type Sub-Category', 'Damage to Property', 'Fatal', 'Non-Fatal Injury']
 
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], header_style)
#         ws.col(col_num).width = 10000
        
#     rows = IncidentGeneral.objects.all().values_list('collision_type__category', 'collision_subcategory__sub_category')
#     rows = rows.annotate(
#         severity1=Count('severity', filter=Q(severity='Damage to Property')),
#         severity2=Count('severity', filter=Q(severity='Fatal')),
#         severity3=Count('severity', filter=Q(severity='Non-Fatal'))
#     )
    
#     # for item in rows:
#     #     print(item.accident_factor, item.severity1, item.severity2, item.severity3)
#     rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], body_style)
    
#     # queryset = IncidentGeneral.objects.all().values('accident_factor')
#     # queryset = queryset.annotate(
#     #     severity1=Count('severity', only=Q(severity=1)),
#     #     severity2=Count('severity', only=Q(severity=2)),
#     #     severity3=Count('severity', only=Q(severity=3))
#     # )

#     # for item in queryset:
#     #     print( item.severity1, item.severity2, item.severity3)
 
#     wb.save(response)
#     return response


# def fetch_resources(uri, rel):
#     path = os.path.join(uri.replace(settings.STATIC_URL, ""))
#     return path

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=fetch_resources)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(check_role_super)
def GenerateInvoiceAccident(request):
    try:
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            report = GenerateReport(user=request.user, fromdate=fromdate, todate=todate, report="Accident Causation PDF")
            report.save()
            
        print(fromdate, todate)
    
        # incident_general_accident = IncidentGeneral.objects.filter(user_report__status = 2).values('accident_factor__category').annotate(Count('severity'), filter=Q(severity='Damage to Property'))
        incident_general_accident = IncidentGeneral.objects.filter(status = 2, date__range=[fromdate, todate ])
        incident_general_accident1 = IncidentGeneral.objects.filter(status = 2,severity='Fatal', date__range=[fromdate, todate ] ).annotate(Count('severity'))
        incident_general_accident2 = IncidentGeneral.objects.filter(status = 2,severity='Damage to Property', date__range=[fromdate, todate ] ).annotate(Count('severity'))
        incident_general_accident3 = IncidentGeneral.objects.filter(status = 2,severity='Non-Fatal', date__range=[fromdate, todate ] ).annotate(Count('severity'))
        incident_general_classification = IncidentGeneral.objects.filter(status = 2, severity="Damage to Property", date__range=[fromdate, todate ]).distinct('accident_factor')
        incident_general_collision = IncidentGeneral.objects.filter(status = 2, severity="Damage to Property", date__range=[fromdate, todate ]).distinct('accident_factor') #you can filter using order_id as well
        
        
        report1 = GenerateReport.objects.all().order_by('-created_at')[:1]
    except:
        return HttpResponse("505 Not Found")
    data = {
        'incident_general_accident': incident_general_accident,
        'incident_general_classification': incident_general_classification,
        'incident_general_collision': incident_general_collision,
        'incident_general_accident1': incident_general_accident1,
        'incident_general_accident2': incident_general_accident2,
        'incident_general_accident3': incident_general_accident3,
        'report1':report1
            # 'amount': order_db.total_amount,
    }
    pdf = render_to_pdf('pages/generate_report_pdf_accident.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Accident_Causation.pdf" #%(data['incident_general.id'])
        content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
        # return HttpResponse("Not found")
    return render(request, 'pages/generate_report_sa.html')

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(check_role_super)
def GenerateInvoiceCollision(request):
    try:
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
            
        print(fromdate, todate)
    
        # incident_general_accident = IncidentGeneral.objects.filter(user_report__status = 2).values('accident_factor__category').annotate(Count('severity'), filter=Q(severity='Damage to Property'))
        incident_general_collision = IncidentGeneral.objects.filter(status = 2, date__range=[fromdate, todate ])
        incident_general_collision1 = IncidentGeneral.objects.filter(status = 2,severity='Fatal', date__range=[fromdate, todate ] ).annotate(Count('severity'))
        incident_general_collision2 = IncidentGeneral.objects.filter(status = 2,severity='Damage to Property', date__range=[fromdate, todate ] ).annotate(Count('severity'))
        incident_general_collision3 = IncidentGeneral.objects.filter(status = 2,severity='Non-Fatal', date__range=[fromdate, todate ]).annotate(Count('severity'))
        incident_general_classification = IncidentGeneral.objects.filter(status = 2, severity="Damage to Property", date__range=[fromdate, todate ]).distinct('accident_factor')
        report = GenerateReport(user=request.user, fromdate=fromdate, todate=todate, report="Collision Type PDF")
        report.save()
        report1 = GenerateReport.objects.all().order_by('-created_at')[:0]      
           
            
    except:
        return HttpResponse("505 Not Found")
    data = {
        'incident_general_collision': incident_general_collision,
        'incident_general_classification': incident_general_classification,
        'incident_general_collision': incident_general_collision,
        'incident_general_collision1': incident_general_collision1,
        'incident_general_collision2': incident_general_collision2,
        'incident_general_collision3': incident_general_collision3,
        'report1': report1
            # 'amount': order_db.total_amount,
    }
    pdf = render_to_pdf('pages/generate_report_pdf_collision.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Collision_Type.pdf" #%(data['incident_general.id'])
        content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
        # return HttpResponse("Not found")
    return render(request, 'pages/generate_report_sa.html')

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(check_role_super)
def GenerateInvoiceVehicle(request):
    try:
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
            
        print(fromdate, todate)
    
        # incident_general_accident = IncidentGeneral.objects.filter(user_report__status = 2).values('accident_factor__category').annotate(Count('severity'), filter=Q(severity='Damage to Property'))
        incident_vehicle = IncidentVehicle.objects.filter(incident_general__status = 2, incident_general__date__range=[fromdate, todate ])
        incident_vehicle1 = IncidentVehicle.objects.filter(incident_general__status = 2,incident_general__severity='Fatal', incident_general__date__range=[fromdate, todate ] ).annotate(Count('incident_general__severity'))
        incident_vehicle2 = IncidentVehicle.objects.filter(incident_general__status = 2,incident_general__severity='Damage to Property', incident_general__date__range=[fromdate, todate ] ).annotate(Count('incident_general__severity'))
        incident_vehicle3 = IncidentVehicle.objects.filter(incident_general__status = 2,incident_general__severity='Non-Fatal', incident_general__date__range=[fromdate, todate ] ).annotate(Count('incident_general__severity'))
            # incident_general_classification = IncidentGeneral.objects.filter(user_report__status = 2, severity="Damage to Property").distinct('accident_factor')
           
    except:
        return HttpResponse("505 Not Found")
        
    data = {'incident_vehicle': incident_vehicle,
            'incident_vehicle1': incident_vehicle1,
            'incident_vehicle2': incident_vehicle2,
            'incident_vehicle3': incident_vehicle3,
                # 'incident_general_collision3': incident_general_collision3,
                # 'amount': order_db.total_amount,
        }
    pdf = render_to_pdf('pages/generate_report_pdf_vehicle.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Vehicle_Classification.pdf" #%(data['incident_general.id'])
        content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return render(request, 'pages/generate_report_sa.html')

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(check_role_admin)
def generate_report(request):
    return render(request, 'pages/generate_report_a.html')

# @login_required(login_url='login')
# @user_passes_test(check_role_super)
# def export_users_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="users.xls"'
 
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Users')
    
#     alignment = xlwt.Alignment()

#     alignment.horz = xlwt.Alignment.HORZ_LEFT
#     alignment.vert = xlwt.Alignment.VERT_TOP
#     alignment.CENTER = xlwt.Alignment.CENTER
#     style = xlwt.XFStyle() # Create Style
#     style.alignment = alignment # Add Alignment to Style
 
#     # Sheet header, first row
#     row_num = 0
 
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
    
#     header_font = xlwt.Font()

#     # Header font preferences
#     header_font.name = 'Times New Roman'
#     header_font.height = 20 * 15
#     header_font.bold = True

#     # Header Cells style definition
#     header_style = xlwt.XFStyle()
#     header_style.font = header_font 


#     body_font = xlwt.Font()

#     # Body font preferences
#     body_font.name = 'Arial'
#     body_font.italic = True


#     borders = xlwt.Borders()
#     borders.left = 1
#     borders.right = 1
#     borders.top = 1
#     borders.bottom = 1
#     header_style.borders = borders
    
#     # body cell name style definition
#     body_style = xlwt.XFStyle()
#     body_style.font = body_font
    
    
    
 
#     columns = ['Username', 'First name', 'Middle name', 'Last name', 'Email address', 'Mobile Number', 'Birthday', 'Role', 'Status', 'Last Login', 'Created At', 'Updated At']
 
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], header_style)
#         ws.col(col_num).width = 7000

        
 
#     # Sheet body, remaining rows
#     # font_style = xlwt.XFStyle()
 
#     rows = UserProfile.objects.all().values_list('user__username', 'user__first_name', "user__middle_name",'user__last_name', 'user__email', 'user__mobile_number', 'birthdate', 'user__role', 'user__status', 'user__last_login', 'created_at', 'updated_at').order_by('-user__last_login')
#     rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], body_style)
 
#     wb.save(response)
#     return response

# @login_required(login_url='login')
# @user_passes_test(check_role_super)
# def export_accidentcausation_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="accident_causation.xls"'
 
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Accident Causation')
    
#     alignment = xlwt.Alignment()

#     alignment.horz = xlwt.Alignment.HORZ_CENTER
#     alignment.vert = xlwt.Alignment.VERT_TOP
#     style = xlwt.XFStyle() # Create Style
#     style.alignment = alignment # Add Alignment to Style
 
#     # Sheet header, first row
#     row_num = 0
 
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
    
#     header_font = xlwt.Font()

#     # Header font preferences
#     header_font.name = 'Times New Roman'
#     header_font.height = 20 * 15
#     header_font.bold = True

#     # Header Cells style definition
#     header_style = xlwt.XFStyle()
#     header_style.font = header_font 


#     body_font = xlwt.Font()

#     # Body font preferences
#     body_font.name = 'Arial'
#     body_font.italic = True


#     borders = xlwt.Borders()
#     borders.left = 1
#     borders.right = 1
#     borders.top = 1
#     borders.bottom = 1
#     header_style.borders = borders
#     header_style.alignment = alignment
    
#     # body cell name style definition
#     body_style = xlwt.XFStyle()
#     body_style.font = body_font
#     body_style.alignment = alignment
    
    
 
#     columns = ['Accident Factor', 'Accident Factor Sub-Category', 'Damage to Property', 'Fatal', 'Non-Fatal Injury']
 
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], header_style)
#         ws.col(col_num).width = 10000
        
#     rows = IncidentGeneral.objects.all().values_list('accident_factor__category', 'accident_subcategory__sub_category')
#     rows = rows.annotate(
#         severity1=Count('severity', filter=Q(severity='Damage to Property')),
#         severity2=Count('severity', filter=Q(severity='Fatal')),
#         severity3=Count('severity', filter=Q(severity='Non-Fatal'))
#     )
    
#     # for item in rows:
#     #     print(item.accident_factor, item.severity1, item.severity2, item.severity3)
#     rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], body_style)
    
#     # queryset = IncidentGeneral.objects.all().values('accident_factor')
#     # queryset = queryset.annotate(
#     #     severity1=Count('severity', only=Q(severity=1)),
#     #     severity2=Count('severity', only=Q(severity=2)),
#     #     severity3=Count('severity', only=Q(severity=3))
#     # )

#     # for item in queryset:
#     #     print( item.severity1, item.severity2, item.severity3)
 
#     wb.save(response)
#     return response

# @login_required(login_url='login')
# @user_passes_test(check_role_super)
# def export_classification_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="vehicle_classification.xls"'
 
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Vehicle Classification')
    
#     alignment = xlwt.Alignment()

#     alignment.horz = xlwt.Alignment.HORZ_CENTER
#     alignment.vert = xlwt.Alignment.VERT_TOP
#     style = xlwt.XFStyle() # Create Style
#     style.alignment = alignment # Add Alignment to Style
 
#     # Sheet header, first row
#     row_num = 0
 
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
    
#     header_font = xlwt.Font()

#     # Header font preferences
#     header_font.name = 'Times New Roman'
#     header_font.height = 20 * 15
#     header_font.bold = True

#     # Header Cells style definition
#     header_style = xlwt.XFStyle()
#     header_style.font = header_font 


#     body_font = xlwt.Font()

#     # Body font preferences
#     body_font.name = 'Arial'
#     body_font.italic = True


#     borders = xlwt.Borders()
#     borders.left = 1
#     borders.right = 1
#     borders.top = 1
#     borders.bottom = 1
#     header_style.borders = borders
#     header_style.alignment = alignment
    
#     # body cell name style definition
#     body_style = xlwt.XFStyle()
#     body_style.font = body_font
#     body_style.alignment = alignment
    
    
 
#     columns = ['Vehicle Classification', 'Damage to Property', 'Fatal', 'Non-Fatal Injury']
 
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], header_style)
#         ws.col(col_num).width = 10000
        
#     rows = IncidentVehicle.objects.all().values_list('classification')
#     rows = rows.annotate(
#         severity1=Count('incident_general__severity', filter=Q(incident_general__severity='Damage to Property')),
#         severity2=Count('incident_general__severity', filter=Q(incident_general__severity='Fatal')),
#         severity3=Count('incident_general__severity', filter=Q(incident_general__severity='Non-Fatal'))
#     )
    
#     # for item in rows:
#     #     print(item.accident_factor, item.severity1, item.severity2, item.severity3)
#     rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], body_style)
    
#     # queryset = IncidentGeneral.objects.all().values('accident_factor')
#     # queryset = queryset.annotate(
#     #     severity1=Count('severity', only=Q(severity=1)),
#     #     severity2=Count('severity', only=Q(severity=2)),
#     #     severity3=Count('severity', only=Q(severity=3))
#     # )

#     # for item in queryset:
#     #     print( item.severity1, item.severity2, item.severity3)
 
#     wb.save(response)
#     return response

# @login_required(login_url='login')
# @user_passes_test(check_role_super)
# def export_collision_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="collision_type.xls"'
 
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Collision Type')
    
#     alignment = xlwt.Alignment()

#     alignment.horz = xlwt.Alignment.HORZ_CENTER
#     alignment.vert = xlwt.Alignment.VERT_TOP
#     style = xlwt.XFStyle() # Create Style
#     style.alignment = alignment # Add Alignment to Style
 
#     # Sheet header, first row
#     row_num = 0
 
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
    
#     header_font = xlwt.Font()

#     # Header font preferences
#     header_font.name = 'Times New Roman'
#     header_font.height = 20 * 15
#     header_font.bold = True

#     # Header Cells style definition
#     header_style = xlwt.XFStyle()
#     header_style.font = header_font 


#     body_font = xlwt.Font()

#     # Body font preferences
#     body_font.name = 'Arial'
#     body_font.italic = True


#     borders = xlwt.Borders()
#     borders.left = 1
#     borders.right = 1
#     borders.top = 1
#     borders.bottom = 1
#     header_style.borders = borders
#     header_style.alignment = alignment
    
#     # body cell name style definition
#     body_style = xlwt.XFStyle()
#     body_style.font = body_font
#     body_style.alignment = alignment
    
    
 
#     columns = ['Collision Type', 'Collision Type Sub-Category', 'Damage to Property', 'Fatal', 'Non-Fatal Injury']
 
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], header_style)
#         ws.col(col_num).width = 10000
        
#     rows = IncidentGeneral.objects.all().values_list('collision_type__category', 'collision_subcategory__sub_category')
#     rows = rows.annotate(
#         severity1=Count('severity', filter=Q(severity='Damage to Property')),
#         severity2=Count('severity', filter=Q(severity='Fatal')),
#         severity3=Count('severity', filter=Q(severity='Non-Fatal'))
#     )
    
#     # for item in rows:
#     #     print(item.accident_factor, item.severity1, item.severity2, item.severity3)
#     rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], body_style)
    
#     # queryset = IncidentGeneral.objects.all().values('accident_factor')
#     # queryset = queryset.annotate(
#     #     severity1=Count('severity', only=Q(severity=1)),
#     #     severity2=Count('severity', only=Q(severity=2)),
#     #     severity3=Count('severity', only=Q(severity=3))
#     # )

#     # for item in queryset:
#     #     print( item.severity1, item.severity2, item.severity3)
 
#     wb.save(response)
#     return response


def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("cp1252")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(check_role_admin)
def A_GenerateInvoiceAccident(request):
    try:
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
            
        print(fromdate, todate)
    
        # incident_general_accident = IncidentGeneral.objects.filter(user_report__status = 2).values('accident_factor__category').annotate(Count('severity'), filter=Q(severity='Damage to Property'))
        incident_general_accident = IncidentGeneral.objects.filter(status = 2, date__range=[fromdate, todate ])
        incident_general_accident1 = IncidentGeneral.objects.filter(status = 2,severity='Fatal', date__range=[fromdate, todate ] ).annotate(Count('severity'))
        incident_general_accident2 = IncidentGeneral.objects.filter(status = 2,severity='Damage to Property', date__range=[fromdate, todate ] ).annotate(Count('severity'))
        incident_general_accident3 = IncidentGeneral.objects.filter(status = 2,severity='Non-Fatal', date__range=[fromdate, todate ] ).annotate(Count('severity'))
        incident_general_classification = IncidentGeneral.objects.filter(status = 2, severity="Damage to Property", date__range=[fromdate, todate ]).distinct('accident_factor')
        incident_general_collision = IncidentGeneral.objects.filter(status = 2, severity="Damage to Property", date__range=[fromdate, todate ]).distinct('accident_factor') #you can filter using order_id as well
            
    except:
        return HttpResponse("505 Not Found")
    data = {
        'incident_general_accident': incident_general_accident,
        'incident_general_classification': incident_general_classification,
        'incident_general_collision': incident_general_collision,
        'incident_general_accident1': incident_general_accident1,
        'incident_general_accident2': incident_general_accident2,
        'incident_general_accident3': incident_general_accident3,
            # 'amount': order_db.total_amount,
    }
    pdf = render_to_pdf('pages/generate_report_pdf_accident.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Accident_Causation.pdf" #%(data['incident_general.id'])
        content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
        # return HttpResponse("Not found")
    return render(request, 'pages/generate_report_a.html')

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(check_role_admin)
def A_GenerateInvoiceCollision(request):
    try:
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
            
        print(fromdate, todate)
    
        # incident_general_accident = IncidentGeneral.objects.filter(user_report__status = 2).values('accident_factor__category').annotate(Count('severity'), filter=Q(severity='Damage to Property'))
        incident_general_collision = IncidentGeneral.objects.filter(status = 2, date__range=[fromdate, todate ])
        incident_general_collision1 = IncidentGeneral.objects.filter(status = 2,severity='Fatal', date__range=[fromdate, todate ] ).annotate(Count('severity'))
        incident_general_collision2 = IncidentGeneral.objects.filter(status = 2,severity='Damage to Property', date__range=[fromdate, todate ] ).annotate(Count('severity'))
        incident_general_collision3 = IncidentGeneral.objects.filter(status = 2,severity='Non-Fatal', date__range=[fromdate, todate ]).annotate(Count('severity'))
        incident_general_classification = IncidentGeneral.objects.filter(status = 2, severity="Damage to Property", date__range=[fromdate, todate ]).distinct('accident_factor')

           
            
    except:
        return HttpResponse("505 Not Found")
    data = {
        'incident_general_collision': incident_general_collision,
        'incident_general_classification': incident_general_classification,
        'incident_general_collision': incident_general_collision,
        'incident_general_collision1': incident_general_collision1,
        'incident_general_collision2': incident_general_collision2,
        'incident_general_collision3': incident_general_collision3,
            # 'amount': order_db.total_amount,
    }
    pdf = render_to_pdf('pages/generate_report_pdf_collision.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Collision_Type.pdf" #%(data['incident_general.id'])
        content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
        # return HttpResponse("Not found")
    return render(request, 'pages/generate_report_a.html')

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(check_role_admin)
def A_GenerateInvoiceVehicle(request):
    try:
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
            
        print(fromdate, todate)
    
        # incident_general_accident = IncidentGeneral.objects.filter(user_report__status = 2).values('accident_factor__category').annotate(Count('severity'), filter=Q(severity='Damage to Property'))
        incident_vehicle = IncidentVehicle.objects.filter(incident_general__user_report__status = 2, incident_general__user_report__date__range=[fromdate, todate ])
        incident_vehicle1 = IncidentVehicle.objects.filter(incident_general__user_report__status = 2,incident_general__severity='Fatal', incident_general__user_report__date__range=[fromdate, todate ] ).annotate(Count('incident_general__severity'))
        incident_vehicle2 = IncidentVehicle.objects.filter(incident_general__user_report__status = 2,incident_general__severity='Damage to Property', incident_general__user_report__date__range=[fromdate, todate ] ).annotate(Count('incident_general__severity'))
        incident_vehicle3 = IncidentVehicle.objects.filter(incident_general__user_report__status = 2,incident_general__severity='Non-Fatal', incident_general__user_report__date__range=[fromdate, todate ] ).annotate(Count('incident_general__severity'))
            # incident_general_classification = IncidentGeneral.objects.filter(user_report__status = 2, severity="Damage to Property").distinct('accident_factor')
           
    except:
        return HttpResponse("505 Not Found")
        
    data = {'incident_vehicle': incident_vehicle,
            'incident_vehicle1': incident_vehicle1,
            'incident_vehicle2': incident_vehicle2,
            'incident_vehicle3': incident_vehicle3,
                # 'incident_general_collision3': incident_general_collision3,
                # 'amount': order_db.total_amount,
        }
    pdf = render_to_pdf('pages/generate_report_pdf_vehicle.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Vehicle_Classification.pdf" #%(data['incident_general.id'])
        content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return render(request, 'pages/generate_report_a.html')