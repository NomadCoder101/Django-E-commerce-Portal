from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Order, OrderItem

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    # Search by order ID
    search = request.GET.get('search')
    if search:
        orders = orders.filter(
            Q(id__icontains=search) |
            Q(stripe_payment_intent__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'orders/order_list.html', {
        'page_obj': page_obj,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status,
        'search': search,
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {
        'order': order,
    })

@login_required
def order_track(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    tracking_info = order.get_tracking_info()
    
    if request.headers.get('HX-Request'):
        return render(request, 'orders/partials/tracking_info.html', {
            'order': order,
            'tracking_info': tracking_info,
        })
    
    return render(request, 'orders/order_track.html', {
        'order': order,
        'tracking_info': tracking_info,
    })

@login_required
def order_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_invoice.html', {
        'order': order,
    })

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        if order.can_cancel():
            order.cancel()
            return JsonResponse({
                'status': 'success',
                'message': _('Order cancelled successfully.')
            })
        return JsonResponse({
            'status': 'error',
            'message': _('This order cannot be cancelled.')
        }, status=400)
    
    return render(request, 'orders/cancel_order.html', {
        'order': order,
    })
