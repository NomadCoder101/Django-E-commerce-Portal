from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
import stripe

from .models import Cart, CartItem, CheckoutSession, OrderItem
from catalog.models import Product, ProductVariant

stripe.api_key = settings.STRIPE_SECRET_KEY

def cart_detail(request):
    cart = Cart.get_or_create(request)
    return render(request, 'checkout/cart.html', {'cart': cart})

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))
    
    cart = Cart.get_or_create(request)
    
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id)
        cart.add_item(product, quantity, variant)
    else:
        cart.add_item(product, quantity)
    
    if request.htmx:
        return JsonResponse({
            'cart_count': cart.total_items,
            'cart_total': cart.get_total_display()
        })
    return redirect('checkout:cart_detail')

@require_POST
def remove_from_cart(request, item_id):
    cart = Cart.get_or_create(request)
    cart.remove_item(item_id)
    
    if request.htmx:
        return JsonResponse({
            'cart_count': cart.total_items,
            'cart_total': cart.get_total_display()
        })
    return redirect('checkout:cart_detail')

@require_POST
def update_cart(request, item_id):
    cart = Cart.get_or_create(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update_quantity(item_id, quantity)
    
    if request.htmx:
        return JsonResponse({
            'cart_count': cart.total_items,
            'cart_total': cart.get_total_display(),
            'item_total': cart.get_item_total_display(item_id)
        })
    return redirect('checkout:cart_detail')

@login_required
def checkout(request):
    cart = Cart.get_or_create(request)
    
    if not cart.items.exists():
        return redirect('checkout:cart_detail')
    
    if request.method == 'POST':
        try:
            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(item.get_total() * 100),
                        'product_data': {
                            'name': item.product.name,
                            'images': [item.product.images.first().image.url] if item.product.images.exists() else [],
                        },
                    },
                    'quantity': item.quantity,
                } for item in cart.items.all()],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('checkout:success')),
                cancel_url=request.build_absolute_uri(reverse('checkout:cart_detail')),
                customer_email=request.user.email,
            )
            
            # Create order
            order = CheckoutSession.objects.create(
                user=request.user,
                email=request.user.email,
                total=cart.get_total(),
                stripe_session_id=checkout_session.id
            )
            
            # Create order items
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.get_price(),
                    total=item.get_total()
                )
            
            # Clear the cart
            cart.clear()
            
            return JsonResponse({'sessionId': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'checkout/checkout.html', {
        'cart': cart,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY
    })

@login_required
def checkout_success(request):
    return render(request, 'checkout/success.html')
