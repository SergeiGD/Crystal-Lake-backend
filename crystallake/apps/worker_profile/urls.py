from django.urls import path

from .views import AdminLoginView, admin_logout_view, AdminSmsCodeView, AdminResetPasswordView, AdminProfileView

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin_login'),
    path('logout/', admin_logout_view, name='admin_logout'),
    path('reset_password/', AdminResetPasswordView.as_view(), name='admin_reset_password'),
    path('reset_password/send_code/', AdminSmsCodeView.as_view(), name='admin_send_code'),
    path('profile/', AdminProfileView.as_view(), name='admin_profile'),
]