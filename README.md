# Django E-commerce Portal

A production-grade e-commerce platform built with Django, offering Shopify-like features with a single customizable theme. The platform supports multi-language, multi-currency, and includes integrated payments, m## 💻 Development Setup

### Project Structure

```
project2/
├── catalog/           # Product catalog management
├── checkout/          # Checkout process and cart
├── customers/         # Customer profiles and authentication
├── docs/             # Project documentation
├── ecommerce/        # Main project settings
├── marketing/        # Marketing features
├── orders/           # Order processing and management
├── shipping/         # Shipping calculations and zones
├── static/           # Static files
├── templates/        # HTML templates
└── requirements.txt  # Python dependencies
```

### Key Apps and Their Purpose

1. **catalog/**

   - Product management
   - Categories and variants
   - Product images and attributes

2. **customers/**

   - User profiles
   - Address management
   - Authentication views

3. **orders/**

   - Order processing
   - Order history
   - Invoice generation

4. **shipping/**
   - Shipping zones
   - Rate calculations
   - Carrier integration

## ⚙️ Configuration

### Essential Settings

1. **Database Configuration** (ecommerce/settings/development.py)

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

2. **Cache Configuration** (ecommerce/settings/development.py)

   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
           'LOCATION': 'unique-snowflake',
       }
   }
   ```

3. **Email Configuration** (.env)
   ```
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```

## 🗃️ Database Population

The project includes a management command to populate the database with sample data:

```bash
python manage.py populate_data
```

This command creates:

- Sample products with variants
- Test users with addresses
- Categories and product images
- Sample orders
- Shipping zones and rates

## 📡 API Documentation

### Available Endpoints

1. **Products API**

   - GET /api/products/ - List all products
   - GET /api/products/{id}/ - Get product details
   - POST /api/products/ - Create new product (admin only)

2. **Orders API**

   - GET /api/orders/ - List user orders
   - POST /api/orders/ - Create new order
   - GET /api/orders/{id}/ - Get order details

3. **Customer API**
   - GET /api/customer/profile/ - Get user profile
   - PUT /api/customer/profile/ - Update profile
   - GET /api/customer/addresses/ - List addresses

## 🚀 Deployment

### Production Setup

1. **Update Production Settings**

   - Set DEBUG=False
   - Configure allowed hosts
   - Set up proper email backend
   - Configure static file serving

2. **Environment Variables**

   ```bash
   SECRET_KEY=your_secret_key
   ALLOWED_HOSTS=your_domain.com
   DATABASE_URL=postgres://user:password@host:5432/dbname
   REDIS_URL=redis://localhost:6379/1
   ```

3. **Static Files**

   ```bash
   python manage.py collectstatic
   ```

4. **Database Migration**
   ```bash
   python manage.py migrate
   ```

## ❗ Troubleshooting

### Common Issues

1. **Database Connection Issues**

   - Check PostgreSQL service is running
   - Verify database credentials
   - Ensure database exists

2. **Static Files Not Loading**

   - Run collectstatic
   - Check STATIC_ROOT setting
   - Verify web server configuration

3. **Email Sending Fails**
   - Verify SMTP credentials
   - Check email backend configuration
   - Test email settings

### Debug Mode

For development, ensure DEBUG=True in settings:

```python
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.eting tools, and customer dashboards.

## � Table of Contents

1. [Features](#-features)
2. [Tech Stack](#-tech-stack)
3. [Installation](#-installation)
4. [Development Setup](#-development-setup)
5. [Project Structure](#-project-structure)
6. [Configuration](#-configuration)
7. [Database Population](#-database-population)
8. [API Documentation](#-api-documentation)
9. [Deployment](#-deployment)
10. [Troubleshooting](#-troubleshooting)

## �🚀 Features

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

Before starting, ensure you have the following installed:

1. Python 3.11 or higher
2. PostgreSQL 13 or higher
3. Redis 6 or higher (optional for development)
4. Node.js 18 or higher
5. Git

### Local Development Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/NomadCoder101/Django-E-commerce-Portal.git
   cd Django-E-commerce-Portal
   ```

2. **Create and Activate Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**

   ```bash
   cp .env.example .env
   # Edit .env file with your settings:
   # - Database credentials
   # - Secret key
   # - Email settings
   # - API keys (Stripe, Mailchimp)
   ```

5. **Database Setup**

   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Populate Database with Sample Data**

   ```bash
   python manage.py populate_data
   ```

8. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

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

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

## 📬 Support

For support, email [cbinary07@gmail.com](mailto:cbinary07@gmail.com) or open an issue on GitHub.

## 🙏 Acknowledgments

- Django and DRF teams
- TailwindCSS team
- Alpine.js developers
- All open-source contributors

---

Made with ❤️ using Django
