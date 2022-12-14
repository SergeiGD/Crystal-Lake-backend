from django.urls import path

from .views import *

urlpatterns = [
    path('', AdminRoomsList.as_view(), name='admin_rooms'),
    path('<slug:room_slug>/', AdminRoomDetail.as_view(), name='admin_show_room'),
    path('<slug:room_slug>/edit/', admin_edit_room, name='admin_edit_room'),
]
