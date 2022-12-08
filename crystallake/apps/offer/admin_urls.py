from django.urls import path

from .views import *

urlpatterns = [
    path('', AdminRoomsList.as_view(), name='admin_rooms'),
    path('room/<slug:room_slug>/', AdminRoomDetail.as_view(), name='admin_show_room'),
]
