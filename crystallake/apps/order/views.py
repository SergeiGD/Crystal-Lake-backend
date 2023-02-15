from datetime import datetime, time

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView, View
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.conf import settings

from .models import Order
from ..core.utils import SafePaginator, RelocateResponseMixin, ResponseMessage
from ..worker_profile.utils import AdminLoginRequired
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
from .utils import ServicePurchaseMixin, RoomPurchaseMixin


# Create your views here.


class AdminOrdersList(PermissionRequiredMixin, AdminLoginRequired, ListView):
    permission_required = 'order.view_order'
    model = Order
    template_name = 'order/admin_orders.html'
    context_object_name = 'orders'
    paginate_by = settings.ADMIN_PAGINATE_BY
    paginator_class = SafePaginator

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'orders'
        return context


class AdminOrderDetail(PermissionRequiredMixin, AdminLoginRequired, DetailView):
    permission_required = 'order.view_order'
    model = Order
    template_name = 'order/admin_show_order.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'orders'
        return context


class AdminOrderCreate(PermissionRequiredMixin, RelocateResponseMixin, AdminLoginRequired, CreateView):
    permission_required = 'order.add_order'
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


class AdminOrderUpdate(PermissionRequiredMixin, RelocateResponseMixin, AdminLoginRequired, UpdateView):
    permission_required = 'order.change_order'
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
        context['form_create_room_purchase'] = RoomPurchaseForm(prefix='create')
        context['form_edit_room_purchase'] = RoomPurchaseForm(prefix='edit_room')
        context['form_edit_service_purchase'] = ServicePurchaseForm(prefix='edit_service')
        context['form_create_service_purchase'] = ServicePurchaseForm(prefix='create')
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

        refund_made = form.cleaned_data['refund_made']
        if refund_made:
            self.object.mark_as_refund_made()

        form.instance.save()

        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=form.instance.get_admin_show_url())
        response = HttpResponse(response_message.get_json(), status=302, content_type='application/json')
        return response


class RoomPurchaseEditView(PermissionRequiredMixin, RoomPurchaseMixin, AdminLoginRequired, View):
    permission_required = 'order.change_order'

    def post(self, request, **kwargs):
        purchase = get_object_or_404(Purchase, pk=request.POST.get('edit_room-purchase_id'))
        form = RoomPurchaseForm(request.POST or None, instance=purchase, prefix='edit_room')

        if form.is_valid():
            purchase.offer = purchase.offer.main_room
            start, end = self.aware_date(form.cleaned_data['start'], form.cleaned_data['end'])

            return self.manage_room_purchase(purchase, start, end, form.cleaned_data['multiple_rooms_acceptable'])
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class RoomPurchaseCreateView(PermissionRequiredMixin, RoomPurchaseMixin, AdminLoginRequired, View):
    permission_required = 'order.change_order'
    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        form = RoomPurchaseForm(request.POST or None, prefix='create', instance=None)
        purchase = form.instance
        purchase.order = order

        if form.is_valid():
            room_id = form.cleaned_data['room_id']
            purchase.offer = get_object_or_404(Room, pk=room_id)
            start, end = self.aware_date(form.cleaned_data['start'], form.cleaned_data['end'])

            return self.manage_room_purchase(purchase, start, end, form.cleaned_data['multiple_rooms_acceptable'])
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class ServicePurchaseEditView(PermissionRequiredMixin, ServicePurchaseMixin, AdminLoginRequired, View):
    permission_required = 'order.change_order'
    def post(self, request, **kwargs):
        purchase = get_object_or_404(PurchaseCountable, pk=request.POST.get('edit_service-purchase_id'))
        form = ServicePurchaseForm(request.POST or None, instance=purchase, prefix='edit_service')

        if form.is_valid():
            purchase.start, purchase.end = self.aware_time(
                form.cleaned_data['day'],
                form.cleaned_data['time_start'],
                form.cleaned_data['time_end']
            )

            return self.manage_service_purchase(purchase)

        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class ServicePurchaseCreateView(PermissionRequiredMixin, ServicePurchaseMixin, AdminLoginRequired, View):
    permission_required = 'order.change_order'
    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        purchase = PurchaseCountable(order=order)
        form = ServicePurchaseForm(request.POST or None, instance=purchase, prefix='create')
        if form.is_valid():
            service_id = form.cleaned_data['service_id']
            service = get_object_or_404(Offer, pk=service_id)
            purchase.offer = service

            purchase.start, purchase.end = self.aware_time(
                form.cleaned_data['day'],
                form.cleaned_data['time_start'],
                form.cleaned_data['time_end']
            )

            return self.manage_service_purchase(purchase)


@permission_required(perm='order.view_order', login_url=reverse_lazy('admin_login'))
@staff_member_required(login_url=reverse_lazy('admin_login'))
def get_purchase_info_view(request, purchase_id, **kwargs):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    data = purchase.get_info()
    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
    response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
    return response


@permission_required(perm='order.change_order', login_url=reverse_lazy('admin_login'))
@staff_member_required(login_url=reverse_lazy('admin_login'))
def cancel_purchase_view(request, **kwargs):
    purchase = get_object_or_404(Purchase, pk=request.POST.get('elem_id'))
    purchase.cancel()
    return redirect(purchase.order.get_admin_edit_url())








