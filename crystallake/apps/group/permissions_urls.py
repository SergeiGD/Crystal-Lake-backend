from django.urls import path

from .views import del_permission_from_group, add_permission_to_group, get_unattached_permissions

urlpatterns = [
    path('del_permission/', del_permission_from_group, name='del_permission_from_group'),
    path('add_permission/', add_permission_to_group, name='add_permission_to_group'),
    path('get_unattached_permissions/', get_unattached_permissions, name='get_unattached_permissions')
]