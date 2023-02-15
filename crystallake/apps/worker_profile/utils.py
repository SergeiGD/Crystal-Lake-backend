from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class AdminLoginRequired(LoginRequiredMixin):
    login_url = reverse_lazy('admin_login')

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        return staff_member_required(view, login_url=reverse_lazy('admin_login'))

