from .cart import Cart

def cart(request):
    return {'cart_context': Cart(request)}

