from django.db import models


class Category(models.Model):
    title = models.CharField(
        max_length=50,
        db_index=True,
        unique=True,
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        max_length=70,
        db_index=True,
        unique=True,
        verbose_name="Часть URL категории",
    )
    image = models.ImageField(
        upload_to='./',
        verbose_name="Фото категории",
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Seedling(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='seedlings',
        verbose_name="Категория",
    )
    title = models.CharField(
        max_length=70,
        db_index=True,
        verbose_name="Название сорта",
    )
    slug = models.SlugField(
        max_length=85,
        db_index=True,
        unique=True,
        verbose_name="Часть URL сорта",
    )
    image = models.ImageField(
        upload_to='./',
        verbose_name="Фото сорта",
    )
    short_description = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Краткое описание сорта",
    )
    full_description = models.TextField(
        blank=True,
        verbose_name="Полное описание сорта",
    )
    retail_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Розничная цена",
    )
    wholesale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Оптовая цена",
    )
    stock = models.PositiveIntegerField(
        verbose_name="Кол-во саженцев",
    )
    available = models.BooleanField(
        default=True,
        verbose_name="Доступность",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата редактирования",
    )

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Саженец'
        verbose_name_plural = 'Саженцы'

    def __str__(self):
        return self.title
