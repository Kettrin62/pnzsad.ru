from django.db import models


class About(models.Model):
    markup = models.TextField(
        verbose_name='Разметка страницы',
    )

    class Meta:
        verbose_name = 'Разметка страницы'
        verbose_name_plural = 'Разметка страницы'
