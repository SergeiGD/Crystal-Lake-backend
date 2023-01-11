from django.urls import path

from ...room.views import find_rooms

urlpatterns = [
    path('get_rooms/', find_rooms, name='get_rooms_for_order'),
]
