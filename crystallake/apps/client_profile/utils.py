from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.utils import timezone

from ..user.models import SmsCode
from ..core.utils import ResponseMessage

from django.conf import settings


class SmsCodeMixin:
    def find_sms_code(self, code):
        code = make_password(code, salt=settings.SMS_CODE_SALT)
        min_date = datetime.now() - settings.CODE_ACTIVE_TIME
        return SmsCode.objects.exclude(date__lt=timezone.make_aware(min_date)).filter(
            code=code,
            is_used=False
        ).order_by('-date').first()

    def get_code_error_message(self):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
            'Ошибка': ['неверный или истекший код']
        })
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def get_unknown_phone_error(self):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
            'Ошибка': 'Не найден пользователь, отправивший запрос'
        })
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response


# class PasswordsMixin:
#     def post(self):
