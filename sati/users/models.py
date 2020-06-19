from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(
        _("email address"),
        unique=True,
        null=True,
        blank=True,
        help_text=_("Required."),
        error_messages={"unique": _("A user with that email already exists.")},
    )
    require_password_change = models.BooleanField(
        default=False, help_text="Force user to change password on next login"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


def user_presave_signal(sender, instance, **kwargs):
    try:
        user = User.objects.get(email=instance.email)
        if not user.password == instance.password:
            instance.require_password_change = False
    except User.DoesNotExist:
        pass


signals.pre_save.connect(user_presave_signal, sender=User, dispatch_uid="users.models")
