from django.urls import path

from .views import AdminWorkersList, AdminCreatWorker

urlpatterns = [
    path('', AdminWorkersList.as_view(), name='admin_workers'),
    path('create/', AdminCreatWorker.as_view(), name='admin_create_worker')
]