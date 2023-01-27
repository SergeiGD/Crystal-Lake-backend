from django.urls import path, re_path

from .views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
]
