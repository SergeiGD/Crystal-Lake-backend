from datetime import datetime, timedelta
import json
import pytz
from django.core.exceptions import PermissionDenied

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils import timezone
from django.template.loader import render_to_string
from django.urls import reverse
from django.middleware.csrf import get_token

from .models import Service, ServiceTimetable
from ..core.utils import SafePaginator, ResponseMessage, get_paginator_data, is_ajax, ClientContextMixin, RelocateResponseMixin
from .forms import SearchServicesForm, ServiceForm, TimetableForm, BookServiceForm, SearchServicesAdmin, SearchTimetablesAdmin
from ..offer.utils import ManageOfferMixin, CartMixin
from ..photo.models import Photo
from ..tag.forms import SearchTagForm
from ..user.forms import SearchUserForm
from ..worker.models import Worker
from ..order.models import PurchaseCountable
from django.conf import settings
from ..order.utils import ServicePurchaseMixin

# Create your views here.


class ServiceDetail(ServicePurchaseMixin, CartMixin, ClientContextMixin, RelocateResponseMixin, DetailView):
    template_name = 'service/service.html'
    model = Service
    slug_url_kwarg = 'service_slug'
    context_object_name = 'offer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'services'
        context['familiar'] = self.object.get_familiar()
        context['book_form'] = BookServiceForm(self.request.POST, user=self.request.user)
        return {**context, **self.get_general_context()}

    def get_object(self, queryset=None):
        obj = super(ServiceDetail, self).get_object(queryset=queryset)
        if obj.date_deleted or obj.is_hidden:
            raise Http404()
        return obj

    def post(self, request, **kwargs):
        book_form = BookServiceForm(self.request.POST, user=self.request.user)
        if book_form.is_valid():
            try:
                cart = self.get_cart(self.request)
            except PermissionDenied:
                response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
                    'Неверные данные': ['Пользователь с этим телефоном зерегестрирован. Сначала авторизируйтесь']
                })
                response = HttpResponse(response_message.get_json(), status=401, content_type='application/json')
                return response
            purchase = PurchaseCountable(order=cart, offer=self.get_object())
            purchase.start, purchase.end = self.aware_time(
                book_form.cleaned_data['date'],
                book_form.cleaned_data['time_start'],
                book_form.cleaned_data['time_end'],
            )
            purchase.quantity = book_form.cleaned_data['quantity']
            return self.manage_service_purchase(purchase, success_url=reverse('cart'))
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=book_form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


class ServicesCatalog(ClientContextMixin, ListView):
    model = Service
    context_object_name = 'services'
    paginator_class = SafePaginator
    paginate_by = settings.CLIENT_PAGINATE_BY
    template_name = 'service/services.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'services'
        context['search_form'] = SearchServicesForm(self.request.GET)
        if len(self.get_queryset()) > self.paginate_by:
            context['paginate_by_range'] = range(self.paginate_by)
        else:
            context['paginate_by_range'] = range(len(self.get_queryset()))
        context['paginate_by'] = self.paginate_by
        return {**context, **self.get_general_context()}

    def get_queryset(self):
        search_form = SearchServicesForm(self.request.GET)
        services = Service.objects.filter(
            date_deleted=None,
            is_hidden=False,
        ).order_by('default_price')

        if search_form.is_valid():
            services = services.search(**search_form.cleaned_data)

        return services


class AdminServicesList(ListView):
    model = Service
    template_name = 'service/admin_services.html'
    context_object_name = 'services'
    paginator_class = SafePaginator
    paginate_by = settings.ADMIN_PAGINATE_BY

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'services'
        context['form_services'] = SearchServicesAdmin(self.request.GET)
        return context

    def get_queryset(self):
        search_form = SearchServicesAdmin(self.request.GET)
        services = Service.objects.filter(date_deleted=None)

        if search_form.is_valid():
            services = services.search(**search_form.cleaned_data)

        return services


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
            form_timetables=SearchTimetablesAdmin(self.request.GET or None),
            form_edit_timetable=TimetableForm(prefix='edit'),
            form_create_timetable=TimetableForm(prefix='create'),
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

    def get_object(self, queryset=None):
        obj = super(AdminUpdateService, self).get_object(queryset=queryset)
        if obj.date_deleted:
            raise Http404()
        return obj


def admin_delete_service(request, offer_id):
    service = get_object_or_404(Service, pk=offer_id)
    service.date_deleted = datetime.now()
    service.save()
    return redirect('admin_services')


def create_timetable_view(request, offer_id):
    if request.POST:
        service = get_object_or_404(Service, pk=offer_id)
        timetable = ServiceTimetable(service=service)
        form = TimetableForm(request.POST or None, prefix='create', instance=timetable)

        if form.is_valid():
            start = datetime.combine(form.cleaned_data['date'], form.cleaned_data['start'])
            end = datetime.combine(form.cleaned_data['date'], form.cleaned_data['end'])
            start, end = timezone.make_aware(start), timezone.make_aware(end)

            workers = json.loads(request.POST.get('workers'))

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

            remaining_objects = set(added_workers) - set(removed_worker)
            if len(remaining_objects) == 0:
                response_message = ResponseMessage(
                    status=ResponseMessage.STATUSES.ERROR,
                    message={'Сотрудники': ['Добавите как минимум одного сотрудника']}
                )
                response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
                return response

            timetable.save()

            timetable.workers.add(*remaining_objects)

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


