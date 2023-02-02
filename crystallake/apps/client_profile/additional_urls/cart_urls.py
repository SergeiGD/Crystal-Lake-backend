from django.urls import path

from ..views import CartView
from ...order.views import remove_from_cart_view

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('remove_item/<int:purchase_id>', remove_from_cart_view, name='remove_cart_item'),
]
