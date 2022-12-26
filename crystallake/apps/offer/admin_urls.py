from django.urls import path

from .views import add_tag_to_offer, del_tag_from_offer, get_unattached_tags

urlpatterns = [
    path('add_tag/', add_tag_to_offer, name='add_tag_to_offer'),
    path('del_tag/', del_tag_from_offer, name='del_tag_from_offer'),
    path('get_unattached_tags/', get_unattached_tags, name='get_unattached_tags'),
]
