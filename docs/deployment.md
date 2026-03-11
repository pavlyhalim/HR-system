# Deployment Guide

## Production Deployment

### 1. Server Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Disk | 20 GB SSD | 50+ GB SSD |
| OS | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |

### 2. Install System Dependencies

```bash
sudo apt update && sudo apt install -y \
  python3.12 python3.12-venv python3.12-dev \
  postgresql postgresql-contrib \
  redis-server \
  nginx \
  supervisor
```

### 3. Create Application User

```bash
sudo useradd -m -s /bin/bash hr-system
sudo su - hr-system
```

### 4. Clone & Setup

```bash
git clone <repository-url> /home/hr-system/app
cd /home/hr-system/app

python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 5. Production Environment

```bash
cp .env.example .env
```

Edit `.env` for production:

```ini
DEBUG=False
SECRET_KEY=<generate-a-256-bit-random-key>
ALLOWED_HOSTS=your-domain.com,api.your-domain.com
DJANGO_SETTINGS_MODULE=config.settings.production

DB_NAME=hr-dashboard
DB_USER=hr_prod
DB_PASSWORD=<strong-password>
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

CORS_ALLOWED_ORIGINS=https://your-frontend.com
```

### 6. Database Setup

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE "hr-dashboard";
CREATE USER hr_prod WITH PASSWORD 'strong-password-here';
ALTER ROLE hr_prod SET client_encoding TO 'utf8';
ALTER ROLE hr_prod SET default_transaction_isolation TO 'read committed';
ALTER ROLE hr_prod SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE "hr-dashboard" TO hr_prod;
\q
```

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 7. Gunicorn Configuration

Create `/home/hr-system/gunicorn.conf.py`:

```python
bind = "127.0.0.1:8000"
workers = 4                    # 2 * CPU cores + 1
worker_class = "gthread"
threads = 2
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
accesslog = "/var/log/hr-system/gunicorn-access.log"
errorlog = "/var/log/hr-system/gunicorn-error.log"
loglevel = "info"
```

### 8. Supervisor Configuration

Create `/etc/supervisor/conf.d/hr-system.conf`:

```ini
[program:hr-system]
command=/home/hr-system/app/.venv/bin/gunicorn config.wsgi:application -c /home/hr-system/gunicorn.conf.py
directory=/home/hr-system/app
user=hr-system
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/hr-system/supervisor.log

[program:hr-celery-worker]
command=/home/hr-system/app/.venv/bin/celery -A config worker -l info
directory=/home/hr-system/app
user=hr-system
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/hr-system/celery-worker.log

[program:hr-celery-beat]
command=/home/hr-system/app/.venv/bin/celery -A config beat -l info
directory=/home/hr-system/app
user=hr-system
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/hr-system/celery-beat.log
```

```bash
sudo mkdir -p /var/log/hr-system
sudo chown hr-system:hr-system /var/log/hr-system
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
```

### 9. Nginx Configuration

Create `/etc/nginx/sites-available/hr-system`:

```nginx
server {
    listen 80;
    server_name api.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.your-domain.com;

    ssl_certificate     /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;

    client_max_body_size 20M;

    location /static/ {
        alias /home/hr-system/app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/hr-system/app/media/;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/hr-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.your-domain.com
```

---

## Docker Deployment (Alternative)

### Dockerfile

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### docker-compose.yml

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: hr-dashboard
      POSTGRES_USER: hr_prod
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    env_file: .env
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    command: >
      sh -c "python manage.py migrate &&
             gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4"

  celery:
    build: .
    env_file: .env
    depends_on:
      - db
      - redis
    command: celery -A config worker -l info

  celery-beat:
    build: .
    env_file: .env
    depends_on:
      - db
      - redis
    command: celery -A config beat -l info

volumes:
  pgdata:
```

```bash
docker compose up -d
docker compose exec web python manage.py createsuperuser
```

---

## Production Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` (256-bit random)
- [ ] HTTPS enabled (SSL certificate)
- [ ] `ALLOWED_HOSTS` set to actual domain(s)
- [ ] `CORS_ALLOWED_ORIGINS` set to frontend URL(s)
- [ ] Database backups configured (pg_dump cron)
- [ ] Log rotation configured
- [ ] Supervisor/systemd auto-restart enabled
- [ ] Static files collected (`collectstatic`)
- [ ] Firewall rules (only 80/443 public)
- [ ] Redis password set (production)
- [ ] Database user with minimal privileges
- [ ] Monitoring (health check endpoint)
