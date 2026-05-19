from django.conf import settings


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, {})

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'name': product.name,
                'price': product.price,
                'image': product.image.url if product.image else '',
                'quantity': quantity
            }
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            if self.cart[product_id]['quantity'] <= 0:
                self.remove(product)
            else:
                self.save()

    def clear(self):
        self.cart = {}
        self.save()
