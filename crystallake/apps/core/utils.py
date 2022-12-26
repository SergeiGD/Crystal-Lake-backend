import json

from django.core.paginator import Paginator, EmptyPage


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
