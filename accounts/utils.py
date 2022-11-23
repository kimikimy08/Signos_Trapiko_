from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from twilio.rest import Client

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'member_profile'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'admin_dashboard'
        return redirectUrl
    elif user.role == 3:
        redirectUrl = 'superadmin_dashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl

def send_verfication_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user' : user,
        'domain' : current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user)
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()

def send_verfication_email_inbox(request, user, mail_subject, email_template, user_from):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user' : user,
        'domain' : current_site,
        'user_from': user_from
        # 'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        # 'token' : default_token_generator.make_token(user)
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()

def send_sms(user_code,phone_number):
    account_sid = 'AC544a74e1519b84282c6d22e90d4dbe12'
    auth_token = '058ea780845da159b017ced55f4668de'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body= f'Hi! You user and verification code is {user_code}',
        from_ = '+15702829445',
        to = f'{phone_number}'
    )
    print(message.sid)