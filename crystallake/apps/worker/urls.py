from django.urls import path, include

from .views import AdminWorkersList, AdminCreatWorker, AdminWorkerDetail, AdminWorkerUpdate, admin_delete_worker

urlpatterns = [
    path('', AdminWorkersList.as_view(), name='admin_workers'),
    path('create/', AdminCreatWorker.as_view(), name='admin_create_worker'),
    path('show/<int:worker_id>/', AdminWorkerDetail.as_view(), name='admin_show_worker'),
    path('delete/<int:worker_id>/', admin_delete_worker, name='admin_delete_worker'),
    path('edit/<int:worker_id>/', AdminWorkerUpdate.as_view(), name='admin_edit_worker'),
    path('edit/<int:worker_id>/', include('apps.worker.qualifications_urls'))
]