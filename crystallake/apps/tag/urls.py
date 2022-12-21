from django.urls import path
from .views import *


urlpatterns = [
    path('', AdminTagsList.as_view(), name='admin_tags'),
    path('show/<int:tag_id>/', AdminTagsDetail.as_view(), name='admin_show_tag'),
    path('edit/<int:tag_id>/', AdminTagsUpdate.as_view(), name='admin_edit_tag'),
    path('create/', AdminTagsCreate.as_view(), name='admin_create_tag'),
]