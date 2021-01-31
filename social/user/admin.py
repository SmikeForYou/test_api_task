from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OldUserAdmin
from django.utils.translation import ugettext_lazy as _

from user.forms import UserChangeForm, UserCreationForm
from user.models import User


class UserAdmin(OldUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "middle_name", "date_joined")
    list_filter = ("is_superuser", "is_active", "groups")
    exclude = ("date_joined", "is_staff", "username")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_filedsets = ((None, {"classes": ("wide",), "fields": ("email", "password", "password2")}),)


admin.site.register(User, UserAdmin)
