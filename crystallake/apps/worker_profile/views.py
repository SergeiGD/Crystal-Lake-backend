from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from ..core.utils import ResponseMessage, RelocateResponseMixin
from .forms import AdminLoginForm

# Create your views here.


class AdminLoginView(RelocateResponseMixin, LoginView):
    template_name = 'worker_profile/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = AdminLoginForm(self.request.POST)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(reverse_lazy('admin_orders'))
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
                return redirect(reverse_lazy('admin_orders'))
            else:
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Неверные данные': 'Не найден сотрудник с таким номером и паролем'
                })
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class AdminLoginRequired(LoginRequiredMixin):
    login_url = reverse_lazy('admin_login')


def admin_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('admin_login')
