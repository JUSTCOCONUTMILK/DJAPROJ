from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    is_banned = models.BooleanField(default=False, verbose_name="Заблокирован")

    def clean(self):
        super().clean()
        if self.is_superuser:
            qs = type(self).objects.filter(is_superuser=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("В системе может быть только один супер админ.")

    def role_label(self) -> str:
        if self.is_superuser:
            return "Супер админ"
        if self.is_staff:
            return "Админ"
        return "Юзер"
