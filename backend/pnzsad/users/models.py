from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия",
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя",
    )
    is_wholesaler = models.BooleanField(
        default=False,
        verbose_name="Оптовик",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)
