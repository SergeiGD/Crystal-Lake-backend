from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .models import Worker
from ..core.utils import SafePaginator, ResponseMessage, RelocateResponseMixin
from ..user.models import CustomUser
from ..user.forms import UserForm
from .forms import WorkerForm
from ..core.forms import ShortSearchForm
from ..service.models import Service


# Create your views here.


class AdminWorkersList(ListView):
    model = Worker
    template_name = 'worker/admin_workers.html'
    context_object_name = 'workers'
    paginate_by = 10
    paginator_class = SafePaginator

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminWorkersList, self).get_context_data(**kwargs)
        context['current_page'] = 'workers'
        return context

    def get_queryset(self):
        return Worker.objects.filter(date_deleted=None)


class AdminCreatWorker(RelocateResponseMixin, CreateView):
    model = Worker
    template_name = 'worker/admin_create_worker.html'
    form_class = WorkerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'workers'
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        form.instance.save()
        return self.relocate(form.instance.get_admin_show_url())


class AdminWorkerDetail(DetailView):
    model = Worker
    template_name = 'worker/admin_show_worker.html'
    context_object_name = 'worker'
    pk_url_kwarg = 'worker_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'workers'
        context['delete_link'] = self.object.get_admin_delete_url()
        return context


class AdminWorkerUpdate(RelocateResponseMixin, UpdateView):
    model = Worker
    template_name = 'worker/admin_edit_worker.html'
    context_object_name = 'worker'
    pk_url_kwarg = 'worker_id'
    form_class = WorkerForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminWorkerUpdate, self).get_context_data(**kwargs)
        context['current_page'] = 'workers'
        context['form_services'] = ShortSearchForm(self.request.POST or None)
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        form.instance.save()
        return self.relocate(form.instance.get_admin_show_url())


def admin_delete_worker(request, worker_id):
    get_object_or_404(Worker, pk=worker_id).mark_as_deleted()
    return redirect('admin_workers')


def get_unattached_services(request, worker_id):
    if request.method == 'POST':
        worker = get_object_or_404(Worker, pk=worker_id)
        services = Service.objects.filter(date_deleted=None).exclude(pk__in=worker.qualifications.values('pk')).search(**request.POST.dict())
        tags_paginator = SafePaginator(services, 1)
        page = request.POST.get('page_number', 1)
        services_page = tags_paginator.get_page(page)
        num_pages = tags_paginator.num_pages

        data = {'pages': {
            'pages_count': num_pages,
            'current_page': services_page.number,
        }, 'tags': []}
        for service in services_page.object_list:
            item = {'name': service.name, 'id': service.pk, 'link': service.get_admin_show_url()}
            data['tags'].append(item)

        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
        return HttpResponse(response_message.get_json(), content_type='application/json', status=200)


def add_service_to_worker(request, worker_id):
    if request.method == 'POST':
        worker = get_object_or_404(Worker, pk=worker_id)
        service_id = request.POST.get('elem_id', -1)
        service = get_object_or_404(Service, pk=service_id)
        worker.qualifications.add(service)
        #worker.save()
        data = {'name': service.name, 'id': service.pk, 'link': service.get_admin_show_url()}
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
        return HttpResponse(response_message.get_json(), content_type='application/json', status=200)


def del_service_from_worker(request, worker_id):
    if request.method == 'POST':
        worker = get_object_or_404(Worker, pk=worker_id)
        service_id = request.POST.get('elem_id', -1)
        service = get_object_or_404(Service, pk=service_id)
        worker.qualifications.remove(service)
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
        return HttpResponse(response_message.get_json(), content_type='application/json', status=200)


