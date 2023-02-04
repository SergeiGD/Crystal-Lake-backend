from django import template


register = template.Library()


@register.filter
def offer_type(obj):
    return obj.__class__.__name__


@register.filter
def index(iterable, i):
    return iterable[i]


@register.simple_tag
def get_position(elem_index, page_num, paginate_by):
    return elem_index + 1 + ((page_num - 1) * paginate_by)
