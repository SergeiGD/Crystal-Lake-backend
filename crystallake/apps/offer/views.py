import json
from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, Http404, JsonResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from .forms import *
from django.db import connection
from ..core.save_paginator import SafePaginator
from ..tag.forms import SearchTagForm
from PIL import Image


# Create your views here.

# class SafePaginator(Paginator):
#     def validate_number(self, number):
#         try:
#             return super(SafePaginator, self).validate_number(number)
#         except EmptyPage:
#             if number > 1:
#                 return self.num_pages
#             else:
#                 return 1


# class RoomsCatalog(ListView):
#     template_name = 'offer/rooms.html'
#     model = Room
#     context_object_name = 'rooms'
#     paginator_class = SafePaginator
#     paginate_by = 1
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['current_page'] = 'rooms'
#         context['search_form'] = SearchRoomsForm(self.request.GET)
#         return context
#
#     def get_queryset(self):
#         search_form = SearchRoomsForm(self.request.GET)
#         if search_form.is_valid():
#             return Room.objects.filter(
#                 date_deleted=None,
#                 is_hidden=False,
#                 main_room=None
#             ).order_by('default_price').search(**search_form.cleaned_data)
#
#
# class RoomDetail(DetailView):
#     template_name = 'offer/room.html'
#     model = Room
#     slug_url_kwarg = 'room_slug'
#     context_object_name = 'offer'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['current_page'] = 'rooms'
#         return context
#
#     def get_object(self, queryset=None):
#         obj = super(RoomDetail, self).get_object(queryset=queryset)
#         if obj.date_deleted or obj.is_hidden or obj.main_room:
#             raise Http404()
#         return obj
#
#
# class AdminRoomsList(PermissionRequiredMixin, ListView):
#     permission_required = 'offer.view_room'
#     template_name = 'offer/admin_rooms.html'
#     model = Room
#     context_object_name = 'rooms'
#     paginate_by = 10
#     paginator_class = SafePaginator
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['current_page'] = 'rooms'
#         return context
#
#     def get_queryset(self):
#         return Room.objects.filter(date_deleted=None, main_room=None)
#
#
# class AdminRoomDetail(PermissionRequiredMixin, DetailView):
#     permission_required = 'offer.view_room'
#     template_name = 'offer/admin_show_room.html'
#     model = Room
#     slug_url_kwarg = 'room_slug'
#     context_object_name = 'offer'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['current_page'] = 'rooms'
#         context['delete_link'] = self.object.get_admin_delete_url()
#         return context
#
#     def get_object(self, queryset=None):
#         obj = super(AdminRoomDetail, self).get_object(queryset=queryset)
#         if obj.date_deleted or obj.main_room:
#             raise Http404()
#         return obj
#
#
# @permission_required('offer.change_room')
# def admin_edit_room(request, room_slug):
#     room = get_object_or_404(Room, slug=room_slug)
#
#     form_room = RoomForm(request.POST or None, files=request.FILES or None, instance=room)
#     PhotoFormset = modelformset_factory(Photo, form=PhotoForm, extra=0, can_delete=True)
#
#     formset = PhotoFormset(request.POST or None, files=request.FILES or None, queryset=room.photos.all())
#
#     form_tags = SearchTagForm(request.POST or None)
#
#     context = {
#         'form_room': form_room,
#         'formset': formset,
#         'current_page': 'rooms',
#         'room': room,
#         'photo_form': zip(formset.queryset, formset.forms),
#         # пакуем формы и экземпляры модели в один объект, для удобной обработки в темплейте
#         'form_tags': form_tags
#     }
#
#     if request.method == 'POST':
#
#         if all([form_room.is_valid(), formset.is_valid()]):
#
#             changed_room = form_room.save(commit=True)
#
#             formset.save(commit=False)
#
#             for created_photo in formset.new_objects:
#                 created_photo.offer = changed_room  # если новая картинки, то присваиваем номер, к которому она относится
#                 created_photo.save()
#
#             for changed_photo in formset.changed_objects:
#                 changed_photo[0].save()
#
#             for deleted_photo in formset.deleted_objects:
#                 deleted_photo.delete()
#
#             success_url = reverse('admin_show_room', kwargs={'room_slug': changed_room.slug})
#             response_data = {'message': 'successfully updated', 'url': success_url}
#             response = HttpResponse(json.dumps(response_data),
#                                     content_type="application/json")  # при успехе отправляем json, который обработает ajax
#             response.status_code = 302  # 302, т.к. редериктим при успехе на просмотр
#             return response
#
#         else:
#             response = HttpResponse(form_room.errors.as_json())  # отправляем ошибки в виде json'a
#             response.status_code = 400
#             return response
#
#     return render(request, 'offer/admin_edit_room.html', context)  # если GET, то просто рендерим темплейт
#
#
# @permission_required('offer.add_room')
# def admin_create_room(request):
#     form_room = RoomForm(request.POST or None, files=request.FILES or None)
#     PhotoFormset = modelformset_factory(Photo, form=PhotoForm, extra=0, can_delete=True)
#
#     formset = PhotoFormset(request.POST or None, files=request.FILES or None, queryset=Photo.objects.none())
#
#     context = {
#         'form_room': form_room,
#         'formset': formset,
#         'current_page': 'rooms',
#     }
#
#     if request.method == 'POST':
#
#         if all([form_room.is_valid(), formset.is_valid()]):
#
#             created_room = form_room.save(commit=True)
#
#             formset.save(commit=False)
#
#             for created_photo in formset.new_objects:
#                 created_photo.offer = created_room  # если новая картинки, то присваиваем номер, к которому она относится
#                 created_photo.save()
#
#
#             success_url = reverse('admin_show_room', kwargs={'room_slug': created_room.slug})
#             response_data = {'message': 'successfully updated', 'url': success_url}
#             response = HttpResponse(json.dumps(response_data),
#                                     content_type="application/json")  # при успехе отправляем json, который обработает ajax
#             response.status_code = 200  # 302, т.к. редериктим при успехе на просмотр
#             return response
#
#         else:
#             response = HttpResponse(form_room.errors.as_json())  # отправляем ошибки в виде json'a
#             response.status_code = 400
#             return response
#
#     return render(request, 'offer/admin_create_room.html', context)  # если GET, то просто рендерим темплейт
#
#
# @permission_required('offer.delete_room')
# def admin_delete_room(request, room_slug):
#     room = get_object_or_404(Room, slug=room_slug)
#     # ТУТ ВСЯКИЕ ПРОВЕРКИ
#     room.date_deleted = datetime.now()
#     room.save()
#     return redirect('admin_rooms')


