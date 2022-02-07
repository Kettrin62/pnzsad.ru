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
        upload_to='./Category/',
        verbose_name="Фото категории",
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        constraints = (
            models.UniqueConstraint(
                fields=['title', ],
                name='unique category value'
            ),
        )

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
        upload_to='./Seedlings/',
        verbose_name="Фото сорта",
    )
    short_description = models.CharField(
        max_length=60,
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
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'category'],
                name='unique seedling value'
            ),
        )

    def __str__(self):
        return self.title


class Swiper(models.Model):
    title = models.CharField(
        max_length=70,
        verbose_name="Название слайда",
    )
    text = models.CharField(
        max_length=450,
        verbose_name="Текст слайда",
    )
    image = models.ImageField(
        upload_to='./Swiper/',
        verbose_name="Фото сорта",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания слайда",
    )
    available = models.BooleanField(
        default=True,
        verbose_name="Активный слайд",
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

    def __str__(self):
        return self.title


class Comment(models.Model):
    seedling = models.ForeignKey(
        Seedling,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Сорт",
    )
    text = models.TextField(
        verbose_name="Текст комментария",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания комментария",
    )
    author_name = models.CharField(
        max_length=50,
        verbose_name="Имя автора",
    )

    class Meta:
        ordering = ("created",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        index_together = ('seedling',)
        constraints = (
            models.UniqueConstraint(
                fields=['seedling', 'text'],
                name='unique comment value'
            ),
        )

    def __str__(self):
        return f"Комментарий от {self.author_name}: {self.text[:30]}"
