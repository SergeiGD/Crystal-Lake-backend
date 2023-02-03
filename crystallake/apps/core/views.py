from django.views.generic import ListView, TemplateView

from ..room.models import Room
from ..service.models import Service
from .utils import ClientContextMixin


# Create your views here.


class Index(ClientContextMixin, ListView):
    template_name = 'core/index.html'
    model = Room
    context_object_name = 'rooms'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_hidden=False, date_deleted=None)[:3]
        context['current_page'] = 'index'
        return {**context, **self.get_general_context()}

    def get_queryset(self):
        return Room.objects.filter(is_hidden=False, main_room=None, date_deleted=None)[:3]


class Contacts(ClientContextMixin, TemplateView):
    template_name = 'core/contacts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'contacts'
        return {**context, **self.get_general_context()}

