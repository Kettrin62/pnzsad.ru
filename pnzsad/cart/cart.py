from decimal import Decimal
from django.conf import settings
from seedlings.models import Seedling


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


def add(self, product, quantity=1, update_quantity=False):
    """
    Добавить продукт в корзину или обновить его количество.
    """
    product_id = str(Seedling.id)
    if product_id not in self.cart:
        self.cart[product_id] = {'quantity': 0,
                                 'price': str(product.price)}
    if update_quantity:
        self.cart[product_id]['quantity'] = quantity
    else:
        self.cart[product_id]['quantity'] += quantity
    self.save()

def save(self):
    # Обновление сессии cart
    self.session[settings.CART_SESSION_ID] = self.cart
    # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
    self.session.modified = True