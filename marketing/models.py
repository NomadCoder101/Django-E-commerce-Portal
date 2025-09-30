from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class NewsletterSubscription(models.Model):
    email = models.EmailField(_('Email address'), unique=True)
    subscribed_at = models.DateTimeField(_('Subscribed at'), auto_now_add=True)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Newsletter subscription')
        verbose_name_plural = _('Newsletter subscriptions')

    def __str__(self):
        return self.email


class DiscountCode(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', _('Percentage')),
        ('fixed', _('Fixed Amount')),
        ('shipping', _('Free Shipping')),
    ]

    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_('For percentage, use values between 0 and 100')
    )
    min_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    uses_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        now = datetime.datetime.now(datetime.UTC)
        if not self.is_active:
            return False
        if now < self.valid_from:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        if self.max_uses and self.uses_count >= self.max_uses:
            return False
        return True


class PromoBanner(models.Model):
    PLACEMENT_CHOICES = [
        ('header', _('Header')),
        ('footer', _('Footer')),
        ('sidebar', _('Sidebar')),
        ('home_hero', _('Home Hero')),
        ('collection_header', _('Collection Header')),
    ]

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='promo_banners')
    url = models.URLField()
    placement = models.CharField(max_length=20, choices=PLACEMENT_CHOICES)
    priority = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-start_date']

    def __str__(self):
        return self.title

    def is_current(self):
        now = datetime.datetime.now(datetime.UTC)
        if not self.is_active:
            return False
        if now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True
