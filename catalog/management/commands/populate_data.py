from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from faker import Faker
from decimal import Decimal
import random

from catalog.models import Category, Product, ProductVariant, ProductImage
from customers.models import CustomerProfile, Address
from shipping.models import ShippingZone, ShippingMethod, ShippingRate
from checkout.models import CheckoutSession
from orders.models import Order, OrderItem

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Populate database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating dummy data...')

        try:
            with transaction.atomic():
                self.create_users()
                self.create_categories()
                self.create_products()
                self.create_shipping()
                self.create_orders()

            self.stdout.write(self.style.SUCCESS('Successfully populated database with dummy data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error populating database: {str(e)}'))

    def create_users(self):
        # Create superuser
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write('Created superuser')

        # Create regular users
        for _ in range(5):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )

            # Create customer profile
            CustomerProfile.objects.create(
                user=user,
                phone=fake.phone_number()[:15]
            )

            # Create one shipping and one billing address as default
            for address_type in ['shipping', 'billing']:
                Address.objects.create(
                    user=user,
                    type=address_type,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    address1=fake.street_address(),
                    city=fake.city(),
                    state=fake.state(),
                    postal_code=fake.postcode(),
                    country='US',
                    phone=fake.phone_number()[:15],
                    is_default=True
                )

    def create_categories(self):
        categories = [
            'Electronics',
            'Fashion',
            'Home & Garden',
            'Books',
            'Sports & Outdoors',
            'Toys & Games'
        ]

        for cat_name in categories:
            Category.objects.create(
                name=cat_name,
                slug=cat_name.lower().replace(' & ', '-').replace(' ', '-'),
                description=fake.paragraph()
            )

    def create_products(self):
        categories = Category.objects.all()

        for category in categories:
            for _ in range(random.randint(5, 10)):
                product = Product.objects.create(
                    category=category,
                    name=fake.catch_phrase(),
                    slug=fake.slug(),
                    description=fake.text(),
                    base_price=Decimal(random.uniform(10, 1000)).quantize(Decimal('0.01')),
                    sku=fake.ean(length=13),
                    is_active=True
                )

                # Create variants
                for _ in range(random.randint(1, 3)):
                    ProductVariant.objects.create(
                        product=product,
                        name=fake.word(),
                        sku=fake.ean(length=13),
                        price_override=Decimal(random.uniform(10, 1000)).quantize(Decimal('0.01')),
                        stock_quantity=random.randint(0, 100)
                    )

                # Create product images
                for _ in range(random.randint(1, 4)):
                    ProductImage.objects.create(
                        product=product,
                        image=f'products/dummy-{random.randint(1, 10)}.jpg',
                        alt_text=fake.sentence()
                    )

    def create_shipping(self):
        # Create shipping zones
        zones = ['Domestic', 'International', 'Express']
        for zone_name in zones:
            # Set countries based on zone type
            if zone_name == 'Domestic':
                countries = ['US']
            elif zone_name == 'International':
                countries = ['CA', 'MX', 'GB', 'FR', 'DE']
            else:  # Express
                countries = ['US', 'CA', 'GB']

            zone = ShippingZone.objects.create(
                name=zone_name,
                description=fake.sentence(),
                countries=countries
            )

            # Create shipping methods
            for method_name in ['Standard', 'Express', 'Next Day']:
                method = ShippingMethod.objects.create(
                    name=f'{zone_name} {method_name}',
                    description=fake.sentence(),
                    calculation_type='weight',
                    estimated_days=random.randint(1, 10)
                )

                # Create shipping rate linking the method to the zone
                ShippingRate.objects.create(
                    shipping_method=method,
                    shipping_zone=zone,
                    base_rate=Decimal(random.uniform(5, 20)).quantize(Decimal('0.01')),
                    weight_rate=Decimal(random.uniform(1, 5)).quantize(Decimal('0.01')),
                    min_weight=Decimal('0.1'),
                    max_weight=Decimal('20.0')
                )

    def create_orders(self):
        users = User.objects.filter(is_superuser=False)
        products = Product.objects.all()

        for user in users:
            # Create 1-3 orders per user
            for _ in range(random.randint(1, 3)):
                shipping_address = Address.objects.filter(user=user, type='shipping', is_default=True).first()
                billing_address = Address.objects.filter(user=user, type='billing', is_default=True).first()

                # Create order with initial values
                order = Order.objects.create(
                    user=user,
                    status='pending',
                    email=user.email,
                    shipping_address=f"{shipping_address.first_name} {shipping_address.last_name}\n{shipping_address.address1}\n{shipping_address.city}, {shipping_address.state} {shipping_address.postal_code}\n{shipping_address.country}",
                    billing_address=f"{billing_address.first_name} {billing_address.last_name}\n{billing_address.address1}\n{billing_address.city}, {billing_address.state} {billing_address.postal_code}\n{billing_address.country}",
                    currency='USD',
                    subtotal=Decimal('0'),
                    shipping_cost=Decimal('10.00'),
                    tax=Decimal('0'),
                    total=Decimal('0')
                )

                # Add order items
                subtotal = Decimal('0')
                for _ in range(random.randint(1, 5)):
                    product = random.choice(products)
                    quantity = random.randint(1, 3)
                    price = product.base_price
                    item_total = price * quantity

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=price,
                        currency='USD'
                    )

                    subtotal += item_total

                # Update order totals
                tax = subtotal * Decimal('0.10')  # 10% tax
                total = subtotal + tax + order.shipping_cost
                
                order.subtotal = subtotal
                order.tax = tax
                order.total = total
                order.save()