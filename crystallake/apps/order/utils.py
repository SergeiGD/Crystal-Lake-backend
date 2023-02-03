from datetime import datetime

from django.http import HttpResponse
from django.utils import timezone

from ..core.utils import ResponseMessage, RelocateResponseMixin
from django.conf import settings
from .models import Purchase


class RoomPurchaseMixin(RelocateResponseMixin):
    def aware_date(self, date_start, date_end):
        return datetime.combine(date_start, settings.CHECK_IN_TIME), datetime.combine(date_end, settings.CHECK_IN_TIME)

    def manage_room_purchase(self, room_purchase, start, end, multiple_rooms_acceptable, success_url=None):
        if not room_purchase.is_editable():
            response_message = ResponseMessage(
                status=ResponseMessage.STATUSES.ERROR,
                message={'Статус': ['Эту покупку нельзя изменить']}
            )
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response
        rooms = room_purchase.offer.pick_rooms_for_purchase(start, end, room_purchase.pk)
        if len(rooms) == 0:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                'Свободность номера': ['Нету свободных комнат на выбранные даты']
            })
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response

        if len(rooms) > 1 and not multiple_rooms_acceptable:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.INFO, message={
                'Свободность номера': ['Нету комнаты на эти даты. Вы можете выбрать опцию подбора нескольких комнат']
            })
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response

        purchases = []
        for room in rooms:
            purchase = Purchase(
                order=room_purchase.order,
                offer=room['room'],
                start=room['start'],
                end=room['end']
            )
            purchases.append(purchase)
        if room_purchase.pk:
            room_purchase.delete()
        Purchase.objects.bulk_create(purchases)
        if success_url:
            return self.relocate(success_url)
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
        response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
        return response


class ServicePurchaseMixin(RelocateResponseMixin):
    def aware_time(self, day, time_start, time_end):
        start = datetime.combine(day, time_start)
        end = datetime.combine(day, time_end)
        return timezone.make_aware(start), timezone.make_aware(end)

    def manage_service_purchase(self, service_purchase, success_url=None):
        if not service_purchase.is_editable():
            response_message = ResponseMessage(
                status=ResponseMessage.STATUSES.ERROR,
                message={'Статус': ['Эту покупку нельзя изменить']}
            )
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response
        if service_purchase.offer.is_time_available(service_purchase.start, service_purchase.end, service_purchase.pk):
            service_purchase.save()
        else:
            response_message = ResponseMessage(
                status=ResponseMessage.STATUSES.ERROR,
                message={'Время': ['На выбранное время нет доступной брони']}
            )
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response

        if success_url:
            return self.relocate(success_url)
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
        response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
        return response
