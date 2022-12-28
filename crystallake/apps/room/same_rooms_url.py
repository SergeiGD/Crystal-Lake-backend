from django.urls import path

from .views import create_same_room_view, del_same_room_view

urlpatterns = [
    path('create_same_room/', create_same_room_view, name='create_same_room'),
    path('del_same_room/', del_same_room_view, name='del_same_room'),
]
