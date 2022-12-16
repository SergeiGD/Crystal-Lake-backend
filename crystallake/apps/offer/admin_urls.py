from django.urls import path

from .views import *

urlpatterns = [
    path('', AdminRoomsList.as_view(), name='admin_rooms'),
    path('show/<slug:room_slug>/', AdminRoomDetail.as_view(), name='admin_show_room'),
    path('edit/<slug:room_slug>/', admin_edit_room, name='admin_edit_room'),
    path('create/', admin_create_room, name='admin_create_room'),
]
