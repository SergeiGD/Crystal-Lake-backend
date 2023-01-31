from django.urls import path

from ..views import ClientRegisterView, SendRegisterCodeView

urlpatterns = [
    path('register/', ClientRegisterView.as_view(), name='client_register'),
    path('register/code/', SendRegisterCodeView.as_view(), name='client_code_register'),
]