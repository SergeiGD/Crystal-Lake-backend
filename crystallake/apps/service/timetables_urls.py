from django.urls import path

from .views import create_timetable_view, edit_timetable_view, get_timetable_info_view

urlpatterns = [
    #path('create_timetable/', manage_timetable_view, name='create_timetable'),
    path('create_timetable/', create_timetable_view, name='create_timetable'),
    path('edit_timetable/<int:timetable_id>/', edit_timetable_view, name='edit_timetable'),
    path('get_timetable/<int:timetable_id>/', get_timetable_info_view, name='get_timetable'),
]
