from django.shortcuts import render, HttpResponse
from django.core.mail import send_mail

from django.conf import settings


def send_email(request):
    a = send_mail(
        'ssssssssssssssssssssssssssssssssss',
        'ssssssssssssssssssssssssssssssssss',
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER, ],
    )

    return HttpResponse('asd')
