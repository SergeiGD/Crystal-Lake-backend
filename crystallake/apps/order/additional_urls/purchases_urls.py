from django.urls import path

from ..views import RoomPurchaseCreateView, RoomPurchaseEditView, get_purchase_info_view, cancel_purchase_view, ServicePurchaseEditView, ServicePurchaseCreateView

urlpatterns = [
    path('edit_room_purchase/', RoomPurchaseEditView.as_view(), name='edit_room_purchase'),
    path('create_room_purchase/', RoomPurchaseCreateView.as_view(), name='create_room_purchase'),
    path('edit_service_purchase/', ServicePurchaseEditView.as_view(), name='edit_service_purchase'),
    path('create_service_purchase/', ServicePurchaseCreateView.as_view(), name='create_service_purchase'),
    path('get_purchase/<int:purchase_id>/', get_purchase_info_view, name='get_purchase'),
    path('cancel_purchase/', cancel_purchase_view, name='cancel_purchase'),
]
