from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.db import models


class About(models.Model):
    markup = RichTextUploadingField(
        verbose_name='Разметка страницы',
    )

    class Meta:
        verbose_name = 'Разметка страницы'
        verbose_name_plural = 'Разметка страницы'

    def save(self, *args, **kwargs):
        if About.objects.count() < 1 or About.objects.all().first() == self:
            super().save(*args, **kwargs)
        else:
            raise ValidationError(
                'Доступна всего одна запись для разметки страницы!'
            )

    def __str__(self):
        return self.markup[:30]
