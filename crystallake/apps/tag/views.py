from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.template.loader import render_to_string
from django.conf import settings


from ..core.utils import SafePaginator, ResponseMessage, RelocateResponseMixin, get_paginator_data, is_ajax
from ..core.forms import ShortSearchForm
from .models import Tag
from .forms import TagForm


# Create your views here.


class AdminTagsList(PermissionRequiredMixin, ListView):
    permission_required = 'tag.view_tag'
    model = Tag
    template_name = 'tag/admin_tags.html'
    context_object_name = 'tags'
    paginate_by = settings.ADMIN_PAGINATE_BY
    paginator_class = SafePaginator

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'tags'
        context['additional_page'] = True
        context['form_tags'] = ShortSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        search_form = ShortSearchForm(self.request.GET)
        tags = Tag.objects.all()

        if search_form.is_valid():
            tags = tags.search(**search_form.cleaned_data)

        return tags


class AdminTagDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'tag.view_tag'
    model = Tag
    template_name = 'tag/admin_show_tag.html'
    context_object_name = 'tag'
    pk_url_kwarg = 'tag_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'tags'
        context['additional_page'] = True
        context['delete_link'] = self.object.get_admin_delete_url()
        context['offers'] = self.object.offers.filter(date_deleted=None)    #TODO: МБ ПЕРЕДЕЛАТЬ КАК-ТО БОЛЕЕ КРАСИВО
        return context


class AdminTagUpdate(RelocateResponseMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'tag.update_tag'
    model = Tag
    template_name = 'tag/admin_edit_tag.html'
    context_object_name = 'tag'
    pk_url_kwarg = 'tag_id'
    form_class = TagForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'tags'
        context['additional_page'] = True
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        form.instance.save()
        return self.relocate(form.instance.get_admin_show_url())


class AdminTagCreate(RelocateResponseMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'tag.create_tag'
    model = Tag
    template_name = 'tag/admin_add_tag.html'
    context_object_name = 'tag'
    form_class = TagForm

    def get_success_url(self):
        return self.object.get_admin_show_url()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'tags'
        context['additional_page'] = True
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        form.instance.save()
        return self.relocate(form.instance.get_admin_show_url())


class AdminDeleteTagView(DeleteView):
    model = Tag
    pk_url_kwarg = 'tag_id'
    success_url = reverse_lazy('admin_tags')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def find_tags(request, **kwargs):
    tags = Tag.objects.all().search(
        **request.POST.dict()
    )

    tags_page, num_pages = get_paginator_data(tags, request.POST.get('page_number', 1))

    data = {'pages': {
        'pages_count': num_pages,
        'current_page': tags_page.number,
    }, 'items': []}

    if is_ajax(request):
        popup_to_open = request.POST.get('popup_to_open')
        html = render_to_string('core/tags_body.html', {'tags_list': tags_page.object_list, 'popup_to_open': popup_to_open})
        data['items'] = html
    else:
        for tag in tags_page.object_list:
            item = {
                'name': tag.name,
                'id': tag.pk,
                'link': tag.get_admin_show_url()
            }
            data['items'].append(item)

    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
    return HttpResponse(response_message.get_json(), content_type='application/json', status=200)





