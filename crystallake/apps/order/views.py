from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView
from django.utils import timezone

from .models import Order
from ..core.utils import SafePaginator, RelocateResponseMixin, ResponseMessage, parse_datetime
from .forms import CreateOrderForm, EditOrderForm, RoomPurchaseForm, ServicePurchaseForm
from ..client.models import Client
from ..user.forms import SearchUserForm
from .status_choises import get_status_by_name
from ..room.forms import SearchRoomsAdmin
from ..offer.models import Offer
from .models import Purchase, PurchaseCountable
from ..service.forms import SearchServicesAdmin, SearchTimetablesAdmin
from ..service.models import ServiceTimetable


# Create your views here.


class AdminOrdersList(ListView):
    model = Order
    template_name = 'order/admin_orders.html'
    context_object_name = 'orders'
    paginate_by = 10
    paginator_class = SafePaginator

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'orders'
        return context


class AdminOrderCreate(RelocateResponseMixin, CreateView):
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


class AdminOrderUpdate(RelocateResponseMixin, UpdateView):
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
        context['form_room_purchase'] = RoomPurchaseForm()
        context['form_service_purchase'] = ServicePurchaseForm()
        context['form_timetables'] = SearchTimetablesAdmin()
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        status = form.cleaned_data['status']
        if status != get_status_by_name(form.cleaned_data['status']):
            if status == 'canceled':
                form.instance.mark_as_canceled()
            if status == 'finished':
                form.instance.mark_as_finished()
            if status == 'in process':
                form.instance.mark_as_in_process()

        # paid = form.cleaned_data['paid']
        # if paid and self.object.date_full_paid is None:
        #     self.object.mark_as_paid()
        # elif not paid and self.object.date_full_paid is not None:
        #     self.object.mark_as_unpaid()

        prepayment_paid = form.cleaned_data['prepayment_paid']
        if prepayment_paid:
            self.object.mark_as_prepayment_paid()

        paid = form.cleaned_data['paid']
        if paid:
            self.object.mark_as_paid()

        refund_made = form.cleaned_data['refund_made']
        if refund_made:
            self.object.mark_as_refund_made()

        form.instance.save()

        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=form.instance.get_admin_edit_url())
        response = HttpResponse(response_message.get_json(), status=302, content_type='application/json')
        return response


def room_purchase_manage_view(request, order_id):
    if request.POST:
        order = get_object_or_404(Order, pk=order_id)
        purchase_id = request.POST['purchase_id'] if request.POST['purchase_id'] else -1
        purchase = Purchase.objects.filter(pk=purchase_id).first()

        form = RoomPurchaseForm(request.POST or None, instance=purchase)    # ???????? purchase_id ???? ??????????????, ???? ?????????? None -> ?????????? ????????????
        if form.is_valid():
            purchase = form.instance
            if not purchase.pk:
                room_id = form.cleaned_data['room_id']
                offer = get_object_or_404(Offer, pk=room_id)
                purchase.offer = offer
                purchase.order = order
            purchase.save()
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
            response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
            return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


def service_purchase_manage_view(request, order_id):
    if request.POST:

        order = get_object_or_404(Order, pk=order_id)
        purchase_id = request.POST['purchase_id'] if request.POST['purchase_id'] else -1
        purchase = PurchaseCountable.objects.filter(pk=purchase_id).first()

        form = ServicePurchaseForm(request.POST or None, instance=purchase)    # ???????? purchase_id ???? ??????????????, ???? ?????????? None -> ?????????? ????????????
        if form.is_valid():
            purchase = form.instance
            if not purchase.pk:
                service_id = form.cleaned_data['service_id']
                offer = get_object_or_404(Offer, pk=service_id)
                purchase.offer = offer
                purchase.order = order

            date_str = request.POST.get('day')
            start_time_str = request.POST.get('time_start')
            end_time_str = request.POST.get('time_end')
            start, end = parse_datetime(date_str, start_time_str, end_time_str)

            purchase.start, purchase.end = start, end
            purchase.save()

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


