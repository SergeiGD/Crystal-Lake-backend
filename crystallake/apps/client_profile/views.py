from datetime import timedelta, datetime

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, TemplateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from ..order.models import Order
from ..core.utils import SafePaginator
from ..core.utils import ResponseMessage, RelocateResponseMixin, ClientContextMixin
from .forms import ClientLoginForm, SendCodeForm, ClientPhoneForm, ClientPasswordsForm, ClientInfoForm
from ..order.models import Order, Purchase, PurchaseCountable
from ..client.models import Client
from ..user.models import SmsCode, CustomUser
from ..worker.models import Worker
from .utils import SmsCodeMixin, PhoneCheckMixin, ActiveLoginRequiredMixin
from django.conf import settings
from ..service.forms import ManageServicePurchaseForm
from ..room.forms import ManageRoomPurchaseForm
from ..order.views import RoomPurchaseMixin, ServicePurchaseMixin

# Create your views here.


class ActiveOrdersCatalog(ActiveLoginRequiredMixin, ListView):
    login_url = 'index'
    model = Order
    context_object_name = 'orders'
    template_name = 'client_profile/active_orders.html'
    paginator_class = SafePaginator
    paginate_by = settings.CLIENT_PAGINATE_BY

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'profile'
        context['current_profile_page'] = 'active_orders'
        return context

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(
            date_canceled=None,
            date_finished=None,
            client=user,
            paid__gt=0
        )

        return orders


class HistoryCatalog(ActiveLoginRequiredMixin, ListView):
    login_url = 'index'
    model = Order
    context_object_name = 'orders'
    template_name = 'client_profile/history.html'
    paginator_class = SafePaginator
    paginate_by = settings.CLIENT_PAGINATE_BY

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'profile'
        context['current_profile_page'] = 'history'
        return context

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.exclude(date_canceled=None, date_finished=None).filter(
            client=user
        )
        return orders


class HistoryItemView(ActiveLoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'
    template_name = 'client_profile/history_item.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'profile'
        context['current_profile_page'] = 'history'
        return context

    def get_object(self, queryset=None):
        obj = super(HistoryItemView, self).get_object(queryset=queryset)
        if obj.client != self.request.user:
            raise Http404()
        if obj.date_finished is not None and obj.date_canceled is not None:
            raise Http404()
        return obj


class ManageOrder(ActiveLoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    url = 'room_slug'
    pk_url_kwarg = 'order_id'
    template_name = 'client_profile/manage_order.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'profile'
        context['current_profile_page'] = 'active_orders'
        return context

    def get_object(self, queryset=None):
        obj = super(ManageOrder, self).get_object(queryset=queryset)
        if obj.date_finished or obj.date_canceled or obj.client != self.request.user or not obj.is_editable():
            raise Http404()
        return obj


class ManagePurchase(ActiveLoginRequiredMixin, DetailView):
    model = Purchase
    template_name = 'client_profile/manage_purchase.html'
    context_object_name = 'purchase'
    pk_url_kwarg = 'purchase_id'

    def get_context_data(self, **kwargs):
        context = super(ManagePurchase, self).get_context_data(**kwargs)
        if isinstance(self.object, PurchaseCountable):
            form = ManageServicePurchaseForm(purchase=self.object)
        else:
            form = ManageRoomPurchaseForm(purchase=self.object)
        context['form'] = form
        context['current_page'] = 'profile'
        context['current_profile_page'] = 'active_orders'
        return context

    def get_object(self, queryset=None):
        obj = super(ManagePurchase, self).get_object(queryset=queryset)
        if not obj.is_editable():
            raise Http404()
        return obj


class RoomPurchaseView(RoomPurchaseMixin, View):
    def post(self, request, purchase_id, **kwargs):
        purchase = get_object_or_404(Purchase, pk=purchase_id)
        form = ManageRoomPurchaseForm(request.POST, purchase=purchase)

        if request.user != purchase.order.client:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                'Ошибка': ['Не удалось опознать пользователя, создавшего заказ']
            })
            response = HttpResponse(response_message.get_json(), status=403, content_type='application/json')
            return response

        if form.is_valid():
            purchase.offer = purchase.offer.main_room
            start, end = self.aware_date(form.cleaned_data['date_start'], form.cleaned_data['date_end'])

            # ВОТКНУТЬ КНОПКУ НЕСКОЛЬКО КОМНАТ
            return self.manage_room_purchase(purchase, start, end, False, success_url=purchase.order.get_client_manage_url())
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class ServicePurchaseView(ServicePurchaseMixin, View):
    def post(self, request, purchase_id, **kwargs):
        purchase = get_object_or_404(PurchaseCountable, pk=purchase_id)
        form = ManageServicePurchaseForm(request.POST, purchase=purchase)

        if request.user != purchase.order.client:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                'Ошибка': ['Не удалось опознать пользователя, создавшего заказ']
            })
            response = HttpResponse(response_message.get_json(), status=403, content_type='application/json')
            return response

        if form.is_valid():
            purchase.quantity = form.cleaned_data['quantity']
            purchase.start, purchase.end = self.aware_time(
                form.cleaned_data['date'],
                form.cleaned_data['time_start'],
                form.cleaned_data['time_end']
            )

            return self.manage_service_purchase(purchase, success_url=purchase.order.get_client_manage_url())

        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


