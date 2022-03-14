from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from seedlings.models import Seedling

from .cart import Cart, calculation_of_quantity, order_send
from .forms import CartEditForm, OrderCreateForm
from .models import OrderItem


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
    MAX_VALUE_ERROR = 'превышено количество'

    cart = Cart(request)

    quantity_valid = True
    for item in cart:
        item['update_quantity_form'] = CartEditForm(
            initial={'quantity': item['quantity']}
        )
        if item['quantity'] > item['product'].stock:
            quantity_valid = False
            item['quantity_error'] = MAX_VALUE_ERROR

    first_name = ''
    last_name = ''
    email = ''
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email

    order_form = OrderCreateForm(
        request.POST or None,
        initial={
            'first_name': first_name,
            'last_name': last_name,
            'phoneNumber': '+7',
            'email': email
        }
    )

    if order_form.is_valid() and quantity_valid:
        new_order = order_form.save()
        for item in cart:
            OrderItem.objects.create(
                order=new_order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        order_send(
            'cart/order_pdf.html',
            {'order': new_order, 'seedlings': cart}
        )
        calculation_of_quantity(cart)
        cart.clear()
        return render(
                request,
                'cart/order_created.html',
                {'order': new_order}
            )

    return render(
        request,
        'cart/cart_detail.html',
        {
            'cart': cart,
            'form': order_form,
            'cart_len': len(cart)
        }
    )
