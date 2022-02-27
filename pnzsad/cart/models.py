from django.db import models

from seedlings.models import Seedling


class Order(models.Model):
    first_name = models.CharField(
        max_length=50, verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=50, verbose_name='Фамилия',
    )
    email = models.EmailField()
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Индекс',
    )
    address = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name='Адрес',
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Населенный пункт',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлён',
    )
    comment = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Комментарий',
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ',
    )
    product = models.ForeignKey(
        Seedling,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        verbose_name='Саженец',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Саженец'
        verbose_name_plural = 'Саженцы'

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