def cancel_purchase_view(request, purchase_id, **kwargs):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    if request.user != purchase.order.client:
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
            'Ошибка': ['Не удалось опознать пользователя, создавшего заказ']
        })
        response = HttpResponse(response_message.get_json(), status=403, content_type='application/json')
        return response
    if not purchase.is_editable():
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
            'Ошибка': ['Эту покупку нельзя изменить']
        })
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response
    purchase.cancel()
    if purchase.order.is_editable():
        return redirect(purchase.order.get_client_manage_url())
    return redirect(reverse_lazy('active_orders'))


def pay_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.user != order.client:
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
            'Ошибка': ['Не удалось опознать пользователя, создавшего заказ']
        })
        response = HttpResponse(response_message.get_json(), status=403, content_type='application/json')
        return response
    order.mark_as_fully_paid()
    return redirect(order.get_client_manage_url())


def cancel_order_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.user != order.client:
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
            'Ошибка': ['Не удалось опознать пользователя, создавшего заказ']
        })
        response = HttpResponse(response_message.get_json(), status=403, content_type='application/json')
        return response
    if not order.is_cancelable():
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
            'Ошибка': ['Нельзя отменить уже начавшийся заказ']
        })
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response
    order.mark_as_canceled()
    return redirect(reverse_lazy('active_orders'))


class ClientInfoView(ActiveLoginRequiredMixin, RelocateResponseMixin, UpdateView):
    login_url = 'index'
    model = Client
    template_name = 'client_profile/info.html'
    context_object_name = 'client'
    form_class = ClientInfoForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'profile'
        context['current_profile_page'] = 'info'

        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        form.instance.save()
        return self.relocate(reverse_lazy('client_info'))


class ClientLoginView(RelocateResponseMixin, View):
    def post(self, request):
        if request.user.is_authenticated and request.user.is_active:
            return self.relocate(reverse_lazy('active_orders'))
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            client = authenticate(phone=phone, password=password)
            if client is not None:
                login(request, client, backend=settings.AUTHENTICATION_BACKENDS[0])
                return self.relocate(reverse_lazy('active_orders'))
            else:
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Неверные данные': ['Не найден пользователь с таким номером и паролем']
                })
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


def client_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')


