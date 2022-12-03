from django.shortcuts import render
from django.views.generic import ListView
from ..offer.models import *

# Create your views here.


def index(request):
    return render(request, 'core/index.html')


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
