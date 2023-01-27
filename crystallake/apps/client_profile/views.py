from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout

from ..order.models import Order
from ..core.utils import SafePaginator
from ..core.utils import ResponseMessage, RelocateResponseMixin
from .forms import ClientLoginForm

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
        if request.user.is_authenticated:
            return self.relocate(reverse_lazy('active_orders'))
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            client = authenticate(phone=phone, password=password)
            if client is not None:
                login(request, client)
                return self.relocate(reverse_lazy('active_orders'))
            else:
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Неверные данные': 'не найден пользователь с таким номером телефона и паролем'
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
