import json

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

from .models import *
from .forms import *


class RoomsCatalog(ListView):
    template_name = 'offer/rooms.html'
    model = Room
    context_object_name = 'rooms'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'rooms'
        return context

    def get_queryset(self):
        return Room.objects.filter(date_deleted=None, is_hidden=False, main_room=None)


class RoomDetail(DetailView):
    template_name = 'offer/room.html'
    model = Room
    slug_url_kwarg = 'room_slug'
    context_object_name = 'offer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'rooms'
        return context

    def get_object(self, queryset=None):
        obj = super(RoomDetail, self).get_object(queryset=queryset)
        if obj.date_deleted or obj.is_hidden or obj.main_room:
            raise Http404()
        return obj


class AdminRoomsList(PermissionRequiredMixin, ListView):
    permission_required = 'offer.view_room'
    template_name = 'offer/admin_rooms.html'
    model = Room
    context_object_name = 'rooms'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'rooms'
        return context

    def get_queryset(self):
        return Room.objects.filter(date_deleted=None, main_room=None)


class AdminRoomDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'offer.view_room'
    template_name = 'offer/admin_show_room.html'
    model = Room
    slug_url_kwarg = 'room_slug'
    context_object_name = 'offer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'rooms'
        return context

    def get_object(self, queryset=None):
        obj = super(AdminRoomDetail, self).get_object(queryset=queryset)
        if obj.date_deleted or obj.main_room:
            raise Http404()
        return obj


@permission_required('offer.change_room')
def admin_edit_room(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)

    form_room = RoomForm(request.POST or None, files=request.FILES or None, instance=room)
    PhotoFormset = modelformset_factory(Photo, form=PhotoForm, extra=0, can_delete=True)

    formset = PhotoFormset(request.POST or None, files=request.FILES or None, queryset=room.photos.all())

    context = {
        'form_room': form_room,
        'formset': formset,
        'current_page': 'rooms',
        'room': room,
        'photo_form': zip(formset.queryset, formset.forms)          # пакуем формы и объекты в один объект, для удобной обработки в темплейте
    }

    if request.method == 'POST':

        if all([form_room.is_valid(), formset.is_valid()]):

            changed_room = form_room.save(commit=True)

            formset.save(commit=False)

            for created_photo in formset.new_objects:
                created_photo.offer = changed_room                  # если новая картинки, то присваиваем номер, к которому она относится
                created_photo.save()

            for changed_photo in formset.changed_objects:
                changed_photo[0].save()

            for deleted_photo in formset.deleted_objects:
                deleted_photo.delete()

            url = reverse('admin_show_room', kwargs={'room_slug': changed_room.slug})
            response_data = {'url': url, 'message': 'successfully updated'}
            response = HttpResponse(json.dumps(response_data), content_type="application/json")     # при успехе отправляем json, который обработам ajax
            response.status_code = 302          # 302, т.к. редериктим при успехе на просмотр
            return response

        else:
            response = HttpResponse(form_room.errors.as_json())     # отправляем ошибки в виде json'a
            response.status_code = 400
            return response

    return render(request, 'offer/admin_edit_room.html', context)      # если GET, то просто рендерим темплейт

