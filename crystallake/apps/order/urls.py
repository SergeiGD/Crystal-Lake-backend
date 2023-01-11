from django.urls import path, include

from .views import AdminOrdersList, AdminOrderUpdate, AdminOrderCreate

urlpatterns = [
    path('', AdminOrdersList.as_view(), name='admin_orders'),
    path('create/', AdminOrderCreate.as_view(), name='admin_create_order'),
    path('create/', include('apps.order.additional_urls.clients_urls')),
    path('edit/<int:order_id>/', AdminOrderUpdate.as_view(), name='admin_edit_order'),
    path('edit/<int:order_id>/', include('apps.order.additional_urls.rooms_urls')),
    path('edit/<int:order_id>/', include('apps.order.additional_urls.services_urls')),
    path('edit/<int:order_id>/', include('apps.order.additional_urls.purchases_urls')),
    path('edit/<int:order_id>/', include('apps.order.additional_urls.timetables_urls')),
]

