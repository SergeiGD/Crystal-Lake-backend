from django.urls import path

from .views import manage_timetable_view, get_timetable_info_view

urlpatterns = [
    path('create_timetable/', manage_timetable_view, name='create_timetable'),
    path('get_timetable/<int:timetable_id>', get_timetable_info_view, name='get_timetable'),
]
