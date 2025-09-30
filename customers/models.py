from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    default_currency = models.CharField(max_length=3, default='USD')
    default_language = models.CharField(max_length=10, default='en')
    marketing_consent = models.BooleanField(default=False)
    mailchimp_subscriber_hash = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.email}"


class Address(models.Model):
    ADDRESS_TYPES = [
        ('shipping', _('Shipping')),
        ('billing', _('Billing')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    is_default = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Addresses'
        unique_together = ('user', 'type', 'is_default')

    def __str__(self):
        return f"{self.type.title()} address for {self.user.email}"

    def save(self, *args, **kwargs):
        if self.is_default:
            # Set all other addresses of this type for this user to non-default
            Address.objects.filter(
                user=self.user,
                type=self.type,
                is_default=True
            ).update(is_default=False)
        super().save(*args, **kwargs)
