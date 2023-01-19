from django.urls import path, include

from .views import AdminServicesList, AdminCreateService, AdminServiceDetail, AdminUpdateService, admin_delete_service, AdminTimetablesList, get_free_time_view

urlpatterns = [
    path('', AdminServicesList.as_view(), name='admin_services'),
    path('timetables/', AdminTimetablesList.as_view(), name='admin_timetables'),
    path('create/', AdminCreateService.as_view(), name='admin_create_service'),
    path('show/<int:offer_id>/', AdminServiceDetail.as_view(), name='admin_show_service'),
    path('show/<int:offer_id>/get_free_time/', get_free_time_view, name='get_free_time'),
    path('edit/<int:offer_id>/', AdminUpdateService.as_view(), name='admin_edit_service'),
    path('edit/<int:offer_id>/', include('apps.service.workers_urls')),
    path('edit/<int:offer_id>/', include('apps.offer.admin_urls')),
    path('edit/<int:offer_id>/',  include('apps.service.timetables_urls')),
    path('delete/<int:offer_id>/', admin_delete_service, name='admin_delete_service'),
]
