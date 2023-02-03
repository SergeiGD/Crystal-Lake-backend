from django.urls import path

from .views import Index, Contacts

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('contacts', Contacts.as_view(), name='contacts')
]
