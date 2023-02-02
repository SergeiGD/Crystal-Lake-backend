from django.urls import path

from ..views import CartView, cart_prepayment_pay_view, cart_fully_pay_view, remove_from_cart_view

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('remove_item/<int:purchase_id>', remove_from_cart_view, name='remove_cart_item'),
    path('fully_pay/', cart_fully_pay_view, name='cart_fully_pay'),
    path('prepayment_pay/', cart_prepayment_pay_view, name='cart_prepayment_pay'),
]
