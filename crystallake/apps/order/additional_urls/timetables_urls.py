from django.urls import path

from ...service.views import find_timetables

urlpatterns = [
    path('get_timetables/', find_timetables, name='get_timetables_for_service'),
]
