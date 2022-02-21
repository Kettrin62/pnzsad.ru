import datetime as dt

from cart.cart import Cart
from seedlings.models import Category


def get_year(request):
    year = dt.date.today().year
    return {'year': year}


def get_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}


def get_len_cart(request):
    cart = Cart(request)
    if not len(cart):
        return {'len_cart': ''}
    return {'len_cart': len(cart)}
