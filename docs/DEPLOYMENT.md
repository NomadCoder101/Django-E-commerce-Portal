# Production Deployment Guide

This guide covers deploying the Django E-commerce Portal to a production environment.

## Prerequisites

- A Linux server (Ubuntu 20.04 LTS or newer recommended)
- Domain name configured with DNS
- SSL certificate (Let's Encrypt recommended)
- Docker and Docker Compose installed
- Access to email service (SMTP)
- Stripe account
- Mailchimp account
- (Optional) AWS S3 or similar for media storage

## Server Setup

### 1. Initial Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    git

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. SSL Certificate Setup

Using Let's Encrypt with Certbot:

```bash
# Install Certbot
sudo apt install -y certbot

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Certificate location
/etc/letsencrypt/live/yourdomain.com/
```

### 3. Environment Configuration

Create production environment file:

```bash
# Create .env file
cp .env.example .env.prod

# Edit production environment variables
nano .env.prod
```

Required production settings:

```env
# Basic Settings
DEBUG=False
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=ecommerce_prod
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# AWS S3 (optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=your-region

# Security
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 4. Production Docker Setup

Create `docker-compose.prod.yml`:

```yaml
version: "3.8"

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.prod
    command: gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    expose:
      - 8000
    env_file:
      - .env.prod
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    volumes:
      - postgres_data_prod:/var/lib/postgresql/data/
    env_file:
      - .env.prod

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data_prod:/data

  celery:
    build:
      context: .
      dockerfile: Dockerfile.prod
    command: celery -A ecommerce worker -l INFO
    volumes:
      - .:/app
    env_file:
      - .env.prod
    depends_on:
      - redis
      - db

  nginx:
    image: nginx:1.21-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./nginx/prod:/etc/nginx/conf.d
      - /etc/letsencrypt:/etc/letsencrypt
    depends_on:
      - web

volumes:
  postgres_data_prod:
  redis_data_prod:
  static_volume:
  media_volume:
```

### 5. NGINX Production Configuration

Create `nginx/prod/default.conf`:

```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
    ssl_stapling on;
    ssl_stapling_verify on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Content-Security-Policy "default-src 'self' https: data: 'unsafe-inline' 'unsafe-eval';";

    location / {
        proxy_pass http://django;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
        client_max_body_size 100M;
    }

    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
        access_log off;
        add_header Cache-Control "public, no-transform";
    }

    location /media/ {
        alias /app/media/;
        expires 30d;
        access_log off;
        add_header Cache-Control "public, no-transform";
    }
}
```

### 6. Deployment Steps

1. Clone repository and navigate to project directory:

```bash
git clone <repository-url>
cd project2
```

2. Set up environment variables:

```bash
cp .env.example .env.prod
# Edit .env.prod with production settings
```

3. Build and start services:

```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

4. Run migrations:

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

5. Create superuser:

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

6. Collect static files:

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input
```

### 7. Monitoring and Maintenance

#### Logging

Configure logging in `settings/production.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

#### Backup Strategy

1. Database backups:

```bash
# Create backup script
#!/bin/bash
BACKUP_DIR="/path/to/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
docker-compose -f docker-compose.prod.yml exec db pg_dump -U $DB_USER $DB_NAME > "$BACKUP_DIR/db_backup_$TIMESTAMP.sql"
```

2. Media backups (if not using S3):

```bash
# Backup media files
tar -czf "$BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz" /path/to/media/folder
```

#### Monitoring

1. Set up monitoring tools:

- Sentry for error tracking
- Prometheus + Grafana for metrics
- ELK Stack for log management

2. Configure health checks:

```python
# urls.py
path('health/', include('health_check.urls'))
```

### 8. Security Checklist

- [ ] SSL certificate installed and configured
- [ ] Environment variables secured
- [ ] Database backup system in place
- [ ] Firewall configured
- [ ] Security headers implemented
- [ ] Rate limiting configured
- [ ] Regular security updates scheduled
- [ ] Error monitoring configured
- [ ] Performance monitoring set up
- [ ] Backup strategy implemented and tested

### 9. Scaling Considerations

1. Horizontal Scaling:

- Use load balancer
- Configure sticky sessions
- Scale web and worker containers

2. Caching Strategy:

- Configure Redis caching
- Implement page caching
- Set up CDN for static/media files

3. Database Optimization:

- Regular maintenance
- Query optimization
- Connection pooling
- Read replicas (if needed)

### 10. Troubleshooting

Common issues and solutions:

1. Static files not showing:

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input
```

2. Database connection issues:

```bash
docker-compose -f docker-compose.prod.yml exec db psql -U $DB_USER -d $DB_NAME
```

3. Permission issues:

```bash
sudo chown -R $USER:$USER .
```

4. Container logs:

```bash
docker-compose -f docker-compose.prod.yml logs -f [service_name]
```

### 11. Updating the Application

1. Pull latest changes:

```bash
git pull origin main
```

2. Rebuild containers:

```bash
docker-compose -f docker-compose.prod.yml build
```

3. Apply migrations:

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

4. Restart services:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 12. Support

For production support:

- Email: support@yourdomain.com
- Emergency contact: +1-XXX-XXX-XXXX
- Documentation: https://docs.yourdomain.com
