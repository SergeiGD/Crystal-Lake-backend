from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View

from ..room.models import Room
from ..service.models import Service
from .utils import ResponseMessage, RelocateResponseMixin


# Create your views here.


class Index(ListView):
    template_name = 'core/index.html'
    model = Room
    context_object_name = 'rooms'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_hidden=False)[:3]
        context['current_page'] = 'index'
        return context

    def get_queryset(self):
        return Room.objects.filter(is_hidden=False, main_room=None)[:3]



# def client_login_view(request):
#     if request.user.is_authenticated:
#         print(request.META.get('HTTP_REFERER', '/'))
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             phone = form.cleaned_data['phone']
#             password = form.cleaned_data['password']
#             client = authenticate(phone=phone, password=password)
#             if client is not None:
#                 login(request, client)
#                 response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=client.phone)
#                 response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
#                 return response
#             else:
#                 response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
#                     'Неверные данные': 'не найден пользователь с таким номером телефона и паролем'
#                 })
#                 response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
#                 return response
#         else:
#             response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
#             response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
#             return response

