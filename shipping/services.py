from decimal import Decimal
from typing import List, Optional
from django.db.models import Q
from .models import ShippingZone, ShippingMethod, ShippingRate

class ShippingCalculator:
    """
    Service class for calculating shipping rates and finding available shipping methods
    """
    def __init__(self, country_code: str, weight: Optional[Decimal] = None, order_total: Optional[Decimal] = None):
        self.country_code = country_code.upper()
        self.weight = Decimal(str(weight)) if weight is not None else None
        self.order_total = Decimal(str(order_total)) if order_total is not None else None

    def get_available_rates(self) -> List[ShippingRate]:
        """
        Get all available shipping rates for the given parameters
        """
        # Find zones that include this country
        zones = ShippingZone.objects.filter(
            is_active=True,
            countries__contains=[self.country_code]
        )

        # Get rates for these zones
        rates = ShippingRate.objects.filter(
            shipping_zone__in=zones,
            shipping_method__is_active=True
        ).select_related('shipping_method', 'shipping_zone')

        # Filter by weight if provided
        if self.weight is not None:
            rates = rates.filter(
                Q(min_weight__isnull=True) | Q(min_weight__lte=self.weight),
                Q(max_weight__isnull=True) | Q(max_weight__gte=self.weight)
            )

        # Filter by order total if provided
        if self.order_total is not None:
            rates = rates.filter(
                Q(min_order_amount__isnull=True) | Q(min_order_amount__lte=self.order_total),
                Q(max_order_amount__isnull=True) | Q(max_order_amount__gte=self.order_total)
            )

        return rates

    def calculate_cost(self, shipping_method_id: int) -> Optional[Decimal]:
        """
        Calculate shipping cost for a specific shipping method
        """
        try:
            rate = ShippingRate.objects.get(
                shipping_method_id=shipping_method_id,
                shipping_method__is_active=True,
                shipping_zone__is_active=True,
                shipping_zone__countries__contains=[self.country_code]
            )
            return rate.calculate_shipping_cost(
                weight=self.weight,
                order_total=self.order_total
            )
        except ShippingRate.DoesNotExist:
            return None

    def get_estimated_delivery_days(self, shipping_method_id: int) -> Optional[int]:
        """
        Get estimated delivery days for a shipping method
        """
        try:
            method = ShippingMethod.objects.get(
                id=shipping_method_id,
                is_active=True
            )
            return method.estimated_days
        except ShippingMethod.DoesNotExist:
            return None