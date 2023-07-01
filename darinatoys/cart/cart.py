from decimal import Decimal
from django.conf import settings
from store.models import Toy


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        

    def add(self, toy, quantity=1, update_quantity=False):
        toy_id = str(toy.id)
        if toy_id not in self.cart:
            self.cart[toy_id] = {'quantity': 0,
                                    'price': str(toy.cost)}
        if update_quantity:
            self.cart[toy_id]['quantity'] = quantity
        else:
            self.cart[toy_id]['quantity'] += quantity
        self.save()


    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, toy):
        toy_id = str(toy.id)
        if toy_id in self.cart:
            del self.cart[toy_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        toy_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        toys = Toy.objects.filter(id__in=toy_ids)
        for toy in toys:
            self.cart[str(toy.id)]['toy'] = toy

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                self.cart.values())
    
    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True