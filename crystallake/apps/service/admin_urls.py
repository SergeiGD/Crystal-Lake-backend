from django.urls import path, include

from .views import AdminServicesList, AdminCreateServiceView, AdminServiceDetail, AdminEditServiceView, admin_delete_service

urlpatterns = [
    path('', AdminServicesList.as_view(), name='admin_services'),
    path('create/', AdminCreateServiceView.as_view(), name='admin_create_service'),
    path('show/<int:offer_id>', AdminServiceDetail.as_view(), name='admin_show_service'),
    path('edit/<int:offer_id>', AdminEditServiceView.as_view(), name='admin_edit_service'),
    path('edit/<int:offer_id>/', include('apps.offer.admin_urls')),
    path('delete/<int:offer_id>', admin_delete_service, name='admin_delete_service'),
]
