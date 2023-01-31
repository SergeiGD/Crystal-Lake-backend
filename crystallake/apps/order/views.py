from datetime import datetime, time

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView, DetailView
from django.utils import timezone
from django.urls import reverse_lazy

from .models import Order
from ..core.utils import SafePaginator, RelocateResponseMixin, ResponseMessage
from ..worker_profile.views import AdminLoginRequired
from .forms import CreateOrderForm, EditOrderForm, RoomPurchaseForm, ServicePurchaseForm
from ..client.models import Client
from ..user.forms import SearchUserForm
from .status_choises import get_status_by_name
from ..room.forms import SearchRoomsAdmin
from ..offer.models import Offer
from .models import Purchase, PurchaseCountable
from ..service.forms import SearchServicesAdmin, SearchTimetablesAdmin
from ..room.models import Room
from .status_choises import Status
from ..service.models import ServiceTimetable
from django.conf import settings


# Create your views here.


class AdminOrdersList(AdminLoginRequired, ListView):
    model = Order
    template_name = 'order/admin_orders.html'
    context_object_name = 'orders'
    paginate_by = 10
    paginator_class = SafePaginator

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'orders'
        return context


class AdminOrderDetail(AdminLoginRequired, DetailView):
    model = Order
    template_name = 'order/admin_show_order.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'orders'
        return context


class AdminOrderCreate(RelocateResponseMixin, AdminLoginRequired, CreateView):
    model = Order
    template_name = 'order/admin_create_order.html'
    context_object_name = 'order'
    form_class = CreateOrderForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'orders'
        context['form_clients'] = SearchUserForm()
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        client_id = form.cleaned_data['client_id']
        client = get_object_or_404(Client, pk=client_id)
        order = form.instance
        order.client = client
        order.save()
        return self.relocate(order.get_admin_edit_url())


class AdminOrderUpdate(RelocateResponseMixin, AdminLoginRequired, UpdateView):
    model = Order
    template_name = 'order/admin_edit_order.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'
    form_class = EditOrderForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminOrderUpdate, self).get_context_data(**kwargs)
        context['current_page'] = 'orders'
        context['form_rooms'] = SearchRoomsAdmin()
        context['form_services'] = SearchServicesAdmin()
        context['form_edit_room_purchase'] = RoomPurchaseForm(prefix='edit')
        context['form_create_room_purchase'] = RoomPurchaseForm(prefix='create')
        context['form_edit_service_purchase'] = ServicePurchaseForm(prefix='edit')
        context['form_create_service_purchase'] = ServicePurchaseForm(prefix='create')
        context['form_timetables'] = SearchTimetablesAdmin()
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        status = form.cleaned_data['status']
        if status != get_status_by_name(form.cleaned_data['status']):
            if status == Status.canceled.name:
                form.instance.mark_as_canceled()
            if status == Status.finished.name:
                form.instance.mark_as_finished()
            if status == Status.process.name:
                form.instance.mark_as_in_process()

        # paid = form.cleaned_data['paid']
        # if paid and self.object.date_full_paid is None:
        #     self.object.mark_as_paid()
        # elif not paid and self.object.date_full_paid is not None:
        #     self.object.mark_as_unpaid()

        # prepayment_paid = form.cleaned_data['prepayment_paid']
        # if prepayment_paid:
        #     self.object.mark_as_prepayment_paid()
        #
        # paid = form.cleaned_data['paid']
        # if paid:
        #     self.object.mark_as_paid()

        refund_made = form.cleaned_data['refund_made']
        if refund_made:
            self.object.mark_as_refund_made()

        form.instance.save()

        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=form.instance.get_admin_show_url())
        response = HttpResponse(response_message.get_json(), status=302, content_type='application/json')
        return response


def room_purchase_edit_view(request, purchase_id, **kwargs):
    if request.POST:
        purchase = get_object_or_404(Purchase, pk=purchase_id)

        form = RoomPurchaseForm(request.POST or None, instance=purchase, prefix='edit')

        if form.is_valid():
            room = purchase.offer.main_room
            rooms = room.pick_rooms_for_purchase(form.cleaned_data['start'], form.cleaned_data['end'], purchase.pk)
            if len(rooms) == 0:
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Свободность номера': ['Нету свободных комнат на выбранные даты']
                })
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response

            if len(rooms) > 1 and not form.cleaned_data['multiple_rooms_acceptable']:
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.INFO, message={
                    'Свободность номера': [
                        'Нету комнаты на эти даты. Вы можете выбрать опцию подбора нескольких комнат']
                })
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response

            purchases = []
            for room in rooms:
                created_purchase = Purchase(
                    order=purchase.order,
                    offer=room['room'],
                    start=room['start'],
                    end=room['end'],
                    is_prepayment_paid=purchase.is_prepayment_paid
                )
                purchases.append(created_purchase)
            purchase.delete()
            Purchase.objects.bulk_create(purchases)
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
            response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
            return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


