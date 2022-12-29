from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .models import Client
from ..core.utils import SafePaginator, ResponseMessage, RelocateResponseMixin
from ..user.forms import UserForm
from ..user.models import CustomUser
from .forms import ClientForm

# Create your views here.


class AdminClientsList(ListView):
    model = Client
    template_name = 'client/admin_clients.html'
    context_object_name = 'clients'
    paginate_by = 10
    paginator_class = SafePaginator
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'clients'
        return context
    
    def get_queryset(self):
        return Client.objects.filter(date_deleted=None)


class AdminCreatClient(RelocateResponseMixin, CreateView):
    model = Client
    template_name = 'client/admin_create_client.html'
    form_class = ClientForm

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


class AdminClientDetail(DetailView):    # TODO: не давать возможность открыть удаленные
    model = Client
    template_name = 'client/admin_show_client.html'
    context_object_name = 'client'
    pk_url_kwarg = 'client_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'clients'
        context['delete_link'] = self.object.get_admin_delete_url()
        return context


class AdminClientUpdate(RelocateResponseMixin, UpdateView):
    model = Client
    template_name = 'client/admin_edit_client.html'
    context_object_name = 'client'
    pk_url_kwarg = 'client_id'
    form_class = ClientForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminClientUpdate, self).get_context_data(**kwargs)
        context['current_page'] = 'clients'
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        form.instance.save()
        return self.relocate(form.instance.get_admin_show_url())


def admin_delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client.mark_as_deleted()
    return redirect('admin_clients')
