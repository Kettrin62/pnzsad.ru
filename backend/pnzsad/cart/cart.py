import io
import os
from decimal import Decimal

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from xhtml2pdf import pisa

from seedlings.models import Seedling


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def get_product_price(self, product, request):
        if request.user.is_anonymous or not request.user.is_wholesaler:
            return product.retail_price
        return product.wholesale_price

    def add(self, product, request, quantity=1):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 1,
                'price': str(
                    self.get_product_price(product, request)
                )
            }
        else:
            self.cart[product_id]['quantity'] = quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Seedling.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет товаров в корзине.
        """
        # return sum(item['quantity'] for item in self.cart.values())
        return len(self.cart)

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(
            Decimal(
                item['price']
            ) * item['quantity'] for item in self.cart.values()
        )

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


def fetch_pdf_resources(uri, rel):
    if uri.find(settings.MEDIA_URL) != -1:
        uri_media = uri.replace(settings.MEDIA_URL, '')
        uri_media = uri_media.replace('/', os.sep)
        path = os.path.join(settings.MEDIA_ROOT, uri_media)
    elif uri.find(settings.STATIC_URL) != -1:
        uri_static = uri.replace(settings.STATIC_URL, '')
        uri_static = uri_static.replace('/', os.sep)
        path = os.path.join(settings.STATIC_ROOT, uri_static)
    else:
        path = None
    return path


def order_send(template, context):
    template_obj = get_template(template)
    context_obj = context
    html = template_obj.render(context_obj)
    result = io.BytesIO()

    pdf = pisa.pisaDocument(
        io.BytesIO(html.encode('UTF-8')),
        result,
        encoding='utf-8',
        link_callback=fetch_pdf_resources
    )

    subject = ''
    message = ''

    if pdf.err:
        subject = 'При формировании заказа возникла ошибка!'
        message = 'При формировании заказа возникла ошибка генерации pdf файла'

    subject = 'Сформирован новый заказ'
    message = (
        'На сайте pnzsad.ru оформлен новый заказ. '
        'Бланк заказа прикреплён к этому письму.'
    )

    msg = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        settings.EMAIL_TO
    )
    msg.attach('Order.pdf', result.getvalue(), 'application/pdf')
    msg.send()

    return None


def calculation_of_quantity(cart):
    for item in cart:
        item['product'].stock = item['product'].stock - item['quantity']
        item['product'].save()
