import json
import os
from datetime import datetime

from django.contrib.auth.mixins import AccessMixin
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.utils import timezone

from ..client_profile.forms import ClientLoginForm, SendCodeForm, ClientPasswordsForm, ClientPhoneForm
from django.conf import settings


class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                return self.num_pages
            else:
                return 1


class ResponseMessage:
    class STATUSES:
        OK = 'OK'
        ERROR = 'ERROR'
        INFO = 'INFO'

    def __init__(self, status, data=None, message=None):
        self.status = status
        self.data = data
        self.message = message

    def get_json(self):
        return json.dumps(self.__dict__, default=str)


class RelocateResponseMixin:
    def relocate(self, url):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=url)
        response = HttpResponse(response_message.get_json(), status=302, content_type='application/json')
        return response


class ClientContextMixin:
    def get_general_context(self):
        context = {
            'login_form': ClientLoginForm(),
            'register_phone_form': ClientPhoneForm(prefix='register'),
            'register_passwords_form': ClientPasswordsForm(prefix='register'),
            'register_code_form': SendCodeForm(prefix='register'),
            'reset_phone_form': ClientPhoneForm(prefix='reset'),
            'reset_code_form': SendCodeForm(prefix='reset'),
            'reset_passwords_form': ClientPasswordsForm(prefix='reset'),
        }
        return context


def get_paginator_data(data_list, page_number):
    paginator = SafePaginator(data_list, 1)
    data_page = paginator.get_page(page_number)
    num_pages = paginator.num_pages

    return data_page, num_pages


def parse_datetime(day, time_start, time_end):
    start_str = day + '/' + time_start
    end_str = day + '/' + time_end

    start = datetime.strptime(start_str, '%Y-%m-%d/%H:%M')
    end = datetime.strptime(end_str, '%Y-%m-%d/%H:%M')

    start = timezone.make_aware(start)
    end = timezone.make_aware(end)

    return start, end


def is_ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return True
    else:
        return False


def get_image_src(name):
    for image_file in os.listdir(f'{settings.STATIC_ROOT}/images'):
        if name in image_file in image_file:
            return f'images/{image_file}'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
