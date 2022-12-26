from django.urls import path

from .views import RoomsCatalog, RoomDetail

urlpatterns = [
    path('', RoomsCatalog.as_view(), name='rooms'),
    path('room/<slug:room_slug>/', RoomDetail.as_view(), name='room'),

]