def edit_timetable_view(request, **kwargs):
    if request.POST:
        timetable = get_object_or_404(ServiceTimetable, pk=request.POST.get('edit-timetable_id'))
        form = TimetableForm(request.POST or None, prefix='edit', instance=timetable)

        if form.is_valid():
            # TODO: СДЕЛАТЬ МИКСИН
            start = datetime.combine(form.cleaned_data['date'], form.cleaned_data['start'])
            end = datetime.combine(form.cleaned_data['date'], form.cleaned_data['end'])
            start, end = timezone.make_aware(start), timezone.make_aware(end)

            workers = json.loads(request.POST.get('workers'))

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
            timetable.workers.add(*remaining_objects)

            response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
            response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
            return response
        else:
            response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message=form.errors)
            response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
            return response


def delete_timetable_view(request, **kwargs):
    timetable = get_object_or_404(ServiceTimetable, pk=request.POST.get('elem_id'))
    if timetable.get_purchases().exists():
        response_message = ResponseMessage(
            status=ResponseMessage.STATUSES.ERROR,
            message={'Заказы': ['Нельзя удалить расписание, на которые забронированы услуги']}
        )
        response = HttpResponse(response_message.get_json(), status=400, content_type='application/json')
        return response
    else:
        timetable.delete()
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
        response = HttpResponse(response_message.get_json(), status=200, content_type='application/json')
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

    if is_ajax(request):
        popup_to_open = request.POST.get('popup_to_open')
        # TODO: тут можно кидать нужны кнопки или нет
        html = render_to_string('core/services_body.html', {'services_list': services_page.object_list, 'popup_to_open': popup_to_open})
        data['items'] = html
    else:
        for service in services_page.object_list:
            item = {
                'name': service.name,
                'id': service.pk,
                'max_in_group': service.max_in_group,
                'link': service.get_admin_show_url(),
                'default_price': service.default_price,
            }
            data['items'].append(item)

    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
    return HttpResponse(response_message.get_json(), content_type='application/json', status=200)


def find_timetables(request, offer_id):
    timetables = ServiceTimetable.objects.filter(service_id=offer_id).search(
        **request.POST.dict()
    )

    timetables_page, num_pages = get_paginator_data(timetables, request.POST.get('page_number', 1))

    data = {'pages': {
        'pages_count': num_pages,
        'current_page': timetables_page.number,
    }, 'items': []}

    if is_ajax(request):
        html = render_to_string('core/timetables_body.html', {'timetables_list': timetables_page.object_list, 'token': get_token(request)})
        data['items'] = html
    else:
        for timetable in timetables_page.object_list:
            item = {
                'start': timetable.start,
                'end': timetable.end,
            }
            data['items'].append(item)

    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
    return HttpResponse(response_message.get_json(), content_type='application/json', status=200)
    # for timetable in timetables_page.object_list:
    #     start_unix_seconds = (timetable.start - timezone.make_aware(datetime(1970, 1, 1))).total_seconds()
    #     end_unix_seconds = (timetable.end - timezone.make_aware(datetime(1970, 1, 1))).total_seconds()
    #     item = {
    #         'start': start_unix_seconds,
    #         'end': end_unix_seconds,
    #         'id': timetable.pk
    #     }
    #     data['items'].append(item)
    #
    # response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
    # return HttpResponse(response_message.get_json(), content_type='application/json', status=200)


def get_free_time_view(request, offer_id, **kwargs):
    # TODO: перенести в миксин
    service = get_object_or_404(Service, pk=offer_id)
    start_timestamp = request.GET.get('start', 0)
    end_timestamp = request.GET.get('end', 0)
    if start_timestamp == 0 or end_timestamp == 0:
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.ERROR, message={
            'Расписание услуги': ['Невозможно получить данные по выбранной дате']
        })
        return HttpResponse(response_message.get_json(), content_type='application/json', status=400)
    start_timestamp = int(start_timestamp) / 1000        # питон принимает в секундах, а не милисекундах
    end_timestamp = int(end_timestamp) / 1000
    start = datetime.fromtimestamp(start_timestamp, tz=pytz.UTC)    # приходит время в UTC
    end = datetime.fromtimestamp(end_timestamp, tz=pytz.UTC)

    dates = service.get_free_time(timezone.localtime(start), timezone.localtime(end))   # конвертим в локальное время при вызове
    # for data in dates:
    #     print(data)
    response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=dates)
    return HttpResponse(response_message.get_json(), content_type='application/json', status=200)

