from django.urls import path

from .views import ActiveOrdersCatalog, ClientInfoView, ClientChangePasswordView, ManageOrder, ManagePurchase, RoomPurchaseView, ServicePurchaseView, cancel_purchase_view, pay_view

urlpatterns = [
    path(
        'active_orders/',
        ActiveOrdersCatalog.as_view(),
        name='active_orders'
    ),
    path(
        'active_orders/manage_order/<int:order_id>',
        ManageOrder.as_view(),
        name='client_manage_order'
    ),
    path(
        'active_orders/manage_order/<int:order_id>/pay',
        pay_view,
        name='client_pay'
    ),
    path(
        'active_orders/manage_order/<int:order_id>/manage_purchase/<int:purchase_id>',
        ManagePurchase.as_view(),
        name='client_manage_purchase'
    ),
    path(
        'active_orders/manage_order/<int:order_id>/manage_purchase/<int:purchase_id>/cancel',
        cancel_purchase_view,
        name='client_cancel_purchase'
    ),
    path(
        'active_orders/manage_order/<int:order_id>/manage_purchase/<int:purchase_id>/save_room_changes',
        RoomPurchaseView.as_view(),
        name='client_save_room_changes'
    ),
    path(
        'active_orders/manage_order/<int:order_id>/manage_purchase/<int:purchase_id>/save_service_changes',
        ServicePurchaseView.as_view(),
        name='client_save_service_changes'
    ),
    path(
        'info/', ClientInfoView.as_view(),
        name='client_info'
    ),
    path(
        'info/change_password/',
        ClientChangePasswordView.as_view(),
        name='client_change_password'
    ),
]