class SendRegisterCodeView(SmsCodeMixin, RelocateResponseMixin, View):
    def post(self, request):
        form = SendCodeForm(request.POST, prefix='register')
        if form.is_valid():
            sms_code = self.find_sms_code(form.cleaned_data['code'])
            if not sms_code:
                return self.get_code_error_message()
            client = Client.objects.filter(phone=sms_code.phone).first()
            if not client:
                return self.get_unknown_phone_error()
            client.is_active = True
            client.save()
            sms_code.is_used = True
            sms_code.save()
            login(request, client, backend=settings.AUTHENTICATION_BACKENDS[0])
            return self.relocate(reverse_lazy('active_orders'))
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class ClientRegisterView(PhoneCheckMixin, View):
    def post(self, request):
        phone_form = ClientPhoneForm(request.POST, prefix='register')
        passwords_form = ClientPasswordsForm(request.POST, prefix='register')
        if phone_form.is_valid() and passwords_form.is_valid():
            cleaned_data = {**passwords_form.cleaned_data, **phone_form.cleaned_data}
            phone = cleaned_data['phone']
            if self.is_phone_in_use(phone):
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Неверные данные': ['Невозможно зарегистировать этот номер. Похоже, он уже зарегестирован']
                })
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response
            client = Client.objects.filter(phone=phone, is_active=False).first()
            if client is None:
                client = Client()
            password = make_password(cleaned_data['password1'])
            client.phone = phone
            client.password = password
            client.is_active = False
            client.save()
            SmsCode.objects.send_sms(phone)
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
            response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
            return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={**passwords_form, **phone_form})
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class ClientResetPasswordCodeView(View):
    def post(self, request):
        phone_form = ClientPhoneForm(request.POST, prefix='reset')
        if phone_form.is_valid():
            phone = phone_form.cleaned_data['phone']
            if not Client.objects.filter(phone=phone, is_active=True).exists():
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Неверные данные': ['Не найден клиент с таким номером телефона']
                })
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response
            SmsCode.objects.send_sms(phone)
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
            response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
            return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=phone_form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class ClientResetPasswordView(SmsCodeMixin, RelocateResponseMixin, View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relocate_url = reverse_lazy('active_orders')

    def post(self, request):
        passwords_form = ClientPasswordsForm(request.POST, prefix='reset')
        code_form = SendCodeForm(request.POST, prefix='reset')
        if passwords_form.is_valid() and code_form.is_valid():
            sms_code = self.find_sms_code(code_form.cleaned_data['code'])
            if sms_code is None:
                return self.get_code_error_message()
            client = Client.objects.filter(phone=sms_code.phone).first()
            if client is None:
                return self.get_unknown_phone_error()
            password = make_password(passwords_form.cleaned_data['password1'])
            client.password = password
            client.save()
            sms_code.is_used = True
            sms_code.save()
            login(request, client, backend=settings.AUTHENTICATION_BACKENDS[0])
            return self.relocate(self.relocate_url)
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={**passwords_form.errors, **code_form.errors})
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class ClientChangePasswordView(ClientResetPasswordView, ActiveLoginRequiredMixin):
    login_url = 'index'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relocate_url = reverse_lazy('client_info')

    def get(self, request):
        context = {
            'current_page': 'profile',
            'current_profile_page': 'info',
            'code_form':  SendCodeForm(prefix='reset'),
            'passwords_form': ClientPasswordsForm(prefix='reset')
        }
        SmsCode.objects.send_sms(request.user.phone)
        return render(request, template_name='client_profile/change_password.html', context=context)


class CartView(ClientContextMixin, TemplateView):
    template_name = 'client_profile/cart.html'

    def get_context_data(self, **kwargs):
        if self.request.user is None or not self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['order'] = Order()
            context['cart_items'] = Purchase.objects.none()
            context['current_page'] = 'cart'
            return {**context, **self.get_general_context()}
        context = super().get_context_data(**kwargs)
        order = self.request.user.get_cart()
        if order is None:
            client = get_object_or_404(CustomUser, pk=self.request.user.pk)
            order = Order(client=client, date_create=timezone.now())
            cart_items = Purchase.objects.none()
        else:
            cart_items = order.purchases
        context['order'] = order
        context['cart_items'] = cart_items
        context['current_page'] = 'cart'
        return {**context, **self.get_general_context()}


def cart_fully_pay_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            order = request.user.get_cart()
            order.mark_as_fully_paid()
            if request.user.is_active:
                return redirect(order.get_client_manage_url())
            return redirect('index')
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                'Ошибка': ['Не удалось обнаружить пользователя, создавшего корзину']
            })
            response = HttpResponse(response_message.get_json(), status=401, content_type='application/json')
            return response


def cart_prepayment_pay_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            order = request.user.get_cart()
            order.mark_as_prepayment_paid()
            if request.user.is_active:
                return redirect('active_orders')
            return redirect('index')
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                'Ошибка': ['Не удалось обнаружить пользователя, создавшего корзину']
            })
            response = HttpResponse(response_message.get_json(), status=401, content_type='application/json')
            return response


def remove_from_cart_view(request, purchase_id, **kwargs):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    if not purchase.order.is_cart:
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
            'Ошибка': ['Этот элемент не является частью корзины']
        })
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response
    if purchase.order.client != request.user:
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
            'Ошибка': ['Нельзя изменить чужую корзину']
        })
        response = HttpResponse(response_message.get_json(), status=403, content_type='application/json')
        return response
    purchase.cancel()
    return redirect(reverse_lazy('cart'))


