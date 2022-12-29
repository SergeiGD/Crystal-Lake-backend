from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .models import Worker
from ..core.utils import SafePaginator, ResponseMessage, RelocateResponseMixin
from ..user.models import CustomUser
from ..user.forms import UserForm
from .forms import WorkerForm


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
        #context['form_worker'] = WorkerForm(self.request.POST or None)
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        form.instance.save()
        return self.relocate(form.instance.get_admin_show_url())
        # context = self.get_context_data()
        # form_worker = context['form_worker']
        # if form_worker.is_valid():
        #     worker = Worker(user=form.instance)
        #     worker.save()
        #     return self.relocate(worker.get_admin_show_url())

