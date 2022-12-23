import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from ..core.save_paginator import SafePaginator
from ..tag.models import Tag
from .models import Offer


# Create your views here.

def get_unattached_tags(request, offer_id):
    if request.method == 'POST':
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
