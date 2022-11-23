from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile, User
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_super
from django.contrib import messages
from accounts.forms import UserForm, MemberForm, UserManagementForm, UserUpdateManagementForm, UserUpdateForm, ProfileMgmtUpdateForm, UserManagementForm1, ProfileMgmtUpdateFormEdit, ProfileMgmtUpdateFormEdit_1
from accounts.utils import send_verfication_email, send_sms, detectUser
from django.urls import reverse
from django.core.paginator import Paginator
from incidentreport.models import IncidentGeneral
from notifications.models import Notification

# Create your views here.

# Create your views here.
@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(user=request.user).order_by('-created_at')
    incidentReports_top = IncidentGeneral.objects.filter(user=request.user).order_by('-created_at')[:4]
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
        'incidentReports_top': incidentReports_top,
    }
    return render(request, 'pages/super/super_profile.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_profile_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(status=1, user=request.user).order_by('-created_at')
    incidentReports_top = IncidentGeneral.objects.filter(user=request.user)[:4]
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
        'incidentReports_top': incidentReports_top,
    }
    return render(request, 'pages/super/super_profile.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_profile_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(status=2, user=request.user).order_by('-created_at')
    incidentReports_top = IncidentGeneral.objects.filter(user=request.user)[:4]
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
        'incidentReports_top': incidentReports_top,
    }
    return render(request, 'pages/super/super_profile.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_profile_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(status=3, user=request.user).order_by('-created_at')
    incidentReports_top = IncidentGeneral.objects.filter(user=request.user)[:4]
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
        'incidentReports_top': incidentReports_top,
    }
    return render(request, 'pages/super/super_profile.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_profile_edit(request):
    user = User.objects.get(username = request.user.username)
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form = ProfileMgmtUpdateFormEdit_1(request.POST  or None, request.FILES  or None, instance=profile)
        user_form = UserUpdateForm(request.POST  or None, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.instance.username = request.user
            # user.first_name = user_form.cleaned_data['first_name']
            # user.middle_name = user_form.cleaned_data['middle_name']
            # user.last_name = user_form.cleaned_data['last_name']
            # user.username = user_form.cleaned_data['username']
            # user.email = user_form.cleaned_data['email']
            # user.mobile_number = user_form.cleaned_data['mobile_number']
            # my_form = user_form.save(commit=False)
            # my_form.username = request.user.username
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated')
            return redirect('super_profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)

    else:
        profile_form = ProfileMgmtUpdateFormEdit_1(instance=profile)
        user_form = UserUpdateForm(instance=request.user, initial={"email": user.email, 
                                                        "username": user.username})
    context = {
        'profile_form': profile_form,
        'user_form' : user_form,
        'profile': profile,
    }
    
    return render(request, 'pages/super/super_profile_edit.html', context)


@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_account(request):
    form = UserManagementForm(request.POST)
    m_form = MemberForm(request.POST, request.FILES)
    user = User.objects.filter(is_deleted=False).order_by('-last_login')
    paginator = Paginator(user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in user:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = User.objects.get(id=i.id)
                b.status = 2
                b.is_active = 'False'
                b.soft_delete()
            messages.success(request, 'User successfully deleted')
    context = {
        'form': form,
        'user': user,
        'page_obj':page_obj
    }
    print(context)
    return render(request, 'pages/super/super_user_account.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_account_member(request):
    user = User.objects.filter(role = 1, is_deleted=False).order_by('-last_login')
    form = UserManagementForm(request.POST)
    paginator = Paginator(user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in user:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = User.objects.get(id=i.id)
                b.status = 2
                b.is_active = 'False'
                b.soft_delete()
            messages.success(request, 'User successfully deleted')
    context = {
        'form': form,
        'user': user,
        'page_obj':page_obj
    }
    print(context)
    return render(request, 'pages/super/super_user_account.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_account_admin(request):
    user = User.objects.filter(role = 2, is_deleted=False).order_by('-last_login')
    form = UserManagementForm(request.POST)
    paginator = Paginator(user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in user:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = User.objects.get(id=i.id)
                b.status = 2
                b.is_active = 'False'
                b.soft_delete()
            messages.success(request, 'User successfully deleted')
    context = {
        'form': form,
        'user': user,
        'page_obj':page_obj
    }
    print(context)
    return render(request, 'pages/super/super_user_account.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_account_superadmin(request):
    user = User.objects.filter(role = 3, is_deleted=False).order_by('-last_login')
    form = UserManagementForm(request.POST)
    paginator = Paginator(user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in user:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = User.objects.get(id=i.id)
                b.status = 2
                b.is_active = 'False'
                b.soft_delete()
            messages.success(request, 'User successfully deleted')
    context = {
        'form': form,
        'user': user,
        'page_obj':page_obj
    }
    return render(request, 'pages/super/super_user_account.html', context)

def super_user_account_add(request):
    if request.method == 'POST':
        form = UserManagementForm1(request.POST)
        try:
            if form.is_valid():
                
                first_name = form.cleaned_data['first_name']
                middle_name = form.cleaned_data['middle_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                mobile_number = form.cleaned_data['mobile_number']
                password = form.cleaned_data['password']
                role = form.cleaned_data['role']

                user = User(first_name=first_name, middle_name=middle_name, last_name=last_name, username=username, email=email, mobile_number=mobile_number, role=role)
                user.set_password(password)
                user.save()
                
            
                # send verification email
                mail_subject = 'Please Activate Your Account'
                email_template = 'emails/account_verification_email.html'
                send_verfication_email(request, user, mail_subject, email_template)
                messages.success(request, 'You have signed up successfully! Please check your email to verify your account.')
                print(user.password)
                return redirect('super_user_account')
            else:
                print(form.errors)
                print(form.non_field_errors)
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = UserManagementForm1()
    context = {
        'form' : form,
    }
    return render(request, 'pages/super/super_user_account_add.html', context)

def super_user_account_view(request, id):
    user = get_object_or_404(User, pk=id)
    profile = get_object_or_404(UserProfile, pk=user.id)
    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'pages/super/super_user_account_view.html', context) 

def super_user_account_edit(request, id=None):
    user =  get_object_or_404(User, pk=id)
    profile = get_object_or_404(UserProfile, pk=id)
    if request.method == 'POST':
        profile_form = ProfileMgmtUpdateFormEdit(request.POST  or None, request.FILES  or None, instance=profile)
        user_form = UserUpdateManagementForm(request.POST  or None,  instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.instance.username = request.user
            # user.first_name = user_form.cleaned_data['first_name']
            # user.middle_name = user_form.cleaned_data['middle_name']
            # user.last_name = user_form.cleaned_data['last_name']
            # user.username = user_form.cleaned_data['username']
            # user.email = user_form.cleaned_data['email']
            # user.mobile_number = user_form.cleaned_data['mobile_number']
            # my_form = user_form.save(commit=False)
            # my_form.username = request.user.username
            profile_form.save()
            user_form.save(commit=False)
            remarks = "update user account"
            if user.status == 3:
                user.is_active = False
                user.status = User.DEACTIVATED
                user.save()
                text = "updated status to deactive"
                incident_report = None
                sender = profile.user
                notification_report = Notification(incident_report=incident_report, sender=sender, user=request.user, remarks=remarks, notification_type=2, text_preview=text)
                notification_report.save()
                messages.success(request, 'Profile updated')
                messages.success(request, 'Account is Inactive')
                return redirect('super_user_account')
            elif user.status == 2:
                user.is_active = False
                user.soft_delete()
                user.save()
                text = "updated status to deleted"
                incident_report = None
                sender = profile.user
                notification_report = Notification(incident_report=incident_report, sender=sender, user=request.user, remarks=remarks, notification_type=2, text_preview=text)
                notification_report.save()
                messages.success(request, 'Profile updated')
                messages.success(request, 'Account is Deleted')
                return redirect('super_user_account')
            elif user.status == 1:
                user.is_active = True
                user.status = User.ACTIVE
                user.save()
                text = "updated status to active"
                incident_report = None
                sender = profile.user
                notification_report = Notification(incident_report=incident_report, sender=sender, user=request.user, remarks=remarks, notification_type=2, text_preview=text)
                notification_report.save()
                messages.success(request, 'Profile updated')
                messages.success(request, 'Account is Active')
                return redirect('super_user_account')
            else:

                return redirect('super_user_account')
        else:
            print(profile_form.errors)
            print(user_form.errors)

    else:
        profile_form = ProfileMgmtUpdateFormEdit(instance=profile)
        user_form = UserUpdateManagementForm(instance=user, initial={"email": user.email, 
                                                        "username": user.username})
    context = {
        'profile_form': profile_form,
        'user_form' : user_form,
        'profile': profile,
        'user': user
    }
    
    return render(request, 'pages/super/super_user_account_edit.html', context)


@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_account_delete(request, id):
    user = User.objects.get(pk=id)
    if user.role == 1 or user.role == 2:
        user.status = 2
        user.is_active = 'False'
        user.soft_delete()
        messages.success(request, 'User successfully deleted')
        return redirect('super_user_account')
    else:
        messages.error(request, 'Unable to Delete Super Admin')
        return redirect('super_user_account')

@login_required(login_url='login')
@user_passes_test(check_role_super)
def sa_recycle_bin_user(request):
    user = User.objects.filter(is_deleted=True).order_by('-last_login')
    paginator = Paginator(user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        if request.POST.get('Restore') == 'Restore':
            for i in user:
                x = request.POST.get(str(i.id))
                print(x)
                if str(x) == 'on':
                    b = User.objects.get(id=i.id)
                    b.status = 1
                    b.is_active = 'True'
                    b.restore()
                    # b.is_deleted = False
                    # b.deleted_at = None
                    messages.success(request, 'User Report successfully restored')
        elif request.POST.get('Yes') == 'Yes':
            for i in user:
                x = User.POST.get(str(i.id))
                print(x)
                if str(x) == 'on':
                    b = User.objects.get(id=i.id)
                    b.delete()
                    # b.is_deleted = False
                    # b.deleted_at = None
                    messages.success(request, 'User Report successfully restored') 
    context = {
        'user': user,
        'page_obj':page_obj
    }
    return render(request, 'pages/super/sa_recycle_bin_user.html', context)
