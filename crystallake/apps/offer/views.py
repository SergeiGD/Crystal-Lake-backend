from django.shortcuts import render

# Create your views here.

from .models import *
from django.views.generic import ListView, DetailView


class RoomsCatalog(ListView):
    template_name = 'offer/rooms.html'
    model = Room
    context_object_name = 'rooms'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'rooms'
        return context


class RoomDetail(DetailView):
    template_name = 'offer/room.html'
    model = Room
    slug_url_kwarg = 'room_slug'
    context_object_name = 'offer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'rooms'
        return context


class AdminRoomsList(ListView):
    template_name = 'offer/admin_rooms.html'
    model = Room
    context_object_name = 'rooms'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'rooms'
        return context


class AdminRoomDetail(DetailView):
    template_name = 'offer/admin_show_room.html'
    model = Room
    slug_url_kwarg = 'room_slug'
    context_object_name = 'offer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'rooms'
        return context

