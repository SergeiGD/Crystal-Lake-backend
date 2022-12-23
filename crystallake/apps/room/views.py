import json
from datetime import datetime

from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, Http404
from django.urls import reverse


from ..core.save_paginator import SafePaginator
from .models import Room
from .forms import RoomForm, SearchRoomsForm
from ..photo.forms import PhotoForm
from ..photo.models import Photo
from ..tag.forms import SearchTagForm

# Create your views here.


class RoomsCatalog(ListView):
    template_name = 'room/rooms.html'
    model = Room
    context_object_name = 'rooms'
    paginator_class = SafePaginator
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'rooms'
        context['search_form'] = SearchRoomsForm(self.request.GET)
        return context

    def get_queryset(self):
        search_form = SearchRoomsForm(self.request.GET)
        if search_form.is_valid():
            return Room.objects.filter(
                date_deleted=None,
                is_hidden=False,
                main_room=None
            ).order_by('default_price').search(**search_form.cleaned_data)


class RoomDetail(DetailView):
    template_name = 'room/room.html'
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
    permission_required = 'room.view_room'
    template_name = 'room/admin_rooms.html'
    model = Room
    context_object_name = 'rooms'
    paginate_by = 10
    paginator_class = SafePaginator

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'rooms'
        return context

    def get_queryset(self):
        return Room.objects.filter(date_deleted=None, main_room=None)


class AdminRoomDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'room.view_room'
    template_name = 'room/admin_show_room.html'
    model = Room
    pk_url_kwarg = 'room_id'
    context_object_name = 'offer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'rooms'
        context['delete_link'] = self.object.get_admin_delete_url()
        return context

    def get_object(self, queryset=None):
        obj = super(AdminRoomDetail, self).get_object(queryset=queryset)
        if obj.date_deleted or obj.main_room:
            raise Http404()
        return obj


@permission_required('room.change_room')
def admin_edit_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    form_room = RoomForm(request.POST or None, files=request.FILES or None, instance=room)
    PhotoFormset = modelformset_factory(Photo, form=PhotoForm, extra=0, can_delete=True)

    formset = PhotoFormset(request.POST or None, files=request.FILES or None, queryset=room.photos.all())

    form_tags = SearchTagForm(request.POST or None)

    context = {
        'form_offer': form_room,
        'formset': formset,
        'current_page': 'rooms',
        'offer': room,
        'photo_form': zip(formset.queryset, formset.forms),
        'form_tags': form_tags  # пакуем формы и экземпляры модели в один объект, для удобной обработки в темплейте
    }

    if request.method == 'POST':

        if all([form_room.is_valid(), formset.is_valid()]):

            changed_room = form_room.save(commit=True)

            formset.save(commit=False)

            for created_photo in formset.new_objects:
                created_photo.offer = changed_room  # если новая картинки, то присваиваем номер, к которому она относится
                created_photo.save()

            for changed_photo in formset.changed_objects:
                changed_photo[0].save()

            for deleted_photo in formset.deleted_objects:
                deleted_photo.delete()

            success_url = reverse('admin_show_room', kwargs={'room_id': changed_room.pk})
            response_data = {'message': 'successfully updated', 'url': success_url}
            response = HttpResponse(json.dumps(response_data),
                                    content_type="application/json")  # при успехе отправляем json, который обработает ajax
            response.status_code = 302      # 302, т.к. редериктим при успехе на просмотр
            return response

        else:
            response = HttpResponse(form_room.errors.as_json())  # отправляем ошибки в виде json'a
            response.status_code = 400
            return response

    return render(request, 'room/admin_edit_room.html', context)  # если GET, то просто рендерим темплейт


@permission_required('room.add_room')
def admin_create_room(request):
    form_room = RoomForm(request.POST or None, files=request.FILES or None)
    PhotoFormset = modelformset_factory(Photo, form=PhotoForm, extra=0, can_delete=True)

    formset = PhotoFormset(request.POST or None, files=request.FILES or None, queryset=Photo.objects.none())

    context = {
        'form_offer': form_room,
        'list_page': reverse('admin_rooms'),
        'formset': formset,
        'current_page': 'rooms',
    }

    if request.method == 'POST':

        if all([form_room.is_valid(), formset.is_valid()]):

            created_room = form_room.save(commit=True)

            formset.save(commit=False)

            for created_photo in formset.new_objects:
                created_photo.offer = created_room  # если новая картинки, то присваиваем номер, к которому она относится
                created_photo.save()

            success_url = reverse('admin_show_room', kwargs={'room_id': created_room.pk})
            response_data = {'message': 'successfully updated', 'url': success_url}
            response = HttpResponse(json.dumps(response_data),
                                    content_type="application/json")  # при успехе отправляем json, который обработает ajax
            response.status_code = 302      # 302, т.к. редериктим при успехе на просмотр
            return response

        else:
            response = HttpResponse(form_room.errors.as_json())  # отправляем ошибки в виде json'a
            response.status_code = 400
            return response

    return render(request, 'room/admin_create_room.html', context)  # если GET, то просто рендерим темплейт


@permission_required('room.delete_room')
def admin_delete_room(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)
    # ТУТ ВСЯКИЕ ПРОВЕРКИ
    room.date_deleted = datetime.now()
    room.save()
    return redirect('admin_rooms')
