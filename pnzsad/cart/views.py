from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from seedlings.models import Seedling

from .cart import Cart, order_send
from .forms import CartEditForm


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Seedling, id=product_id)
    cart.add(product=product, request=request)
    return redirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Seedling, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Seedling, id=product_id)
    form = CartEditForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        cart.add(
            product=product, quantity=clean_data['quantity'], request=request
        )
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartEditForm(
            initial={'quantity': item['quantity']}
        )
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def order_gen(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartEditForm(
            initial={'quantity': item['quantity']}
        )
    order_send('cart/test.html', {'cart': cart})
    cart.clear()
    return redirect('seedlings:index')
