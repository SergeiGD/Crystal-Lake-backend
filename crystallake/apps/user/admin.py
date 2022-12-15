from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


# Register your models here.

#from django.contrib.auth.models import Group, Permission
#g = Group()
#g.permissions.add(Permission())
#u = CustomUserAdmin()
#u.groups.add(g)
#group.user_set.all()


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('phone',)
    ordering = ('phone',)

    add_fieldsets = (
        (None, {
            'fields': (
                'phone', 'first_name', 'last_name', 'password1', 'password2', 'groups', 'is_superuser', 'is_staff'
            )
        }),
    )

    fieldsets = (
        (None, {
            "fields": (
                ('phone', 'first_name', 'last_name', 'password', 'groups', 'is_superuser', 'is_staff')
            ),
        }),
    )


#admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(CustomUser, CustomUserAdmin)