def room_purchase_create_view(request, order_id):
    if request.POST:
        order = get_object_or_404(Order, pk=order_id)

        form = RoomPurchaseForm(request.POST or None, prefix='create')
        purchase = form.instance
        purchase.order = order

        if form.is_valid():
            room_id = form.cleaned_data['room_id']
            room = get_object_or_404(Room, pk=room_id)
            start = datetime.combine(form.cleaned_data['start'], settings.CHECK_IN_TIME)
            end = datetime.combine(form.cleaned_data['end'], settings.CHECK_IN_TIME)

            rooms = room.pick_rooms_for_purchase(start, end)
            if len(rooms) == 0:
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Свободность номера': ['Нету свободных комнат на выбранные даты']
                })
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response

            if len(rooms) > 1 and not form.cleaned_data['multiple_rooms_acceptable']:
                print(form.cleaned_data)
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.INFO, message={
                    'Свободность номера': ['Нету комнаты на эти даты. Вы можете выбрать опцию подбора нескольких комнат']
                })
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response

            purchases = []
            for room in rooms:
                purchase = Purchase(
                    order=order,
                    offer=room['room'],
                    start=room['start'],
                    end=room['end']
                )
                purchases.append(purchase)
            Purchase.objects.bulk_create(purchases)
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
            response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
            return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


def service_purchase_create_view(request, order_id):
    if request.POST:
        order = get_object_or_404(Order, pk=order_id)
        # print(request.POST)
        # service_id = request.POST['create-service_id']
        # service = get_object_or_404(Offer, pk=service_id)

        # day = datetime(request.POST['create-day'])
        # time_start = datetime.time(request.POST['create-time_start'])
        # time_end = datetime.time(request.POST['create-time_end'])
        # start = datetime.combine(day, time_start)
        # end = datetime.combine(day, time_end)
        # start, end = timezone.make_aware(start), timezone.make_aware(end)

        purchase = PurchaseCountable(order=order)
        form = ServicePurchaseForm(request.POST or None, instance=purchase, prefix='create')

        if form.is_valid():
            service_id = form.cleaned_data['service_id']
            service = get_object_or_404(Offer, pk=service_id)
            purchase.offer = service

            start = datetime.combine(form.cleaned_data['day'], form.cleaned_data['time_start'])
            end = datetime.combine(form.cleaned_data['day'], form.cleaned_data['time_end'])
            start, end = timezone.make_aware(start), timezone.make_aware(end)

            purchase.start, purchase.end = start, end

            if purchase.offer.is_time_available(purchase.start, purchase.end):
                purchase.save()
            else:
                response_message = ResponseMessage(
                    status=ResponseMessage.STATUSES.ERROR,
                    message={'Время': ['На выбранное время нет доступной брони']}
                )
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response

            response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
            response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
            return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


def service_purchase_edit_view(request, purchase_id, **kwargs):
    # TODO: mixin
    if request.POST:
        purchase = get_object_or_404(PurchaseCountable, pk=purchase_id)
        form = ServicePurchaseForm(request.POST or None, instance=purchase, prefix='edit')

        if form.is_valid():
            start = datetime.combine(form.cleaned_data['day'], form.cleaned_data['time_start'])
            end = datetime.combine(form.cleaned_data['day'], form.cleaned_data['time_end'])
            start, end = timezone.make_aware(start), timezone.make_aware(end)

            purchase.start, purchase.end = start, end

            if purchase.offer.is_time_available(purchase.start, purchase.end, purchase.pk):
                purchase.save()
            else:
                response_message = ResponseMessage(
                    status=ResponseMessage.STATUSES.ERROR,
                    message={'Время': ['На выбранное время нет доступной брони']}
                )
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response

            response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
            response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
            return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


def get_purchase_info_view(request, purchase_id, **kwargs):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    data = purchase.get_info()
    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
    response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
    return response


def cancel_purchase_view(request, purchase_id, **kwargs):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    purchase.cancel()
    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
    response = HttpResponse(response_message.get_json(), status=302, content_type='application/json')
    response['Location'] = purchase.order.get_admin_edit_url()
    return response







