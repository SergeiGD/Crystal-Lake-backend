from django.urls import path

from ..views import ClientLoginView, client_logout_view

urlpatterns = [
    path('login/', ClientLoginView.as_view(), name='client_login'),
    path('logout/', client_logout_view, name='client_logout'),
]
