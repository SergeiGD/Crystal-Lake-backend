from django.contrib.auth import login, authenticate
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.utils.timezone import now
from django.contrib.auth.backends import AllowAllUsersModelBackend

from ..core.utils import ResponseMessage
from ..photo.models import Photo
from ..photo.forms import PhotoForm
from ..order.models import Order
from ..client_profile.utils import PhoneCheckMixin
from ..client.models import Client
from django.conf import settings


class ManageOfferMixin:
    def save_offer(self, **kwargs):
        formset_photos = kwargs['formset_photos']

        offer = kwargs['offer']

        offer.save()
        formset_photos.save(commit=False)

        for created_photo in formset_photos.new_objects:
            created_photo.offer = offer  # если новая картинки, то присваиваем номер, к которому она относится
            created_photo.save()

        for changed_photo in formset_photos.changed_objects:
            changed_photo[0].save()

        for deleted_photo in formset_photos.deleted_objects:
            deleted_photo.delete()

        success_url = offer.get_admin_show_url()
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=success_url)
        response = HttpResponse(response_message.get_json(), status=302, content_type='application/json')
        return response

    def get_common_context(self, request, photos_qs, **kwargs):
        context = kwargs
        PhotoFormset = modelformset_factory(Photo, form=PhotoForm, extra=0, can_delete=True)
        context['formset_photos'] = PhotoFormset(
            request.POST or None,
            files=request.FILES or None,
            queryset=photos_qs
        )
        context['photo_form'] = zip(context['formset_photos'].queryset, context['formset_photos'].forms)
        return context


class CartMixin(PhoneCheckMixin):
    def get_cart(self, request):
        if request.user.is_authenticated:
            client = request.user
        else:
            phone = request.POST['phone']
            if self.is_phone_in_use(phone):
                raise PermissionDenied('Пользователь с этим телефоном зерегестрирован. Сначала авторизируйтесь')
            if self.is_phone_registered(phone):
                client = Client.objects.get(phone=phone)
            else:
                client = Client.objects.create(phone=phone, is_active=False)
                client.save()
            login(request, client, backend=settings.AUTHENTICATION_BACKENDS[1])

        cart_order = Order.objects.filter(
            client__id=client.id,
            paid=0, refunded=0,
            date_canceled=None,
            date_finished=None
        ).first()
        if cart_order is None:
            cart_order = Order(client=client, date_create=now())
            cart_order.save()

        return cart_order
