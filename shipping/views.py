from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .models import ShippingAddress
from .forms import ShippingAddressForm, ShippingMethodForm
from checkout.models import CheckoutSession

@login_required
def shipping_address_list(request):
    addresses = ShippingAddress.objects.filter(user=request.user)
    return render(request, 'shipping/address_list.html', {
        'addresses': addresses
    })

@login_required
def shipping_address_add(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, _('Shipping address added successfully.'))
            return redirect('shipping:address_list')
    else:
        form = ShippingAddressForm()

    return render(request, 'shipping/address_form.html', {
        'form': form,
        'title': _('Add New Shipping Address')
    })

@login_required
def shipping_address_edit(request, pk):
    address = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, _('Shipping address updated successfully.'))
            return redirect('shipping:address_list')
    else:
        form = ShippingAddressForm(instance=address)

    return render(request, 'shipping/address_form.html', {
        'form': form,
        'title': _('Edit Shipping Address'),
        'address': address
    })

@login_required
def shipping_address_delete(request, pk):
    address = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
    
    if request.method == 'POST':
        address.delete()
        messages.success(request, _('Shipping address deleted successfully.'))
        return redirect('shipping:address_list')

    return render(request, 'shipping/address_confirm_delete.html', {
        'address': address
    })

@login_required
def set_default_address(request, pk):
    address = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
    address.is_default = True
    address.save()
    messages.success(request, _('Default shipping address updated.'))
    return redirect('shipping:address_list')

def select_shipping_method(request):
    checkout_session = CheckoutSession.objects.filter(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key,
        status='pending'
    ).first()

    if not checkout_session or not checkout_session.shipping_address:
        messages.error(request, _('Please select a shipping address first.'))
        return redirect('checkout:shipping_address')

    available_methods = checkout_session.get_available_shipping_methods()

    if request.method == 'POST':
        form = ShippingMethodForm(request.POST, available_methods=available_methods)
        if form.is_valid():
            checkout_session.shipping_method = form.cleaned_data['shipping_method']
            checkout_session.calculate_shipping_cost()
            checkout_session.save()
            return redirect('checkout:payment')
    else:
        form = ShippingMethodForm(
            available_methods=available_methods,
            initial={'shipping_method': checkout_session.shipping_method}
        )

    return render(request, 'shipping/select_method.html', {
        'form': form,
        'checkout_session': checkout_session
    })
