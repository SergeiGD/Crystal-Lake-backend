from django.urls import path

from .views import add_group_to_worker, del_group_from_worker
from ..group.views import find_groups

urlpatterns = [
    path('get_groups/', find_groups, name='get_groups_for_worker'),
    path('add_group/', add_group_to_worker, name='add_group_to_worker'),
    path('del_group/', del_group_from_worker, name='del_group_from_worker'),
]