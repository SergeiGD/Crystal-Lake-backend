from django.urls import path, include

from .views import *

urlpatterns = [
    path('', AdminRoomsList.as_view(), name='admin_rooms'),
    path('show/<int:offer_id>/', AdminRoomDetail.as_view(), name='admin_show_room'),
    path('show/<int:offer_id>/get_busy_dates/<int:room_id>/', get_busy_dates_view, name='get_busy_dates'),
    path('show/<int:offer_id>/get_general_busy_dates/', get_general_busy_dates_view, name='get_general_busy_dates'),
    path('edit/<int:offer_id>/', AdminUpdateRoom.as_view(), name='admin_edit_room'),
    path('edit/<int:offer_id>/', include('apps.offer.admin_urls')),
    path('edit/<int:offer_id>/', include('apps.room.same_rooms_url')),
    path('delete/<int:offer_id>/', admin_delete_room, name='admin_delete_room'),
    path('create/', AdminCreateRoom.as_view(), name='admin_create_room'),
]