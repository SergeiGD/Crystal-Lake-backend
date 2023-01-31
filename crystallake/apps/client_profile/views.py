from datetime import timedelta, datetime

from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from ..order.models import Order
from ..core.utils import SafePaginator
from ..core.utils import ResponseMessage, RelocateResponseMixin, ClientContextMixin
from .forms import ClientLoginForm, SendCodeForm, ClientPhoneForm, ClientPasswordsForm
from ..order.models import Order, Purchase
from ..client.models import Client
from ..user.models import SmsCode, CustomUser
from ..worker.models import Worker
from .utils import SmsCodeMixin, PasswordsMixin

# Create your views here.


class ActiveOrdersCatalog(LoginRequiredMixin, ListView):
    login_url = 'index'
    model = Order
    context_object_name = 'orders'
    template_name = 'client_profile/active_orders.html'
    paginator_class = SafePaginator
    paginate_by = 10

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


class ClientLoginView(RelocateResponseMixin, View):
    def post(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            return self.relocate(reverse_lazy('active_orders'))
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            client = authenticate(phone=phone, password=password)
            if client is not None and not client.is_staff:
                login(request, client)
                return self.relocate(reverse_lazy('active_orders'))
            else:
                # branch test
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
            login(request, client)
            return self.relocate(reverse_lazy('active_orders'))
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class ClientRegisterView(PasswordsMixin, View):
    def post(self, request):
        phone_form = ClientPhoneForm(request.POST, prefix='register')
        passwords_form = ClientPasswordsForm(request.POST, prefix='register')
        if phone_form.is_valid() and passwords_form.is_valid():
            cleaned_data = {**passwords_form.cleaned_data, **phone_form.cleaned_data}
            phone = cleaned_data['phone']
            if Client.objects.filter(phone=phone, is_active=True).exists() or Worker.objects.filter(phone=phone).exists():
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Неверные данные': ['Невозможно зарегистировать этот номер. Похоже, он уже зарегестирован']
                })
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response
            client = Client.objects.filter(phone=phone, is_active=False).first()
            if client is None:
                client = Client()
            password1 = cleaned_data['password1']
            password2 = cleaned_data['password2']
            if password1 != password2:
                return self.get_unequal_passwords_error()
            password = make_password(password1)
            client.phone = phone
            client.password = password
            client.is_active = False
            client.save()
            SmsCode.objects.send_sms(phone)
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
            response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
            return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class ClientResetPasswordCodeView(View):
    def post(self, request):
        phone_form = ClientPhoneForm(request.POST, prefix='reset')
        if phone_form.is_valid():
            phone = phone_form.cleaned_data['phone']
            if not Client.objects.filter(phone=phone, is_active=True).exists():
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Неверные данные': ['Не найден пользователь с таким номером телефона']
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


class ClientResetPasswordView(PasswordsMixin, SmsCodeMixin, RelocateResponseMixin, View):
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
            password1 = passwords_form.cleaned_data['password1']
            password2 = passwords_form.cleaned_data['password2']
            if password1 != password2:
                return self.get_unequal_passwords_error()
            password = make_password(password1)
            client.password = password
            client.save()
            sms_code.is_used = True
            sms_code.save()
            login(request, client)
            return self.relocate(reverse_lazy('active_orders'))
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=reset_form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class CartView(ClientContextMixin, TemplateView):
    template_name = 'client_profile/cart.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated or self.request.user.is_staff:
            context = super().get_context_data(**kwargs)
            context['order'] = Order()
            context['cart_items'] = Purchase.objects.none()
            context['current_page'] = 'cart'
            return {**context, **self.get_general_context()}
        context = super().get_context_data(**kwargs)
        order = Order.objects.filter(
            client=self.request.user,
            paid=0, refunded=0,
            date_canceled=None,
            date_finished=None
        ).first()
        if order is None:
            # TODO: пофиксить, мб ссылка просто на кастом юзера
            client = get_object_or_404(Client, pk=self.request.user.pk)
            order = Order(client=client, date_create=timezone.now())
            cart_items = Purchase.objects.none()
        else:
            cart_items = order.purchases
        context['order'] = order
        context['cart_items'] = cart_items
        context['current_page'] = 'cart'
        return context