def get_unattached_tags(request, offer_id):
    if request.method == 'POST':
        print(request.POST)
        offer = get_object_or_404(Offer, pk=offer_id)
        tags = Tag.objects.exclude(pk__in=[offer.tags.values('pk')]).search(**request.POST.dict())
        tags_paginator = SafePaginator(tags, 1)
        page = request.POST.get('page_number', 1)
        tags_page = tags_paginator.get_page(page)
        num_pages = tags_paginator.num_pages

        data = {'pages': {
            'pages_count': num_pages,
            'current_page': tags_page.number,
        }, 'tags': []}

        for tag in tags_page.object_list:
            item = {'name': tag.name, 'id': tag.pk}
            data['tags'].append(item)

        return HttpResponse(json.dumps(data), content_type="application/json", status=200)


def add_tag_to_offer(request, offer_id):
    if request.method == 'POST':
        offer = get_object_or_404(Offer, pk=offer_id)
        tag_id = request.POST.get('tag_id', -1)
        tag = get_object_or_404(Tag, pk=tag_id)
        offer.tags.add(tag)
        offer.save()
        #data = serializers.serialize('json', [tag])
        data = {'name': tag.name, 'id': tag.pk, 'link': tag.get_admin_show_url()}
        return HttpResponse(json.dumps(data), content_type="application/json", status=200)


def del_tag_from_offer(request, offer_id):
    if request.method == 'POST':
        offer = get_object_or_404(Offer, pk=offer_id)
        tag_id = request.POST.get('tag_id', -1)
        tag = get_object_or_404(Tag, pk=tag_id)
        offer.tags.remove(tag)
        offer.save()
        data = serializers.serialize('json', [tag])
        return HttpResponse(data, content_type="application/json", status=200)


# @csrf_exempt
# def resize_image(request):
#     print('sss')
#     if request.method == 'POST':
#         print(request.FILES)
#         file = request.FILES['image']
#         print(file.file)
#         # img = Image.open(file)
#         # img.thumbnail((300, 300))
#         #return HttpResponse(img, content_type='image/jpeg')
#         #with open(file, "rb") as f:
#         #return HttpResponse(file.read(), content_type="image/jpeg")
#         return FileResponse(file.file)
