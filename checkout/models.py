from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from orders.models import Order


class CheckoutSession(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('abandoned', _('Abandoned')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40)
    email = models.EmailField()
    currency = models.CharField(max_length=3)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True)
    stripe_payment_intent = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.JSONField(null=True)
    billing_address = models.JSONField(null=True)
    shipping_method = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Checkout session {self.id} - {self.email}"


class PaymentAttempt(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('succeeded', _('Succeeded')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
    ]

    checkout_session = models.ForeignKey(CheckoutSession, on_delete=models.CASCADE, related_name='payment_attempts')
    stripe_payment_intent = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment attempt {self.id} for checkout {self.checkout_session.id}"
