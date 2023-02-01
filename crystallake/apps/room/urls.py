from django.urls import path

from .views import RoomsCatalog, RoomDetail, get_general_busy_dates_view

urlpatterns = [
    path('', RoomsCatalog.as_view(), name='rooms'),
    path('room/<slug:room_slug>/', RoomDetail.as_view(), name='room'),
    path('room/<slug:room_slug>/get_general_busy_dates/', get_general_busy_dates_view, name='get_client_busy_dates'),
]
