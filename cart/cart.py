from decimal import Decimal
from django.conf import settings
from shop.models import Product, Variation



class Cart:
    def __init__(self, request):
        """
        Initialze the cart
        """

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #save and empty cart in the session
            cart == self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, variation, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        variation_id = str(variation.id)
        if variation_id not in self.cart:
            self.cart[variation_id] = {
                'quantity': 0,
                'price': str(variation.price)
            }
        if override_quantity:
            self.cart[variation_id]['quantity'] = quantity
        else:
            self.cart[variation_id]['quantity'] += quantity
        
        self.save()
    
    def save(self):
        #mark the session as modified to make sure it gets saved
        self.session.modified = True
    
    def remove(self, variation):
        """
        Remove the product from the cart
        """
        variation_id = str(variation.id)
        if variation_id in self.cart:
            del self.cart[variation_id]
            self.save()
    
    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database
        """
        variation_ids = self.cart.keys()
        #get the variation objects and add them to the cart
        variations = Variation.objects.filter(id__in=variation_ids)
        cart = self.cart.copy()
        for variation in variations:
            cart[str(variation.id)]['variation'] = variation
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        count all items in the cart
        """
        return sum (item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity'] 
            for item in self.cart.values()
        )

    def clear(self):
        #remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()