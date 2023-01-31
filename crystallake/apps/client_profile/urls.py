from django.urls import path

from .views import ActiveOrdersCatalog

urlpatterns = [
    path('active_orders/', ActiveOrdersCatalog.as_view(), name='active_orders')
]
