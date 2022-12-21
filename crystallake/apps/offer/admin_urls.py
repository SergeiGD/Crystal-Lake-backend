from django.urls import path

from .views import *

urlpatterns = [
    path('', AdminRoomsList.as_view(), name='admin_rooms'),
    path('show/<slug:room_slug>/', AdminRoomDetail.as_view(), name='admin_show_room'),
    path('edit/<slug:room_slug>/', admin_edit_room, name='admin_edit_room'),
    path('delete/<slug:room_slug>/', admin_delete_room, name='admin_delete_room'),
    path('create/', admin_create_room, name='admin_create_room'),
    path('get_tags/<int:offer_id>', get_tags, name='get_tags'),
    path('tag_to_offer/<int:offer_id>/', add_tag_to_offer, name='tag_to_offer'),
    path('tag_from_offer/<int:offer_id>/', del_tag_from_offer, name='tag_from_offer'),
]
