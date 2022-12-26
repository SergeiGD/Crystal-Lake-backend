from django.urls import path
from .views import *


urlpatterns = [
    path('', AdminTagsList.as_view(), name='admin_tags'),
    path('show/<int:tag_id>/', AdminTagDetail.as_view(), name='admin_show_tag'),
    path('edit/<int:tag_id>/', AdminTagUpdate.as_view(), name='admin_edit_tag'),
    path('create/', AdminTagCreate.as_view(), name='admin_create_tag'),
    path('delete/<int:tag_id>/', AdminDeleteTagView.as_view(), name='admin_delete_tag'),
]