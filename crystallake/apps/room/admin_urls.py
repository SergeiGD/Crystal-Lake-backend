from django.urls import path, include

from .views import *

urlpatterns = [
    path('', AdminRoomsList.as_view(), name='admin_rooms'),
    path('show/<int:offer_id>/', AdminRoomDetail.as_view(), name='admin_show_room'),
    path('edit/<int:offer_id>/', AdminEditRoomView.as_view(), name='admin_edit_room'),
    path('edit/<int:offer_id>/', include('apps.offer.admin_urls')),
    path('edit/<int:offer_id>/', include('apps.room.same_rooms_url')),
    path('delete/<int:offer_id>/', admin_delete_room, name='admin_delete_room'),
    path('create/', AdminCreateRoomView.as_view(), name='admin_create_room'),
]