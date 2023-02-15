from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView

from ..core.utils import ResponseMessage, RelocateResponseMixin
from .forms import AdminLoginForm, AdminResetForm, AdminPhoneForm
from django.conf import settings

from ..client_profile.utils import SmsCodeMixin
from ..core.utils import get_client_ip
from ..user.code_type_choises import CodeType
from ..worker.models import Worker
from ..user.models import SmsCode

# Create your views here.


class AdminLoginView(RelocateResponseMixin, LoginView):
    template_name = 'worker_profile/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = AdminLoginForm(self.request.POST)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(reverse_lazy('admin_profile'))
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(reverse_lazy('admin_orders'))
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            worker = authenticate(phone=phone, password=password)
            if worker is not None and worker.is_staff:
                login(request, worker, backend=settings.AUTHENTICATION_BACKENDS[0])
                return self.relocate(reverse_lazy('admin_profile'))
            else:
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Неверные данные': ['Не найден сотрудник с таким номером и паролем']
                })
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class AdminSmsCodeView(RelocateResponseMixin, TemplateView):
    template_name = 'worker_profile/send_sms.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdminPhoneForm(self.request.POST)
        return context

    def post(self, request, *args, **kwargs):
        form = AdminPhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if not Worker.objects.filter(phone=phone, is_active=True).exists():
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Неверные данные': ['Не найден сотрудник с таким номером телефона']
                })
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response
            SmsCode.objects.send_sms(phone, code_type=CodeType.password_reset.name, ip=get_client_ip(request))
            return self.relocate(reverse_lazy('admin_reset_password'))
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=phone_form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class AdminResetPasswordView(SmsCodeMixin, RelocateResponseMixin, TemplateView):
    template_name = 'worker_profile/reset_password.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_form'] = AdminResetForm(self.request.POST)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(reverse_lazy('admin_orders'))
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(reverse_lazy('admin_orders'))
        form = AdminResetForm(request.POST)
        if form.is_valid():
            password_1 = form.cleaned_data['password_1']
            password_2 = form.cleaned_data['password_2']
            if password_1 != password_2:
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Неверные данные': ['Пароли не совпадают']
                })
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response
            sms_code = self.find_sms_code(
                form.cleaned_data['code'],
                code_type=CodeType.password_reset.name,
                ip=get_client_ip(request)
            )
            if sms_code is None:
                return self.get_code_error_message()
            worker = Worker.objects.filter(phone=sms_code.phone, is_active=True).first()
            if worker is None:
                return self.get_unknown_phone_error()
            password = make_password(form.cleaned_data['password_1'])
            worker.password = password
            worker.save()
            sms_code.is_used = True
            sms_code.save()
            login(request, worker, backend=settings.AUTHENTICATION_BACKENDS[0])
            return self.relocate(reverse_lazy('admin_profile'))
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class AdminProfileView(TemplateView):
    template_name = 'worker_profile/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'profile'
        return context


def admin_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('admin_login')
    return redirect('admin_login')
