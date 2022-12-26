from django.forms import modelformset_factory
from django.http import HttpResponse

from ..core.utils import ResponseMessage
from ..photo.models import Photo
from ..photo.forms import PhotoForm


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
