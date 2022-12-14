from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserQuerySet(models.QuerySet):
    """
    Кверисет для удобного поиска по данным с форм
    """
    def search(self, **kwargs):
        qs = self
        if kwargs.get('id', ''):
            qs = qs.filter(id=kwargs['id'])
        if kwargs.get('first_name', ''):
            qs = qs.filter(first_name__icontains=kwargs['first_name'])
        if kwargs.get('last_name', ''):
            qs = qs.filter(last_name__icontains=kwargs['last_name'])
        if kwargs.get('phone', ''):
            qs = qs.filter(phone__icontains=kwargs['phone'])
        if kwargs.get('email', ''):
            qs = qs.filter(email__icontains=kwargs['email'])
        if kwargs.get('sort_by', ''):
            qs = qs.order_by(kwargs['sort_by'])

        return qs


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер для аутентификации по номеру телефона
    """
    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError(_('Необходимо указать номер телефона'))
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен быть членом персонала.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен быть отмечен как суперпользователь.'))
        return self.create_user(phone, password, **extra_fields)

    def get_queryset(self):
        return UserQuerySet(self.model, self._db)       # использем расширенный кверисет с методом search

    def search(self, **kwargs):
        return self.get_queryset().search(**kwargs)     # для вызываем метод search UserQuerySet
