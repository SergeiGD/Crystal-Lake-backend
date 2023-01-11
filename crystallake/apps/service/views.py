from datetime import datetime
import json

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils import timezone

from .models import Service, ServiceTimetable
from ..core.utils import SafePaginator, ResponseMessage, get_paginator_data, RelocateResponseMixin
from .forms import SearchServicesForm, ServiceForm, TimetableForm
from ..offer.utils import ManageOfferMixin
from ..photo.forms import PhotoForm
from ..photo.models import Photo
from ..tag.forms import SearchTagForm
from ..user.forms import SearchUserForm
from ..worker.models import Worker

# Create your views here.


class ServiceDetail(DetailView):
    template_name = 'service/service.html'
    model = Service
    slug_url_kwarg = 'service_slug'
    context_object_name = 'offer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'services'
        context['familiar'] = self.object.get_familiar()
        return context

    def get_object(self, queryset=None):
        obj = super(ServiceDetail, self).get_object(queryset=queryset)
        if obj.date_deleted or obj.is_hidden:
            raise Http404()
        return obj


class ServicesCatalog(ListView):
    model = Service
    context_object_name = 'services'
    paginator_class = SafePaginator
    paginate_by = 1
    template_name = 'service/services.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'services'
        context['search_form'] = SearchServicesForm(self.request.GET)
        return context

    def get_queryset(self):
        search_form = SearchServicesForm(self.request.GET)
        services = Service.objects.filter(
            date_deleted=None,
            is_hidden=False,
        )

        if search_form.is_valid():
            services = services.search(**search_form.cleaned_data)

        return services


class AdminServicesList(ListView):
    model = Service
    template_name = 'service/admin_services.html'
    context_object_name = 'services'
    paginator_class = SafePaginator
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'services'
        return context

    def get_queryset(self):
        return Service.objects.filter(date_deleted=None)


