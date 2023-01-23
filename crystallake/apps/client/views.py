from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.template.loader import render_to_string

from .models import Client
from ..core.utils import SafePaginator, ResponseMessage, RelocateResponseMixin, get_paginator_data, is_ajax
from ..user.forms import UserForm, SearchUserForm
from ..user.models import CustomUser
from .forms import ClientForm

# Create your views here.


class AdminClientsList(ListView):
    model = Client
    template_name = 'client/admin_clients.html'
    context_object_name = 'clients'
    paginate_by = 1
    paginator_class = SafePaginator
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'clients'
        context['form_clients'] = SearchUserForm(self.request.GET)
        return context
    
    def get_queryset(self):
        search_form = SearchUserForm(self.request.GET)
        clients = Client.objects.filter(date_deleted=None)

        if search_form.is_valid():
            clients = clients.search(**search_form.cleaned_data)

        return clients


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
    get_object_or_404(Client, pk=client_id).mark_as_deleted()
    return redirect('admin_clients')


def find_clients(request, **kwargs):
    clients = Client.objects.filter(date_deleted=None).search(
        **request.POST.dict()
    )

    clients_page, num_pages = get_paginator_data(clients, request.POST.get('page_number', 1))

    data = {'pages': {
        'pages_count': num_pages,
        'current_page': clients_page.number,
    }, 'items': []}

    if is_ajax(request):
        popup_to_open = request.POST.get('popup_to_open')
        html = render_to_string('core/clients_body.html', {'clients_list': clients_page.object_list, 'popup_to_open': popup_to_open})
        data['items'] = html
    else:
        for client in clients_page.object_list:
            item = {
                'name': client.full_name,
                'id': client.pk,
                'phone': str(client.phone),
                'email': client.email,
                'link': client.get_admin_show_url()
            }
            data['items'].append(item)

    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
    return HttpResponse(response_message.get_json(), content_type='application/json', status=200)
