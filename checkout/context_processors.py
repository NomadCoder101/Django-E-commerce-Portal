from .models import Cart

def cart_processor(request):
    """
    Context processor that adds the current cart to the template context.
    """
    cart = None
    if hasattr(request, 'session'):
        # Ensure session is created
        if not request.session.session_key:
            request.session.create()
            
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = None
    
    if not cart:
        cart = Cart.objects.create(
            session_key=request.session.session_key or '',
            currency='USD'  # Set default currency
        )
        if hasattr(request, 'session'):
            request.session['cart_id'] = cart.id
            request.session.modified = True
    
    return {
        'cart': cart
    }