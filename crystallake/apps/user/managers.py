from django.contrib.auth.base_user import BaseUserManager
#from django.utils.translation import ugettext_lazy as _


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
