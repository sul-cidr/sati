from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import User

import hashlib
import urllib


def gravatar_url(email, size=50):
    # urllib.parse.urlencode({"d": "/static/images/defaultavatar.jpg", "s": str(size)}),
    return "https://www.gravatar.com/avatar/{}?{}&d={}".format(
        hashlib.md5(email.lower().encode("utf8")).hexdigest(),
        urllib.parse.urlencode({"s": str(size)}),
        settings.BATON.get("GRAVATAR_DEFAULT_IMG", "retro"),
    )


class UserAdmin(UserAdmin):
    model = User
    list_display = (
        "gravatar",
        "email",
        "last_login",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_display_links = (
        "gravatar",
        "email",
    )
    list_filter = (
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password", "require_password_change")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "require_password_change",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def gravatar(self, obj):
        return mark_safe(f"<img src='{gravatar_url(obj.email)}' width='50' height='50'>")

    gravatar.allow_tags = True
    gravatar.__name__ = ""


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
