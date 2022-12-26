from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from ..core.utils import SafePaginator
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


class AdminTagUpdate(PermissionRequiredMixin, UpdateView):
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


class AdminTagCreate(PermissionRequiredMixin, CreateView):
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


# def admin_delete_tag(request, tag_id):
#     tag = get_object_or_404(Tag, slug=tag_id)
#     tag.date_deleted = datetime.now()
#     tag.save()
#     return redirect('admin_rooms')

class AdminDeleteTagView(DeleteView):
    model = Tag
    pk_url_kwarg = 'tag_id'
    success_url = reverse_lazy('admin_tags')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)





