from django.urls import path, re_path

from .views import ActiveOrdersCatalog, ClientLoginView, client_logout_view

urlpatterns = [
    path('active_orders/', ActiveOrdersCatalog.as_view(), name='active_orders'),
    path('login/', ClientLoginView.as_view(), name='client_login'),
    path('logout/', client_logout_view, name='client_logout'),
]