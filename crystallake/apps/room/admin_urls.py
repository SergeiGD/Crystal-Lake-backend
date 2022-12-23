from django.urls import path

from .views import *

urlpatterns = [
    path('', AdminRoomsList.as_view(), name='admin_rooms'),
    path('show/<int:room_id>/', AdminRoomDetail.as_view(), name='admin_show_room'),
    path('edit/<int:room_id>/', admin_edit_room, name='admin_edit_room'),
    path('delete/<int:room_id>/', admin_delete_room, name='admin_delete_room'),
    path('create/', admin_create_room, name='admin_create_room'),
]