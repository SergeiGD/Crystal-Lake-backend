from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from .models import Client
from ..core.utils import SafePaginator, ResponseMessage, RelocateResponseMixin
from .forms import ClientForm

# Create your views here.


class AdminClientsList(ListView):
    model = Client
    template_name = 'client/admin_clients.html'
    context_object_name = 'rooms'
    paginate_by = 10
    paginator_class = SafePaginator
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'clients'
        return context
    
    def get_queryset(self):
        return Client.objects.all()


class AdminCreateRoomView(RelocateResponseMixin, CreateView):
    model = Client
    template_name = 'client/admin_create_client.html'
    form_class = ClientForm

    def get_success_url(self):
        print(self.object.get_admin_show_url())
        return self.object.get_admin_show_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'clients'
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        form.instance.save()
        return self.relocate(form.instance.get_admin_show_url())

