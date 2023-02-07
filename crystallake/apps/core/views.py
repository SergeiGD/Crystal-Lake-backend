from django.views.generic import ListView, TemplateView

from ..room.models import Room
from ..service.models import Service
from .utils import ClientContextMixin, get_image_src
from django.conf import settings


# Create your views here.


class Index(ClientContextMixin, ListView):
    template_name = 'core/index.html'
    model = Room
    context_object_name = 'rooms'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_hidden=False, date_deleted=None)[:3]
        context['current_page'] = 'index'
        min_price_room = Room.objects.filter(
            is_hidden=False,
            date_deleted=None
        ).order_by('default_price').values('default_price').first()
        max_price_room = Room.objects.filter(
            is_hidden=False,
            date_deleted=None
        ).order_by('-default_price').values('default_price').first()
        if max_price_room is not None and min_price_room is not None:
            context['min_price'] = min_price_room['default_price']
            context['max_price'] = max_price_room['default_price']
        else:
            context['min_price'] = 0
            context['max_price'] = 0
        context['check_in'] = settings.CHECK_IN_TIME
        context['check_out'] = settings.CHECK_OUT_TIME
        return {**context, **self.get_general_context()}

    def get_queryset(self):
        return Room.objects.filter(is_hidden=False, main_room=None, date_deleted=None)[:3]


class Contacts(ClientContextMixin, TemplateView):
    template_name = 'core/contacts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'contacts'
        return {**context, **self.get_general_context()}

