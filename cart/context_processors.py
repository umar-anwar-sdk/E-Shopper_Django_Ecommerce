def cart_total_amount(request):
    cart = request.session.get('cart', {})
    return {'cart_total_amount': len(cart)}