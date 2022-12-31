from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from ..core.utils import SafePaginator, ResponseMessage
from ..tag.models import Tag
from .models import Offer


# Create your views here.

def get_unattached_tags(request, offer_id):
    if request.method == 'POST':
        offer = get_object_or_404(Offer, pk=offer_id)
        tags = Tag.objects.exclude(pk__in=offer.tags.values('pk')).search(**request.POST.dict())
        tags_paginator = SafePaginator(tags, 1)
        page = request.POST.get('page_number', 1)
        tags_page = tags_paginator.get_page(page)
        num_pages = tags_paginator.num_pages

        data = {'pages': {
            'pages_count': num_pages,
            'current_page': tags_page.number,
        }, 'tags': []}
        for tag in tags_page.object_list:
            item = {'name': tag.name, 'id': tag.pk, 'link': tag.get_admin_show_url()}
            data['tags'].append(item)

        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
        return HttpResponse(response_message.get_json(), content_type='application/json', status=200)


def add_tag_to_offer(request, offer_id):
    if request.method == 'POST':
        offer = get_object_or_404(Offer, pk=offer_id)
        tag_id = request.POST.get('elem_id', -1)
        tag = get_object_or_404(Tag, pk=tag_id)
        offer.tags.add(tag)
        offer.save()
        data = {'name': tag.name, 'id': tag.pk, 'link': tag.get_admin_show_url()}
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK, data=data)
        return HttpResponse(response_message.get_json(), content_type='application/json', status=200)


def del_tag_from_offer(request, offer_id):
    if request.method == 'POST':
        offer = get_object_or_404(Offer, pk=offer_id)
        tag_id = request.POST.get('elem_id', -1)
        tag = get_object_or_404(Tag, pk=tag_id)
        offer.tags.remove(tag)
        offer.save()
        response_message = ResponseMessage(status=ResponseMessage.STATUSES.OK)
        return HttpResponse(response_message.get_json(), content_type='application/json', status=200)

