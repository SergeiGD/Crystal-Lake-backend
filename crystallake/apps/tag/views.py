from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from ..core.save_paginator import SafePaginator
from .models import Tag
from .forms import TagForm



# Create your views here.


class AdminTagsList(PermissionRequiredMixin, ListView):
    permission_required = 'tag.view_tag'
    model = Tag
    template_name = 'tag/admin_tags.html'
    context_object_name = 'tags'
    paginate_by = 10
    paginator_class = SafePaginator

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'tags'
        context['additional_page'] = True
        return context


class AdminTagsDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'tag.view_tag'
    model = Tag
    template_name = 'tag/admin_show_tag.html'
    context_object_name = 'tag'
    pk_url_kwarg = 'tag_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'tags'
        context['additional_page'] = True
        return context


class AdminTagsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'tag.update_tag'
    model = Tag
    template_name = 'tag/admin_edit_tag.html'
    context_object_name = 'tag'
    pk_url_kwarg = 'tag_id'
    form_class = TagForm

    def get_success_url(self):
        return self.object.get_admin_show_url()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'tags'
        context['additional_page'] = True
        return context


class AdminTagsCreate(PermissionRequiredMixin, CreateView):
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






