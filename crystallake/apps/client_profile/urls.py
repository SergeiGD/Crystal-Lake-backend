from django.urls import path

from .views import ActiveOrdersCatalog, ClientInfoView, ClientChangePasswordView

urlpatterns = [
    path('active_orders/', ActiveOrdersCatalog.as_view(), name='active_orders'),
    path('info/', ClientInfoView.as_view(), name='client_info'),
    path('info/change_password/', ClientChangePasswordView.as_view(), name='client_change_password'),
]