class AdminCreateService(ManageOfferMixin, CreateView):
    model = Service
    template_name = 'service/admin_create_service.html'
    form_class = ServiceForm

    def get_context_data(self, **kwargs):
        context = super(AdminCreateService, self).get_context_data(**kwargs)
        common_context = self.get_common_context(
            request=self.request,
            photos_qs=Photo.objects.none(),
            current_page='services'
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


class AdminServiceDetail(DetailView):
    template_name = 'service/admin_show_service.html'
    model = Service
    pk_url_kwarg = 'offer_id'
    context_object_name = 'offer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'services'
        context['delete_link'] = self.object.get_admin_delete_url()
        return context

    def get_object(self, queryset=None):
        obj = super(AdminServiceDetail, self).get_object(queryset=queryset)
        if obj.date_deleted:
            raise Http404()
        return obj


class AdminUpdateService(ManageOfferMixin, UpdateView):
    model = Service
    template_name = 'service/admin_edit_service.html'
    form_class = ServiceForm
    pk_url_kwarg = 'offer_id'
    context_object_name = 'offer'

    def get_context_data(self, **kwargs):
        context = super(AdminUpdateService, self).get_context_data(**kwargs)
        common_context = self.get_common_context(
            request=self.request,
            photos_qs=self.object.photos.all(),
            form_tags=SearchTagForm(self.request.POST or None),
            current_page='services',
            form_timetable=TimetableForm(),
            form_workers=SearchUserForm()
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


def admin_delete_service(request, offer_id):
    service = get_object_or_404(Service, pk=offer_id)
    service.date_deleted = datetime.now()
    service.save()
    return redirect('admin_services')


def manage_timetable_view(request, offer_id):
    if request.POST:
        service = get_object_or_404(Service, pk=offer_id)

        timetable_id = request.POST['timetable_id'] if request.POST['timetable_id'] else -1
        timetable = ServiceTimetable.objects.filter(pk=timetable_id).first()

        form = TimetableForm(request.POST or None)
        if form.is_valid():
            workers = json.loads(request.POST.get('workers'))
            date_str = request.POST.get('date')
            start_time_str = request.POST.get('start')
            end_time_str = request.POST.get('end')
            start_str = date_str + '/' + start_time_str
            end_str = date_str + '/' + end_time_str


            start = datetime.strptime(start_str, '%Y-%m-%d/%H:%M')
            end = datetime.strptime(end_str, '%Y-%m-%d/%H:%M')

            start = timezone.make_aware(start)
            end = timezone.make_aware(end)

            if not timetable:
                timetable = ServiceTimetable(service=service)

            timetable.start = start
            timetable.end = end

            added_workers = []
            removed_worker = []

            for worker_id, added in workers.items():
                worker = get_object_or_404(Worker, pk=worker_id)
                if added:
                    added_workers.append(worker)
                else:
                    removed_worker.append(worker)

            remaining_objects = set(list(timetable.workers.all()) + added_workers) - set(removed_worker)
            if len(remaining_objects) == 0:
                response_message = ResponseMessage(
                    status=ResponseMessage.STATUSES.ERROR,
                    message={'Сотрудники': ['Добавите как минимум одного сотрудника']}
                )
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response

            timetable.save()
            timetable.workers.clear()
            for worker in remaining_objects:
                timetable.workers.add(worker)

            response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
            response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
            return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


def get_timetable_info_view(request, timetable_id, **kwargs):
    timetable = get_object_or_404(ServiceTimetable, pk=timetable_id)
    data = timetable.get_info()
    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
    response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
    return response


def edit_timetable_view(request, offer_id):
    if request.POST:

        timetable_id = request.POST['timetable_id'] if request.POST['timetable_id'] else -1
        timetable = get_object_or_404(ServiceTimetable, pk=timetable_id)

        form = TimetableForm(request.POST or None)    # если purchase_id не передан, то будет None -> новый объект
        if form.is_valid():
            workers = json.loads(request.POST.get('workers'))
            date_str = request.POST.get('date')
            start_time_str = request.POST.get('start')
            end_time_str = request.POST.get('end')
            start_str = date_str + '/' + start_time_str
            end_str = date_str + '/' + end_time_str

            start = datetime.strptime(start_str, '%Y-%m-%d/%H:%M')
            end = datetime.strptime(end_str, '%Y-%m-%d/%H:%M')

            timetable.start = start
            timetable.end = end


            response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
            response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
            return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


def find_services(request, **kwargs):
    services = Service.objects.filter(date_deleted=None, is_hidden=False).search(
        **request.POST.dict()
    )

    services_page, num_pages = get_paginator_data(services, request.POST.get('page_number', 1))

    data = {'pages': {
        'pages_count': num_pages,
        'current_page': services_page.number,
    }, 'items': []}
    for service in services_page.object_list:
        item = {
            'name': service.name,
            'id': service.pk,
            'dynamic_timetable': service.dynamic_timetable,
            'max_for_moment': service.max_for_moment,
            'link': service.get_admin_show_url(),
            'default_price': service.default_price,
            'weekend_price': service.weekend_price
        }
        data['items'].append(item)

    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
    return HttpResponse(response_message.get_json(), content_type='application/json', status=200)


def find_timetables(request, **kwargs):
    # service_id = request.POST.get('service_id', -1)
    # service = get_object_or_404(Service, pk=service_id)
    # service.timetables.filter(date_deleted=None, is_hidden=False).search(
    #     **request.POST.dict()
    # )
    timetables = ServiceTimetable.objects.filter().search(
        **request.POST.dict()
    )

    timetables_page, num_pages = get_paginator_data(timetables, request.POST.get('page_number', 1))

    data = {'pages': {
        'pages_count': num_pages,
        'current_page': timetables_page.number,
    }, 'items': []}
    for timetable in timetables_page.object_list:
        print(timetable.start)
        start_unix_seconds = (timetable.start - timezone.make_aware(datetime(1970, 1, 1))).total_seconds()
        end_unix_seconds = (timetable.end - timezone.make_aware(datetime(1970, 1, 1))).total_seconds()
        item = {
            'start': start_unix_seconds,
            'end': end_unix_seconds,
            'id': timetable.pk
        }
        data['items'].append(item)

    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
    return HttpResponse(response_message.get_json(), content_type='application/json', status=200)


class AdminTimetablesList(ListView):
    model = ServiceTimetable
    template_name = 'service/admin_timetables.html'
    context_object_name = 'timetables'
    paginate_by = 10
    paginator_class = SafePaginator

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'timetables'
        return context


class AdminTimetableDetail(DetailView):
    model = ServiceTimetable
    template_name = 'service/admin_show_timetable.html'
    context_object_name = 'timetable'
    pk_url_kwarg = 'timetable_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'timetables'
        context['delete_link'] = self.object.get_admin_delete_url()
        context['workers'] = self.object.workers.all()
        return context


class AdminTimetableUpdate(RelocateResponseMixin, UpdateView):
    model = ServiceTimetable
    template_name = 'service/admin_edit_timetable.html'
    context_object_name = 'timetable'
    pk_url_kwarg = 'timetable_id'
    form_class = TimetableForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'timetables'
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        form.instance.save()
        return self.relocate(form.instance.get_admin_show_url())


class AdminTimetableCreate(RelocateResponseMixin, CreateView):
    model = ServiceTimetable
    template_name = 'service/admin_create_timetable.html'
    context_object_name = 'timetable'
    form_class = TimetableForm

    def get_success_url(self):
        return self.object.get_admin_show_url()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'timetables'
        return context

    def form_invalid(self, form):
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response

    def form_valid(self, form):
        form.instance.save()
        return self.relocate(form.instance.get_admin_show_url())

