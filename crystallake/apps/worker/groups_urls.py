from django.urls import path

from .views import get_unattached_groups, add_group_to_worker, del_group_from_worker

urlpatterns = [
    path('get_unattached_groups/', get_unattached_groups, name='get_unattached_groups'),
    path('add_group/', add_group_to_worker, name='add_group_to_worker'),
    path('del_group/', del_group_from_worker, name='del_group_from_worker'),
]