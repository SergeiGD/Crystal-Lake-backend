from datetime import datetime

from django.forms import modelformset_factory
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .models import Service
from ..core.utils import SafePaginator, ResponseMessage
from .forms import SearchServicesForm, ServiceForm
from ..offer.utils import ManageOfferMixin
from ..photo.forms import PhotoForm
from ..photo.models import Photo
from ..tag.forms import SearchTagForm

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


class AdminCreateServiceView(ManageOfferMixin, CreateView):
    model = Service
    template_name = 'service/admin_create_service.html'
    form_class = ServiceForm

    def get_context_data(self, **kwargs):
        context = super(AdminCreateServiceView, self).get_context_data(**kwargs)
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


class AdminEditServiceView(ManageOfferMixin, UpdateView):
    model = Service
    template_name = 'service/admin_edit_service.html'
    form_class = ServiceForm
    pk_url_kwarg = 'offer_id'
    context_object_name = 'offer'

    def get_context_data(self, **kwargs):
        context = super(AdminEditServiceView, self).get_context_data(**kwargs)
        common_context = self.get_common_context(
            request=self.request,
            photos_qs=self.object.photos.all(),
            form_tags=SearchTagForm(self.request.POST or None),
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


def admin_delete_service(request, offer_id):
    service = get_object_or_404(Service, pk=offer_id)
    service.date_deleted = datetime.now()
    service.save()
    return redirect('admin_services')

