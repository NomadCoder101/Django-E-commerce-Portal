# Django E-commerce Portal

A production-grade e-commerce platform built with Django, offering Shopify-like features with a single customizable theme. The platform supports multi-language, multi-currency, and includes integrated payments, marketing tools, and customer dashboards.

## 🚀 Features

### Core Features

- Full product catalog management with variants
- Multi-language support (i18n)
- Multi-currency with live exchange rates
- Shopping cart with HTMX/Alpine.js
- Secure checkout with Stripe
- Customer accounts and dashboards
- Order management and tracking
- Marketing tools (promo banners, discount codes)
- SEO optimization
- Blog/CMS functionality
- Email marketing integration (Mailchimp)

### Technical Features

- Django + Django REST Framework backend
- TailwindCSS + Alpine.js frontend
- PostgreSQL database
- Redis for caching
- Celery for async tasks
- Docker Compose deployment
- NGINX reverse proxy
- HTTPS ready
- Comprehensive test suite

## 🛠️ Tech Stack

### Backend

- Django 5.0
- Django REST Framework 3.14
- PostgreSQL 13
- Redis 6
- Celery 5.3
- Stripe API
- Mailchimp API

### Frontend

- TailwindCSS
- Alpine.js
- HTMX
- Responsive design

### DevOps

- Docker
- Docker Compose
- NGINX
- Gunicorn
- WhiteNoise

## 📦 Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 13+
- Redis 6+

### Setup Steps

1. Clone the repository:

```bash
git clone <repository-url>
cd project2
```

2. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Build and start Docker containers:

```bash
docker-compose build
docker-compose up -d
```

4. Run database migrations:

```bash
docker-compose exec web python manage.py migrate
```

5. Create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

6. Install frontend dependencies and build assets:

```bash
npm install
npm run build:css
```

## 🔧 Configuration

### Environment Variables

Required environment variables in `.env`:

```env
# Django settings
DEBUG=True/False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,example.com

# Database settings
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=db
DB_PORT=5432

# Redis settings
REDIS_URL=redis://redis:6379/0

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Stripe settings
STRIPE_PUBLISHABLE_KEY=your-stripe-key
STRIPE_SECRET_KEY=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-webhook-secret

# Mailchimp settings
MAILCHIMP_API_KEY=your-mailchimp-key
MAILCHIMP_LIST_ID=your-list-id
```

### Multi-Language Support

Languages are configured in `settings/base.py`:

```python
LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fr', _('French')),
]
```

### Multi-Currency Support

Currencies are configured in `settings/base.py`:

```python
CURRENCIES = [
    ('USD', _('US Dollar')),
    ('EUR', _('Euro')),
    ('GBP', _('British Pound')),
]
```

## 📁 Project Structure

```
project2/
├── catalog/           # Product catalog app
├── checkout/          # Checkout process app
├── customers/         # Customer management app
├── marketing/         # Marketing features app
├── orders/           # Order management app
├── ecommerce/        # Main project settings
├── static/           # Static files
│   ├── css/         # Compiled CSS
│   ├── js/          # JavaScript files
│   └── src/         # Source files
├── templates/        # HTML templates
│   └── base/        # Base templates
├── media/           # User-uploaded files
├── nginx/           # NGINX configuration
└── docker/          # Docker configuration
```

## 🔒 Security Features

- CSRF protection
- XSS prevention
- SQL injection protection
- Secure cookie settings
- HTTPS enforcement
- Rate limiting
- Input sanitization
- Stripe webhook signature validation

## 🧪 Testing

Run the test suite:

```bash
docker-compose exec web python manage.py test
```

### Test Coverage

Generate coverage report:

```bash
docker-compose exec web coverage run manage.py test
docker-compose exec web coverage report
```

## 📈 Performance Optimizations

- Database query optimization
- Redis caching
- Static file compression
- Image optimization
- CDN-ready setup
- Lazy loading images
- Efficient database indexes

## 🚀 Deployment

### Production Setup

1. Update `.env` with production settings
2. Configure SSL certificates
3. Update `ALLOWED_HOSTS`
4. Set `DEBUG=False`
5. Configure CDN (optional)

### Deploy with Docker

```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

## 📝 API Documentation

API endpoints are documented using Django REST Framework's built-in documentation.
Access the API documentation at `/api/docs/` when running the development server.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📬 Support

For support, email [your-email@example.com](mailto:your-email@example.com) or open an issue on GitHub.

## 🙏 Acknowledgments

- Django and DRF teams
- TailwindCSS team
- Alpine.js developers
- All open-source contributors

---

Made with ❤️ using Django
