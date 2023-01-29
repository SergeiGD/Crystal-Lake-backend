from django.urls import path, re_path

from .views import CartView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
]