from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_member, check_role_super
from accounts.models import UserProfile, User
from .models import Message
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

from accounts.utils import send_verfication_email, send_sms, detectUser, send_verfication_email_inbox
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
# @login_required(login_url='login')
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def sent_message(request):
#     profile = get_object_or_404(UserProfile, user=request.user)
#     if request.method == 'POST':
#         form = SentMessage(request.POST or None, request.FILES or None)
#         try:
#             if form.is_valid():
#                 form.user = request.user
#                 to_email = request.POST.get('to_email')
#                 subject = request.POST.get('subject')
#                 message = request.POST.get('message')
                
#                 if User.objects.filter(email = to_email).exists():
#                     user_from = User.objects.get(email__exact=request.user.email)
#                     user = User.objects.get(email__exact=to_email)
                    
#                 # to_email = form.cleaned_data['to_email']
#                 # subject = form.cleaned_data['subject']
#                 # message = form.cleaned_data['message']

#                     sent_email_message = Sent(user=request.user, to_email=to_email, subject=subject, message=message)
#                     sent_email_message.save()
                    
#                     mail_subject = str(request.user) + ' just sent you a message in Signos Trapiko'
#                     email_template = 'emails/notification_receive.html'
#                     send_verfication_email_inbox(request, user, mail_subject, email_template, user_from)
                    
#                     messages.success(request, 'Message sent successfully')
                    
                
#                 else:
#                     messages.warning(request, 'Email does not exists in the system')
            
#                 # # send verification email
#                 # mail_subject = 'Please Activate Your Account'
#                 # email_template = 'emails/account_verification_email.html'
#                 # send_verfication_email(request, user, mail_subject, email_template)
#                 # messages.success(request, 'You have signed up successfully! Please check your email to verify your account.')
#                 # print(user.password)
#                 return redirect('sent_message')
#             else:
#                 print(form.errors)
#                 print(form.non_field_errors)
#         except Exception as e:
#             print('invalid form')
#             messages.error(request, str(e))


#     else:
#         form = SentMessage()
#     context = {
#         'form' : form,
#     }
#     return render(request, 'pages/inbox/sent_message.html', context)

# @login_required(login_url='login')
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def a_sent_message(request):
#     profile = get_object_or_404(UserProfile, user=request.user)
#     if request.method == 'POST':
#         form = SentMessage(request.POST or None, request.FILES or None)
#         try:
#             if form.is_valid():
#                 form.user = request.user
#                 to_email = request.POST.get('to_email')
#                 subject = request.POST.get('subject')
#                 message = request.POST.get('message')
                
#                 if User.objects.filter(email = to_email).exists():
#                     user_from = User.objects.get(email__exact=request.user.email)
#                     user = User.objects.get(email__exact=to_email)
                    
#                 # to_email = form.cleaned_data['to_email']
#                 # subject = form.cleaned_data['subject']
#                 # message = form.cleaned_data['message']

#                     sent_email_message = Sent(user=request.user, to_email=to_email, subject=subject, message=message)
#                     sent_email_message.save()
                    
#                     mail_subject = str(request.user) + ' just sent you a message in Signos Trapiko'
#                     email_template = 'emails/notification_receive.html'
#                     send_verfication_email_inbox(request, user, mail_subject, email_template, user_from)
                    
#                     messages.success(request, 'Message sent successfully')
                    
                
#                 else:
#                     messages.warning(request, 'Email does not exists in the system')
            
#                 # # send verification email
#                 # mail_subject = 'Please Activate Your Account'
#                 # email_template = 'emails/account_verification_email.html'
#                 # send_verfication_email(request, user, mail_subject, email_template)
#                 # messages.success(request, 'You have signed up successfully! Please check your email to verify your account.')
#                 # print(user.password)
#                 return redirect('sent_message')
#             else:
#                 print(form.errors)
#                 print(form.non_field_errors)
#         except Exception as e:
#             print('invalid form')
#             messages.error(request, str(e))


