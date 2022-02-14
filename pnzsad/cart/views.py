from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from seedlings.models import Seedling
from .cart import Cart
from .forms import CartEditForm


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Seedling, id=product_id)
    cart.add(product=product)
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
        cart.add(product=product, quantity=clean_data['quantity'])
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['quantity'] = CartEditForm(
            initial={'update_quantity_form': item['quantity']}
        )
    return render(request, 'cart/cart_detail.html', {'cart': cart})
