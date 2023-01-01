from django.urls import path
from django.urls import include

from .views import AdminGroupsList, AdminGroupDetail, AdminGroupUpdate, AdminGroupDelete, AdminGroupCreate

urlpatterns = [
    path('', AdminGroupsList.as_view(), name='admin_groups'),
    path('show/<int:group_id>/', AdminGroupDetail.as_view(), name='admin_show_group'),
    path('create/', AdminGroupCreate.as_view(), name='admin_create_group'),
    path('edit/<int:group_id>/', AdminGroupUpdate.as_view(), name='admin_edit_group'),
    path('edit/<int:group_id>/', include('apps.group.permissions_urls')),
    path('delete/<int:group_id>/', AdminGroupDelete.as_view(), name='admin_delete_group'),
]