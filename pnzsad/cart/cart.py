import os
import io
from xhtml2pdf import pisa
from decimal import Decimal

from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage

from seedlings.models import Seedling


# def get_order_file_path(file_name):
#     if not os.path.exists(settings.ORDER_PDF_DIR):
#         os.mkdir(settings.ORDER_PDF_DIR)
#     return os.path.join(settings.ORDER_PDF_DIR, file_name)


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
        path = os.path.join(settings.STATICFILES_DIRS[0], uri_static)
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

    # file_path = get_order_file_path('hello.pdf')
    # with open(file_path, 'ab+') as f:
    #     f.write(result.getvalue())

    subject = ''
    message = ''

    if pdf.err:
        subject = 'При формировании заказа возникла ошибка!'
        message = 'При формировании заказа возникла ошибка генерации pdf файла'

    subject = 'Сформирован новый заказ'
    message = 'Поздравляем! На сайте питомника сформирован новый заказ!'

    msg = EmailMessage(
        subject,
        message,
        'EsYA.Specsnab@gmail.com',
        ['h466h@mail.ru']
    )
    # email.attach_file(file_path)
    msg.attach('Order.pdf', result.getvalue(), 'application/pdf')
    msg.send()

    return None