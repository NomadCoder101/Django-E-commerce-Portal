from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q

from .models import PromoBanner, DiscountCode, NewsletterSubscription
from .forms import NewsletterSubscriptionForm, DiscountForm
from checkout.models import Cart

def deals(request):
    active_banners = PromoBanner.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).order_by('priority')
    
    active_discounts = DiscountCode.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now()
    ).filter(
        Q(valid_until__isnull=True) | Q(valid_until__gte=timezone.now())
    )
    
    return render(request, 'marketing/deals.html', {
        'banners': active_banners,
        'discounts': active_discounts,
    })

@require_POST
def newsletter_signup(request):
    form = NewsletterSubscriptionForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        if not NewsletterSubscription.objects.filter(email=email).exists():
            subscription = form.save()
            # Send welcome email (using Celery task)
            subscription.send_welcome_email()
            
            if request.htmx:
                return render(request, 'marketing/partials/newsletter_success.html')
            messages.success(request, _('Thank you for subscribing to our newsletter!'))
        else:
            if request.htmx:
                return render(request, 'marketing/partials/newsletter_exists.html')
            messages.info(request, _('You are already subscribed to our newsletter.'))
    else:
        if request.htmx:
            return render(request, 'marketing/partials/newsletter_error.html', {'form': form})
        messages.error(request, _('Please enter a valid email address.'))
    
    return redirect('catalog:home')

@require_POST
def apply_discount(request):
    form = DiscountForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            discount = DiscountCode.objects.get(
                code=code,
                is_active=True,
                valid_from__lte=timezone.now()
            ).filter(Q(valid_until__isnull=True) | Q(valid_until__gte=timezone.now())).first()
            cart = Cart.get_or_create(request)
            if cart.can_apply_discount(discount):
                cart.apply_discount(discount)
                if request.htmx:
                    return render(request, 'marketing/partials/discount_success.html', {
                        'discount': discount,
                        'cart': cart,
                    })
                messages.success(request, _('Discount applied successfully!'))
            else:
                if request.htmx:
                    return render(request, 'marketing/partials/discount_invalid.html', {
                        'message': _('This discount cannot be applied to your cart.')
                    })
                messages.error(request, _('This discount cannot be applied to your cart.'))
        except DiscountCode.DoesNotExist:
            if request.htmx:
                return render(request, 'marketing/partials/discount_invalid.html', {
                    'message': _('Invalid discount code.')
                })
            messages.error(request, _('Invalid discount code.'))
    else:
        if request.htmx:
            return render(request, 'marketing/partials/discount_error.html', {'form': form})
        messages.error(request, _('Please enter a valid discount code.'))
    
    return redirect('checkout:cart_detail')

@require_POST
def remove_discount(request):
    cart = Cart.get_or_create(request)
    cart.remove_discount()
    
    if request.htmx:
        return render(request, 'marketing/partials/cart_summary.html', {'cart': cart})
    
    messages.success(request, _('Discount removed successfully.'))
    return redirect('checkout:cart_detail')

@login_required
def my_discounts(request):
    discounts = DiscountCode.objects.filter(
        is_active=True,
        valid_from__lte=timezone.now()
    ).filter(
        Q(valid_until__isnull=True) | Q(valid_until__gte=timezone.now())
    ).filter(customer=request.user)
    
    return render(request, 'marketing/my_discounts.html', {
        'discounts': discounts,
    })
