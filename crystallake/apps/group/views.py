from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.template.loader import render_to_string
from django.conf import settings

from .models import GroupProxy, PermissionsProxy
from ..core.utils import SafePaginator, ResponseMessage, RelocateResponseMixin, get_paginator_data, is_ajax
from ..worker.models import Worker
from ..core.forms import ShortSearchForm
from .forms import GroupForm

# Create your views here.


class AdminGroupsList(ListView):
    model = GroupProxy
    template_name = 'group/admin_groups.html'
    context_object_name = 'groups'
    paginate_by = settings.ADMIN_PAGINATE_BY
    paginator_class = SafePaginator

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminGroupsList, self).get_context_data()
        context['current_page'] = 'groups'
        context['additional_page'] = True
        context['form_groups'] = ShortSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        search_form = ShortSearchForm(self.request.GET)
        groups = GroupProxy.objects.all()

        if search_form.is_valid():
            groups = groups.search(**search_form.cleaned_data)

        return groups


class AdminGroupDetail(DetailView):
    model = GroupProxy
    template_name = 'group/admin_show_group.html'
    context_object_name = 'group'
    pk_url_kwarg = 'group_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminGroupDetail, self).get_context_data(**kwargs)
        context['current_page'] = 'groups'
        context['additional_page'] = True
        context['delete_link'] = self.object.get_admin_delete_url()
        context['workers'] = Worker.objects.filter(groups=self.object, date_deleted=None)
        context['permissions'] = self.object.permissions.all()
        return context


class AdminGroupUpdate(RelocateResponseMixin, UpdateView):
    model = GroupProxy
    template_name = 'group/admin_edit_group.html'
    context_object_name = 'group'
    pk_url_kwarg = 'group_id'
    form_class = GroupForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'groups'
        context['additional_page'] = True
        context['workers'] = Worker.objects.filter(groups__in=[self.object])
        context['form_permissions'] = ShortSearchForm()
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        form.instance.save()
        return self.relocate(form.instance.get_admin_show_url())


class AdminGroupCreate(RelocateResponseMixin, CreateView):
    model = GroupProxy
    template_name = 'group/admin_create_group.html'
    context_object_name = 'group'
    form_class = GroupForm

    def get_success_url(self):
        return self.object.get_admin_show_url()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'groups'
        context['additional_page'] = True
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        form.instance.save()
        return self.relocate(form.instance.get_admin_show_url())


class AdminGroupDelete(DeleteView):
    model = GroupProxy
    pk_url_kwarg = 'group_id'
    success_url = reverse_lazy('admin_groups')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def del_permission_from_group(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(GroupProxy, pk=group_id)
        permission_id = request.POST.get('elem_id', -1)
        permission = get_object_or_404(PermissionsProxy, pk=permission_id)
        group.permissions.remove(permission)
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
        return HttpResponse(response_message.get_json(), content_type='application/json', status=200)


def find_permissions(request, **kwargs):
    permissions = PermissionsProxy.objects.all().search(
        **request.POST.dict()
    )

    permissions_page, num_pages = get_paginator_data(permissions, request.POST.get('page_number', 1))

    data = {'pages': {
        'pages_count': num_pages,
        'current_page': permissions_page.number,
    }, 'items': []}

    if is_ajax(request):
        popup_to_open = request.POST.get('popup_to_open')
        html = render_to_string('core/permissions_body.html', {'permissions_list': permissions_page.object_list, 'popup_to_open': popup_to_open})
        data['items'] = html
    else:
        for tag in permissions_page.object_list:
            item = {
                'name': tag.name,
                'id': tag.pk,
            }
            data['items'].append(item)

    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
    return HttpResponse(response_message.get_json(), content_type='application/json', status=200)


def add_permission_to_group(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(GroupProxy, pk=group_id)
        permission_id = request.POST.get('elem_id', -1)
        permission = get_object_or_404(PermissionsProxy, pk=permission_id)
        group.permissions.add(permission)
        data = {'name': permission.name, 'id': permission.pk}
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
        return HttpResponse(response_message.get_json(), content_type='application/json', status=200)


def find_groups(request, **kwargs):
    groups = GroupProxy.objects.all().search(
        **request.POST.dict()
    )

    groups_page, num_pages = get_paginator_data(groups, request.POST.get('page_number', 1))

    data = {'pages': {
        'pages_count': num_pages,
        'current_page': groups_page.number,
    }, 'items': []}

    if is_ajax(request):
        popup_to_open = request.POST.get('popup_to_open')
        html = render_to_string('core/groups_body.html', {'groups_list': groups_page.object_list, 'popup_to_open': popup_to_open})
        data['items'] = html
    else:
        for tag in groups_page.object_list:
            item = {
                'name': tag.name,
                'id': tag.pk,
                'link': tag.get_admin_show_url()
            }
            data['items'].append(item)

    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
    return HttpResponse(response_message.get_json(), content_type='application/json', status=200)