#     else:
#         form = SentMessage()
#     context = {
#         'form' : form,
#     }
#     return render(request, 'pages/inbox/a_sent_message.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def inbox(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_user = None
    directs = None
    if messages:
        message = messages[0]
        active_user = message['user'].username
        directs = Message.objects.filter(user=user, recipient=message['user'])
        directs.update(is_read=True)
        
        for message in messages:
            if message['user'].username == active_user:
                message['unread'] = 0
    
    context = {
		'directs': directs,
		'messages': messages,
		'active_user': active_user,
		}
    
    template = loader.get_template('pages/inbox/inbox_message.html')
    
    return HttpResponse(template.render(context, request))
    
    # return render(request, 'pages/inbox/inbox_message.html', context)

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def a_inbox(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_user = None
    directs = None
    if messages:
        message = messages[0]
        active_user = message['user'].username
        directs = Message.objects.filter(user=user, recipient=message['user'])
        directs.update(is_read=True)
        
        for message in messages:
            if message['user'].username == active_user:
                message['unread'] = 0
    
    context = {
		'directs': directs,
		'messages': messages,
		'active_user': active_user,
		}
    
    template = loader.get_template('pages/inbox/a_inbox_message.html')
    
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def m_inbox(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_user = None
    directs = None
    if messages:
        message = messages[0]
        active_user = message['user'].username
        directs = Message.objects.filter(user=user, recipient=message['user'])
        directs.update(is_read=True)
        
        for message in messages:
            if message['user'].username == active_user:
                message['unread'] = 0
    
    context = {
		'directs': directs,
		'messages': messages,
		'active_user': active_user,
		}
    
    template = loader.get_template('pages/inbox/m_inbox_message.html')
    
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_search(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query))

		#Pagination
		paginator = Paginator(users, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'users': users_paginator,
			}
	
	template = loader.get_template('pages/inbox/sent_message.html')
	
	return HttpResponse(template.render(context, request))

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def a_user_search(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query))

		#Pagination
		paginator = Paginator(users, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'users': users_paginator,
			}
	
	template = loader.get_template('pages/inbox/a_sent_message.html')
	
	return HttpResponse(template.render(context, request))

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def m_user_search(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query))

		#Pagination
		paginator = Paginator(users, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'users': users_paginator,
			}
	
	template = loader.get_template('pages/inbox/m_sent_message.html')
	
	return HttpResponse(template.render(context, request))



@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Directs(request, username):
	user = request.user
	messages = Message.get_messages(user=user)
	active_user = username
	directs = Message.objects.filter(user=user, recipient__username=username)
	directs.update(is_read=True)
	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_user':active_user,
	}

	template = loader.get_template('pages/inbox/inbox_message.html')

	return HttpResponse(template.render(context, request))


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def a_Directs(request, username):
	user = request.user
	messages = Message.get_messages(user=user)
	active_user = username
	directs = Message.objects.filter(user=user, recipient__username=username)
	directs.update(is_read=True)
	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_user':active_user,
	}

	template = loader.get_template('pages/inbox/a_inbox_message.html')
	return HttpResponse(template.render(context, request))

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def m_Directs(request, username):
	user = request.user
	messages = Message.get_messages(user=user)
	active_user = username
	directs = Message.objects.filter(user=user, recipient__username=username)
	directs.update(is_read=True)
	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_user':active_user,
	}

	template = loader.get_template('pages/inbox/m_inbox_message.html')
	return HttpResponse(template.render(context, request))


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def new_message(request, username):
	from_user = request.user
	body = ''
	try:
		to_user = User.objects.get(username=username)
	except Exception as e:
		return redirect('user_search')
	if from_user != to_user:
		Message.send_message(from_user, to_user, body)
	return redirect('inbox')

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def a_new_message(request, username):
	from_user = request.user
	body = ''
	try:
		to_user = User.objects.get(username=username)
	except Exception as e:
		return redirect('a_user_search')
	if from_user != to_user:
		Message.send_message(from_user, to_user, body)
	return redirect('a_inbox')

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def m_new_message(request, username):
	from_user = request.user
	body = ''
	try:
		to_user = User.objects.get(username=username)
	except Exception as e:
		return redirect('m_user_search')
	if from_user != to_user:
		Message.send_message(from_user, to_user, body)
	return redirect('m_inbox')

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def send_direct(request):
	from_user = request.user
	to_user_username = request.POST.get('to_user')
	body = request.POST.get('body')
	
	if request.method == 'POST':
		to_user = User.objects.get(username=to_user_username)
		Message.send_message(from_user, to_user, body)
		return redirect('inbox')
	else:
		HttpResponseBadRequest()

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def a_send_direct(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')
    
    if request.method == 'POST':
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect('a_inbox')
    else:
        HttpResponseBadRequest()

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def m_send_direct(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')
    
    if request.method == 'POST':
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect('m_inbox')
    else:
        HttpResponseBadRequest()

def check_inbox(request):
	directs_count = 0
	if request.user.is_authenticated:
		directs_count = Message.objects.filter(user=request.user, is_read=False).count()

	return {'directs_count':directs_count}