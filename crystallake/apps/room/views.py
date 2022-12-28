import json
from datetime import datetime

from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.http import HttpResponse, Http404


from ..core.utils import SafePaginator, ResponseMessage
from .models import Room
from .forms import RoomForm, SearchRoomsForm
from ..photo.forms import PhotoForm
from ..photo.models import Photo
from ..tag.forms import SearchTagForm
from ..offer.utils import ManageOfferMixin

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
        rooms = Room.objects.filter(
            date_deleted=None,
            is_hidden=False,
            main_room=None
        ).order_by('default_price')

        if search_form.is_valid():
            rooms = rooms.search(**search_form.cleaned_data)

        return rooms


class RoomDetail(DetailView):
    template_name = 'room/room.html'
    model = Room
    slug_url_kwarg = 'room_slug'
    context_object_name = 'offer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'rooms'
        context['familiar'] = self.object.get_familiar()
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
    pk_url_kwarg = 'offer_id'
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


class AdminEditRoomView(ManageOfferMixin, UpdateView):  # TODO: не давать возможность открыть удаленные/дочерние
    model = Room
    template_name = 'room/admin_edit_room.html'
    form_class = RoomForm
    pk_url_kwarg = 'offer_id'
    context_object_name = 'offer'

    def get_context_data(self, **kwargs):
        context = super(AdminEditRoomView, self).get_context_data(**kwargs)
        common_context = self.get_common_context(
            request=self.request,
            photos_qs=self.object.photos.all(),
            form_tags=SearchTagForm(self.request.POST or None),
            current_page='rooms',
        )
        return {**context, **common_context}

    def form_valid(self, form):
        context = self.get_context_data()
        formset_photos = context['formset_photos']
        if formset_photos.is_valid():
            offer = form.instance
            return self.save_offer(
                formset_photos=formset_photos,
                offer=offer
            )

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response


class AdminCreateRoomView(ManageOfferMixin, CreateView):
    model = Room
    template_name = 'room/admin_create_room.html'
    form_class = RoomForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        common_context = self.get_common_context(
            request=self.request,
            photos_qs=Photo.objects.none(),
            current_page='rooms'
        )
        return {**context, **common_context}

    def form_valid(self, form):
        context = self.get_context_data()
        formset_photos = context['formset_photos']
        if formset_photos.is_valid():
            offer = form.instance
            response = self.save_offer(
                formset_photos=formset_photos,
                offer=offer,
            )
            form.instance.create_same_room()
            return response

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response


def create_same_room_view(request, offer_id):
    if request.method == 'POST':
        base_room = get_object_or_404(Room, pk=offer_id, date_deleted=None, main_room=None)
        same_room = base_room.create_same_room()
        data = {'id': same_room.pk}
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
        response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
        return response


def del_same_room_view(request, **kwargs):
    if request.method == 'POST':
        room = get_object_or_404(Room, pk=request.POST['elem_id'], date_deleted=None)
        if room.main_room is None:
            response_message = ResponseMessage(
                status=ResponseMessage.STATUSES.ERROR,
                message=['Нельзя удалить номер-представитель']
            )
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response

        room.mark_as_deleted()

        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
        response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
        return response


@permission_required('room.delete_room')
def admin_delete_room(request, offer_id):
    room = get_object_or_404(Room, pk=offer_id)
    room.mark_as_deleted()
    return redirect('admin_rooms')
