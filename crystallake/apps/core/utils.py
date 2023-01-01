import json

from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse


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

    def __init__(self, status, data=None, message=None):
        self.status = status
        self.data = data
        self.message = message

    def get_json(self):
        return json.dumps(self.__dict__)


class RelocateResponseMixin:
    def relocate(self, url):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=url)
        response = HttpResponse(response_message.get_json(), status=302, content_type='application/json')
        return response


def get_paginator_data(data_list, page_number):
    paginator = SafePaginator(data_list, 8)
    data_page = paginator.get_page(page_number)
    num_pages = paginator.num_pages

    return data_page, num_pages
