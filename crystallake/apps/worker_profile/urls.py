from django.urls import path

from .views import AdminLoginView, admin_logout_view

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin_login'),
    path('logout/', admin_logout_view, name='admin_logout'),
]