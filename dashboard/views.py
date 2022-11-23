
from datetime import datetime
from io import BytesIO
from django.http import JsonResponse
from django.shortcuts import render
import folium
from folium import plugins
from folium.plugins import HeatMapWithTime
from folium.plugins import FastMarkerCluster
from folium.plugins import MarkerCluster
import plotly.express as px
from django.db.models import Count
import numpy as np

from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf

import pandas as pd
from incidentreport.models import IncidentGeneral, IncidentRemark, IncidentMedia, IncidentPerson, IncidentVehicle, AccidentCausation, CollisionType, CrashType
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_admin, check_role_super, check_role_member, check_role_super_admin
from django.views.decorators.cache import cache_control

# Create your views here.


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(check_role_admin)
def admin_dashboard(request):
    fromdate = request.POST.get('fromdate')
    todate = request.POST.get('todate')
    incidentReports_pending = IncidentGeneral.objects.filter(
        status=1)
    today = datetime.today().date()
    incidentReports_today = IncidentGeneral.objects.filter(
        created_at__date=today)
    incidentReports_approved = IncidentGeneral.objects.filter(
        status=2)
    incidentReports = IncidentGeneral.objects.all()
    incident_general = IncidentGeneral.objects.filter(status='2')
    incident_vehicle = IncidentVehicle.objects.filter(
        incident_general__status='2')
    user_report = IncidentGeneral.objects.filter(status='2')
    if fromdate:
        incident_general = incident_general.filter(
            date__gte=fromdate)
        incident_vehicle = incident_vehicle.filter(
            incident_general__date__gte=fromdate)
    if todate:
        incident_general = incident_general.filter(
            user_report__date__lte=todate)
        incident_vehicle = incident_vehicle.filter(
            incident_general__date__gte=fromdate)

    # labels = []
    # data = []

    # queryset = IncidentGeneral.objects.annotate(severity_count=Count('severity'))
    # for severity in queryset:
    #     labels.append(severity.severity)
    #     data.append(severity.severity_count)

    # print(labels)

    queryset = incident_general.exclude(severity=None).values(
        'severity').annotate(severity_count=Count('severity'))

    data = list(queryset.values_list('severity_count', flat=True))
    labels = list(queryset.values_list('severity', flat=True))

    queryset1 = incident_vehicle.exclude(vehicle_type=None).values(
        'vehicle_type').annotate(vehicle_type_count=Count('vehicle_type'))

    data1 = list(queryset1.values_list('vehicle_type_count', flat=True))
    labels1 = list(queryset1.values_list('vehicle_type', flat=True))

    queryset2 = user_report.exclude(date=None).values(
        'date').annotate(status_count=Count('status'))

    data2 = list(queryset2.values_list('status_count', flat=True))
    labels2 = list(queryset2.values_list('date', flat=True))

    print(labels2)
    print(data2)

    df = pd.DataFrame(incident_general.values(
        'latitude', 'longitude'))
    
    # df.fillna(value=np.nan, inplace=True)

    # incident_vehicle = IncidentVehicle.objects.all()
    # incident_vehicle_count = incident_vehicle.count()

    # IncidentVehicle.objects
    # .filter(author=author)                 # Filter by the author
    # .annotate(month=TruncMonth('created')) # Truncate by month and add 'month' to values
    # .values('month')                       # Group By month
    # .annotate(count_id=Count('id'))        # Count the number of articles in the grouping
    # .order_by('-month')[:12]

    # coordenadas = list(IncidentGeneral.objects.values_list('user_report__latitude','user_report__longitude'))[-1]
    map1 = folium.Map(location=[14.676208, 121.043861],
                      zoom_start=12)

    # df = df.dropna(axis=0, subset=['user_report__latitude', 'user_report__longitude', 'accident_factor', 'user_report__date'])
    # mapquestopen

    fg = folium.FeatureGroup(name='Marker Cluster', show=False)
    map1.add_child(fg)

    fg2 = folium.FeatureGroup(name='Heat Map', show=True)
    map1.add_child(fg2)

    plugins.HeatMap(df).add_to(fg2)
    FastMarkerCluster(data=df.values.tolist()).add_to(fg)
    # marker_cluster = MarkerCluster().add_to(fg)
    folium.TileLayer(('openstreetmap'), attr='openstreetmap').add_to(map1)
    # folium.TileLayer('mapquestopen', attr='mapquestopen').add_to(map1)
    # folium.TileLayer('MapQuest Open Aerial', attr='MapQuest Open Aerial').add_to(map1)
    folium.TileLayer('cartodbpositron', attr='cartodbpositron').add_to(map1)
    folium.TileLayer('cartodbdark_matter',
                     attr='cartodbdark_matter').add_to(map1)
    plugins.Fullscreen(position='topright').add_to(map1)
    folium.LayerControl().add_to(map1)

    plugins.HeatMap(df).add_to(fg2)

    map2 = folium.Map(location=[14.676208, 121.043861],
                      zoom_start=12, zoom_control=False,
                      scrollWheelZoom=False,
                      dragging=False)
    folium.TileLayer(('openstreetmap'), attr='openstreetmap').add_to(map2)
    # folium.TileLayer('mapquestopen', attr='mapquestopen').add_to(map1)
    # folium.TileLayer('MapQuest Open Aerial', attr='MapQuest Open Aerial').add_to(map1)
    folium.TileLayer('cartodbpositron', attr='cartodbpositron').add_to(map2)
    folium.TileLayer('cartodbdark_matter',
                     attr='cartodbdark_matter').add_to(map2)
    plugins.Fullscreen(position='topright').add_to(map2)
    folium.LayerControl().add_to(map2)

    for id, row in df.iterrows():
        folium.CircleMarker(location=[row['latitude'],
                            row['longitude']], radius=2, fill=True).add_to(map2)

    map1 = map1._repr_html_()
    map2 = map2._repr_html_()
    context = {
        'map1': map1,
        'map2': map2,
        'labels': labels,
        'data': data,
        'labels1': labels1,
        'data1': data1,
        'labels2': labels2,
        'data2': data2,
        'incidentReports_pending': incidentReports_pending,
        "incidentReports": incidentReports,
        'incidentReports_approved': incidentReports_approved,
        'incidentReports_today': incidentReports_today
    }
    return render(request, 'pages/a_Dashboard.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(check_role_super)
def superadmin_dashboard(request):
    fromdate = request.POST.get('fromdate')
    todate = request.POST.get('todate')
    incidentReports_pending = IncidentGeneral.objects.filter(
        status=1)
    today = datetime.today().date()
    incidentReports_today = IncidentGeneral.objects.filter(
        date=today)
    incidentReports_approved = IncidentGeneral.objects.filter(
        status=2)
    incidentReports = IncidentGeneral.objects.all()
    incident_general = IncidentGeneral.objects.filter(status='2')
    incident_vehicle = IncidentVehicle.objects.filter(
        incident_general__status='2')
    user_report = IncidentGeneral.objects.filter(status='2')
    if fromdate:
        incident_general = incident_general.filter(
            date__gte=fromdate)
        incident_vehicle = incident_vehicle.filter(
            incident_general__date__gte=fromdate)
    if todate:
        incident_general = incident_general.filter(
            date__lte=todate)
        incident_vehicle = incident_vehicle.filter(
            incident_general__date__gte=todate)

    # labels = []
    # data = []

    # queryset = IncidentGeneral.objects.annotate(severity_count=Count('severity'))
    # for severity in queryset:
    #     labels.append(severity.severity)
    #     data.append(severity.severity_count)

    # print(labels)

    queryset = incident_general.exclude(severity=None).values(
        'severity').annotate(severity_count=Count('severity'))

    data = list(queryset.values_list('severity_count', flat=True))
    labels = list(queryset.values_list('severity', flat=True))

    queryset1 = incident_vehicle.exclude(vehicle_type=None).values(
        'vehicle_type').annotate(vehicle_type_count=Count('vehicle_type'))

    data1 = list(queryset1.values_list('vehicle_type_count', flat=True))
    labels1 = list(queryset1.values_list('vehicle_type', flat=True))

    queryset2 = user_report.exclude(date=None).values(
        'date').annotate(status_count=Count('status'))

    data2 = list(queryset2.values_list('status_count', flat=True))
    labels2 = list(queryset2.values_list('date', flat=True))

    print(labels2)
    print(data2)

    df = pd.DataFrame(incident_general.values(
        'latitude', 'longitude'))
    

    # incident_vehicle = IncidentVehicle.objects.all()
    # incident_vehicle_count = incident_vehicle.count()

    # IncidentVehicle.objects
    # .filter(author=author)                 # Filter by the author
    # .annotate(month=TruncMonth('created')) # Truncate by month and add 'month' to values
    # .values('month')                       # Group By month
    # .annotate(count_id=Count('id'))        # Count the number of articles in the grouping
    # .order_by('-month')[:12]

    # coordenadas = list(IncidentGeneral.objects.values_list('user_report__latitude','user_report__longitude'))[-1]
    map1 = folium.Map(location=[14.676208, 121.043861],
                      zoom_start=12)

    # df = df.dropna(axis=0, subset=['user_report__latitude', 'user_report__longitude', 'accident_factor', 'user_report__date'])
    # mapquestopen

    fg = folium.FeatureGroup(name='Marker Cluster', show=False)
    map1.add_child(fg)

    fg2 = folium.FeatureGroup(name='Heat Map', show=True)
    map1.add_child(fg2)

    plugins.HeatMap(df).add_to(fg2)
    FastMarkerCluster(data=df.values.tolist()).add_to(fg)
    # marker_cluster = MarkerCluster().add_to(fg)
    folium.TileLayer(('openstreetmap'), attr='openstreetmap').add_to(map1)
    # folium.TileLayer('mapquestopen', attr='mapquestopen').add_to(map1)
    # folium.TileLayer('MapQuest Open Aerial', attr='MapQuest Open Aerial').add_to(map1)
    folium.TileLayer('cartodbpositron', attr='cartodbpositron').add_to(map1)
    folium.TileLayer('cartodbdark_matter',
                     attr='cartodbdark_matter').add_to(map1)
    plugins.Fullscreen(position='topright').add_to(map1)
    folium.LayerControl().add_to(map1)

    plugins.HeatMap(df).add_to(fg2)

    map2 = folium.Map(location=[14.676208, 121.043861],
                      zoom_start=12, zoom_control=False,
                      scrollWheelZoom=False,
                      dragging=False)
    folium.TileLayer(('openstreetmap'), attr='openstreetmap').add_to(map2)
    # folium.TileLayer('mapquestopen', attr='mapquestopen').add_to(map1)
    # folium.TileLayer('MapQuest Open Aerial', attr='MapQuest Open Aerial').add_to(map1)
    folium.TileLayer('cartodbpositron', attr='cartodbpositron').add_to(map2)
    folium.TileLayer('cartodbdark_matter',
                     attr='cartodbdark_matter').add_to(map2)
    plugins.Fullscreen(position='topright').add_to(map2)
    folium.LayerControl().add_to(map2)

    for id, row in df.iterrows():
        folium.CircleMarker(location=[row['latitude'],
                            row['longitude']], radius=2, fill=True).add_to(map2)

    map1 = map1._repr_html_()
    map2 = map2._repr_html_()
    context = {
        'map1': map1,
        'map2': map2,
        'labels': labels,
        'data': data,
        'labels1': labels1,
        'data1': data1,
        'labels2': labels2,
        'data2': data2,
        'incidentReports_pending': incidentReports_pending,
        "incidentReports": incidentReports,
        'incidentReports_approved': incidentReports_approved,
        'incidentReports_today': incidentReports_today
    }
    return render(request, 'pages/sa_Dashboard.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(check_role_super_admin)
def index_map(request):
    fromdate = request.POST.get('fromdate')
    todate = request.POST.get('todate')
    incident_general = IncidentGeneral.objects.filter(status='2')
    if fromdate:
        incident_general = incident_general.filter(
            date__gte=fromdate)
    if todate:
        incident_general = incident_general.filter(
            date__lte=todate)

    df = pd.DataFrame(incident_general.values('address', 'latitude',
                      'longitude', 'accident_factor__category', 'collision_type__category',))
    print(fromdate)

    # coordenadas = list(IncidentGeneral.objects.values_list('user_report__latitude','user_report__longitude'))[-1]
    map1 = folium.Map(location=[14.676208, 121.043861], zoom_start=12, )

    # df = df.dropna(axis=0, subset=['user_report__latitude', 'user_report__longitude', 'accident_factor', 'user_report__date'])
    # mapquestopen

    fg3 = folium.FeatureGroup(name='Map with Markers', show=True)
    map1.add_child(fg3)

    # marker_cluster = MarkerCluster().add_to(fg)
    folium.TileLayer(('openstreetmap'), attr='openstreetmap').add_to(map1)
    # folium.TileLayer('mapquestopen', attr='mapquestopen').add_to(map1)
    # folium.TileLayer('MapQuest Open Aerial', attr='MapQuest Open Aerial').add_to(map1)
    folium.TileLayer('cartodbpositron', attr='cartodbpositron').add_to(map1)
    folium.TileLayer('cartodbdark_matter',
                     attr='cartodbdark_matter').add_to(map1)
    plugins.Fullscreen(position='topright').add_to(map1)
    folium.LayerControl().add_to(map1)

    for id, row in df.iterrows():

        html = '<strong>' + 'Address: ' + '</strong>' + str(row['address']) + ' <br>' + '<strong>' + 'Latitude: ' + '</strong>' + str(row['latitude']) + ' <br>' + \
            '<strong>' + 'Longitude: ' + '</strong>' + \
            str(row['longitude']) 
            # + '<br>' + '<strong>' + 'Accident Factor: ' + \
            # '</strong>' + str(row['accident_factor__category']) + '<br>' + '<strong>' + 'Accident Factor Sub Category: ' + '</strong>'+ str(row['accident_subcategory__sub_category'])+ '<br>' + \
            # '<strong>' + 'Collision Type: ' + '</strong>'+ str(row['collision_type__category'])+ '<br>' + \
            # '<strong>' + 'Collision Type Sub Category: ' + '</strong>'+ str(row['collision_subcategory__sub_category'])+ '<br>'

        iframe = folium.IFrame(html,
                               width=300,
                               height=100)

        popup = folium.Popup(iframe,
                             max_width=300)
        folium.Marker(location=[row['latitude'], row['longitude']], icon=folium.Icon(
            icon="car", prefix='fa'), popup=popup).add_to(fg3)
        # folium.Marker(coordenadas).add_to(map1)

        # df['user_report__date'] = df['user_report__date'].sort_values(ascending=True)
        # data = []
        # for _, d in df.groupby('user_report__date'):
        #     data.append([[row['user_report__latitude'], row['user_report__longitude'], row['accident_factor']] for _, row in d.iterrows()])

    map1 = map1._repr_html_()

    context = {
        'map1': map1
    }
    return render(request, 'pages/sa_Dashboard_map.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(check_role_admin)
def index_map_admin(request):
    fromdate = request.POST.get('fromdate')
    todate = request.POST.get('todate')
    incident_general = IncidentGeneral.objects.filter(user_report__status='2')
    if fromdate:
        incident_general = incident_general.filter(
            user_report__date__gte=fromdate)
    if todate:
        incident_general = incident_general.filter(
            user_report__date__lte=todate)

    df = pd.DataFrame(incident_general.values('user_report__address', 'user_report__latitude',
                      'user_report__longitude', 'accident_factor__category', 'accident_subcategory__sub_category', 'collision_type__category', 'collision_subcategory__sub_category'))
    print(fromdate)

    # coordenadas = list(IncidentGeneral.objects.values_list('user_report__latitude','user_report__longitude'))[-1]
    map1 = folium.Map(location=[14.676208, 121.043861], zoom_start=12, )

    # df = df.dropna(axis=0, subset=['user_report__latitude', 'user_report__longitude', 'accident_factor', 'user_report__date'])
    # mapquestopen

    fg3 = folium.FeatureGroup(name='Map with Markers', show=True)
    map1.add_child(fg3)

    # marker_cluster = MarkerCluster().add_to(fg)
    folium.TileLayer(('openstreetmap'), attr='openstreetmap').add_to(map1)
    # folium.TileLayer('mapquestopen', attr='mapquestopen').add_to(map1)
    # folium.TileLayer('MapQuest Open Aerial', attr='MapQuest Open Aerial').add_to(map1)
    folium.TileLayer('cartodbpositron', attr='cartodbpositron').add_to(map1)
    folium.TileLayer('cartodbdark_matter',
                     attr='cartodbdark_matter').add_to(map1)
    plugins.Fullscreen(position='topright').add_to(map1)
    folium.LayerControl().add_to(map1)

    for id, row in df.iterrows():

        html = '<strong>' + 'Address: ' + '</strong>' + str(row['user_report__address']) + ' <br>' + '<strong>' + 'Latitude: ' + '</strong>' + str(row['user_report__latitude']) + ' <br>' + \
            '<strong>' + 'Longitude: ' + '</strong>' + \
            str(row['user_report__longitude']) + '<br>' + '<strong>' + 'Accident Factor: ' + \
            '</strong>' + str(row['accident_factor__category']) + '<br>' + '<strong>' + 'Accident Factor Sub Category: ' + '</strong>'+ str(row['accident_subcategory__sub_category'])+ '<br>' + \
            '<strong>' + 'Collision Type: ' + '</strong>'+ str(row['collision_type__category'])+ '<br>' + \
            '<strong>' + 'Collision Type Sub Category: ' + '</strong>'+ str(row['collision_subcategory__sub_category'])+ '<br>'

        iframe = folium.IFrame(html,
                               width=300,
                               height=200)

        popup = folium.Popup(iframe,
                             max_width=300)
        folium.Marker(location=[row['user_report__latitude'], row['user_report__longitude']], icon=folium.Icon(
            icon="car", prefix='fa'), popup=popup).add_to(fg3)
        # folium.Marker(coordenadas).add_to(map1)

        # df['user_report__date'] = df['user_report__date'].sort_values(ascending=True)
        # data = []
        # for _, d in df.groupby('user_report__date'):
        #     data.append([[row['user_report__latitude'], row['user_report__longitude'], row['accident_factor']] for _, row in d.iterrows()])

    map1 = map1._repr_html_()

    context = {
        'map1': map1
    }
    return render(request, 'pages/a_Dashboard_map.html', context)

# @login_required(login_url = 'login')
# @user_passes_test(check_role_super)
# def superadmin_dashboard_export(request):
#     products = IncidentGeneral.objects.all()

#     template_path = 'pages/sa_Dashboard.html'

#     context = {'products': products}

#     template = get_template(template_path)

#     html = template.render(context)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

#     response = HttpResponse(pdf, content_type='application/pdf')

#     response['Content-Disposition'] = 'filename="products_report.pdf"'

#     # create a pdf
#     # pisa_status = pisa.CreatePDF(
#     #    html, dest=response)
#     # if error then show some funy view
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return response

# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         data = {
#         "name": "Mama", #you can feach the data from database
#         "id": 18,
#         "amount": 333,
#         }
#         pdf = render_to_pdf('pages/sa_Dashboard.html',data)
#         if pdf:
#             response=HttpResponse(pdf,content_type='application/pdf')
#             filename = "Report_for_%s.pdf" %(data['id'])
#             content = "inline; filename= %s" %(filename)
#             response['Content-Disposition']=content
#             return response
#         return HttpResponse("Page Not Found")
