import random
from django.core.management.base import BaseCommand                    postal_code=fake.postcode(),
                    country='US',
                    phone=fake.msisdn()[:15],
                    is_default=Falsem django.contrib.auth import get_user_model
from django.db import transaction
from faker import Faker
from decimal import Decimal

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

            CustomerProfile.objects.create(
                user=user,
                phone=fake.phone_number()[:15]
            )

            # Create one default shipping and one default billing address
            for address_type in ['shipping', 'billing']:
                # Create one default shipping and one default billing address
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
                
                # Optionally create a non-default address of each type
                if random.choice([True, False]):
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
                        is_default=False
                    )
                
                # Optionally create a non-default address of each type
                if random.choice([True, False]):
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
                        phone=fake.msisdn()[:20],
                        is_default=False
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
                    price=Decimal(random.uniform(10, 1000)).quantize(Decimal('0.01')),
                    stock=random.randint(0, 100),
                    is_active=True
                )

                # Create variants
                colors = ['Red', 'Blue', 'Green', 'Black', 'White']
                sizes = ['S', 'M', 'L', 'XL'] if category.name == 'Fashion' else None

                if sizes:
                    for color in random.sample(colors, 3):
                        for size in sizes:
                            ProductVariant.objects.create(
                                product=product,
                                name=f'{color} - {size}',
                                sku=fake.ean(length=13),
                                price=product.price + Decimal(random.uniform(0, 50)).quantize(Decimal('0.01')),
                                stock=random.randint(0, 50)
                            )
                else:
                    for color in random.sample(colors, 3):
                        ProductVariant.objects.create(
                            product=product,
                            name=color,
                            sku=fake.ean(length=13),
                            price=product.price + Decimal(random.uniform(0, 50)).quantize(Decimal('0.01')),
                            stock=random.randint(0, 50)
                        )

    def create_shipping(self):
        # Create shipping zones
        zones = [
            ('Domestic', ['US']),
            ('Canada', ['CA']),
            ('Europe', ['GB', 'DE', 'FR', 'IT', 'ES']),
            ('Asia', ['JP', 'CN', 'KR', 'IN'])
        ]

        for name, countries in zones:
            zone = ShippingZone.objects.create(
                name=name,
                countries=countries,
                description=f'Shipping zone for {name}'
            )

            # Create shipping methods
            methods = [
                ('Standard', 'flat', 5, 7),
                ('Express', 'flat', 2, 3),
                ('Next Day', 'flat', 1, 1)
            ]

            for method_name, calc_type, min_days, max_days in methods:
                method = ShippingMethod.objects.create(
                    name=method_name,
                    description=f'{method_name} shipping ({min_days}-{max_days} business days)',
                    calculation_type=calc_type,
                    estimated_days=max_days
                )

                # Create shipping rates
                ShippingRate.objects.create(
                    shipping_method=method,
                    shipping_zone=zone,
                    base_rate=Decimal(random.uniform(5, 50)).quantize(Decimal('0.01')),
                    weight_rate=Decimal(random.uniform(0.5, 2)).quantize(Decimal('0.01'))
                )

    def create_orders(self):
        users = User.objects.filter(is_staff=False)
        products = Product.objects.filter(is_active=True)

        for user in users:
            for _ in range(random.randint(1, 3)):
                # Create order
                order = Order.objects.create(
                    user=user,
                    email=user.email,
                    status=random.choice(['pending', 'processing', 'shipped', 'delivered']),
                    shipping_address=fake.address(),
                    billing_address=fake.address(),
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
                    price = product.price

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=price,
                        currency='USD'
                    )

                    subtotal += price * quantity

                # Update order totals
                tax = subtotal * Decimal('0.10')  # 10% tax
                order.subtotal = subtotal
                order.tax = tax
                order.total = subtotal + tax + order.shipping_cost
                order.save()