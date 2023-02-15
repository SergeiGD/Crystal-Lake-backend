from django.urls import path

from .views import create_timetable_view, edit_timetable_view, delete_timetable_view, get_timetable_info_view, find_timetables

urlpatterns = [
    path('get_timetables/', find_timetables, name='admin_service_timetables'),
    path('create_timetable/', create_timetable_view, name='create_timetable'),
    path('edit_timetable/', edit_timetable_view, name='edit_timetable'),
    path('delete_timetable/', delete_timetable_view, name='delete_timetable'),
    path('get_timetable/<int:timetable_id>/', get_timetable_info_view, name='get_timetable'),
]
