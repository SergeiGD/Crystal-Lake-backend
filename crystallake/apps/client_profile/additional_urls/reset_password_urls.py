from django.urls import path

from ..views import ClientResetPasswordView, ClientResetPasswordCodeView

urlpatterns = [
    path('reset_password/', ClientResetPasswordView.as_view(), name='client_reset_password'),
    path('reset_password/code/', ClientResetPasswordCodeView.as_view(), name='client_code_reset_password'),
]