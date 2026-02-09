# AI Todo App - Deployment Guide

## Table of Contents
1. [Quick Start (Development)](#quick-start-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment (Linux)](#production-deployment-linux)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [SSL/HTTPS Setup](#sslhttps-setup)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start (Development)

### Windows
```bash
# Double-click start.bat or run:
start.bat
```

### Linux/Mac
```bash
# Make scripts executable
chmod +x start.sh stop.sh

# Start services
./start.sh

# Stop services
./stop.sh
```

The scripts will:
- Check prerequisites (Python, Node.js)
- Create virtual environment
- Install dependencies
- Run database migrations
- Start backend (http://localhost:8000)
- Start frontend (http://localhost:3000)

---

## Docker Deployment

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Setup

1. **Copy environment file:**
```bash
cp .env.docker .env
```

2. **Edit .env and add your API keys:**
```bash
# Required
OPENAI_API_KEY=sk-your-key-here
SECRET_KEY=your-secret-key-min-32-chars

# Optional
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

3. **Start services:**
```bash
docker-compose up -d
```

4. **Check status:**
```bash
docker-compose ps
docker-compose logs -f
```

5. **Access application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service_name]

# Restart a service
docker-compose restart [service_name]

# Rebuild after code changes
docker-compose up -d --build

# Run migrations
docker-compose exec backend alembic upgrade head

# Access database
docker-compose exec postgres psql -U aitodo -d aitodo_db

# Clean up (removes volumes)
docker-compose down -v
```

---

## Production Deployment (Linux)

### Prerequisites
- Ubuntu 20.04+ or similar Linux distribution
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Nginx
- Domain name with DNS configured

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv \
    nodejs npm postgresql postgresql-contrib nginx \
    certbot python3-certbot-nginx git

# Create application user
sudo useradd -m -s /bin/bash aitodo
sudo usermod -aG www-data aitodo
```

### Step 2: Database Setup

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE aitodo_db;
CREATE USER aitodo WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE aitodo_db TO aitodo;
\q
```

### Step 3: Application Deployment

```bash
# Clone repository
sudo mkdir -p /var/www
sudo chown aitodo:www-data /var/www
sudo -u aitodo git clone https://github.com/yourusername/aitodo.git /var/www/aitodo
cd /var/www/aitodo

# Backend setup
cd phase-2-web/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
nano .env  # Edit with your configuration

# Run migrations
alembic upgrade head

# Frontend setup
cd ../frontend
npm install
npm run build

# Set permissions
sudo chown -R aitodo:www-data /var/www/aitodo
sudo chmod -R 755 /var/www/aitodo
```

### Step 4: Systemd Services

```bash
# Copy service files
sudo cp deployment/systemd/aitodo-backend.service /etc/systemd/system/
sudo cp deployment/systemd/aitodo-frontend.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start services
sudo systemctl enable aitodo-backend aitodo-frontend
sudo systemctl start aitodo-backend aitodo-frontend

# Check status
sudo systemctl status aitodo-backend
sudo systemctl status aitodo-frontend
```

### Step 5: Nginx Configuration

```bash
# Copy nginx configuration
sudo cp deployment/nginx/aitodo.conf /etc/nginx/sites-available/aitodo

# Edit configuration with your domain
sudo nano /etc/nginx/sites-available/aitodo

# Enable site
sudo ln -s /etc/nginx/sites-available/aitodo /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### Step 6: SSL Certificate (Let's Encrypt)

```bash
# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run

# Certificate will auto-renew via cron
```

---

## Environment Configuration

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://aitodo:password@localhost:5432/aitodo_db

# JWT
SECRET_KEY=your-secret-key-min-32-chars-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Services (at least one required)
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# MCP Server
MCP_SERVER_URL=http://localhost:8001

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_CLIENT_ID=your-facebook-client-id
FACEBOOK_CLIENT_SECRET=your-facebook-client-secret
```

### Frontend (.env.local)

```bash
# Production
NEXT_PUBLIC_API_URL=https://yourdomain.com/api

# Development
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Generate Secure Keys

```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Generate random password
openssl rand -base64 32
```

---

## Database Setup

### Initial Migration

```bash
cd phase-2-web/backend
source .venv/bin/activate
alembic upgrade head
```

### Create New Migration

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Rollback Migration

```bash
# Rollback one version
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>
```

### Database Backup

```bash
# Backup
pg_dump -U aitodo -d aitodo_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
psql -U aitodo -d aitodo_db < backup_20260208_120000.sql
```

---

## SSL/HTTPS Setup

### Using Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
# Test renewal
sudo certbot renew --dry-run
```

### Using Custom Certificate

```bash
# Copy certificate files
sudo cp your-cert.crt /etc/ssl/certs/
sudo cp your-key.key /etc/ssl/private/

# Update nginx configuration
ssl_certificate /etc/ssl/certs/your-cert.crt;
ssl_certificate_key /etc/ssl/private/your-key.key;

# Reload nginx
sudo systemctl reload nginx
```

---

## Monitoring & Maintenance

### Service Logs

```bash
# Backend logs
sudo journalctl -u aitodo-backend -f

# Frontend logs
sudo journalctl -u aitodo-frontend -f

# Nginx logs
sudo tail -f /var/log/nginx/aitodo_access.log
sudo tail -f /var/log/nginx/aitodo_error.log
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000

# Database connection
psql -U aitodo -d aitodo_db -c "SELECT 1;"
```

### Performance Monitoring

```bash
# System resources
htop

# Disk usage
df -h

# Database size
psql -U aitodo -d aitodo_db -c "SELECT pg_size_pretty(pg_database_size('aitodo_db'));"

# Active connections
psql -U aitodo -d aitodo_db -c "SELECT count(*) FROM pg_stat_activity;"
```

### Automated Backups

Create backup script `/usr/local/bin/backup-aitodo.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/aitodo"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U aitodo -d aitodo_db | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

Add to crontab:
```bash
sudo crontab -e
# Add line:
0 2 * * * /usr/local/bin/backup-aitodo.sh
```

---

## Troubleshooting

### Backend Won't Start

```bash
# Check logs
sudo journalctl -u aitodo-backend -n 50

# Common issues:
# 1. Database connection
psql -U aitodo -d aitodo_db -c "SELECT 1;"

# 2. Missing environment variables
cat /var/www/aitodo/phase-2-web/backend/.env

# 3. Port already in use
sudo lsof -i :8000

# 4. Permission issues
sudo chown -R aitodo:www-data /var/www/aitodo
```

### Frontend Won't Start

```bash
# Check logs
sudo journalctl -u aitodo-frontend -n 50

# Rebuild
cd /var/www/aitodo/phase-2-web/frontend
npm run build

# Check environment
cat .env.local
```

### Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -U aitodo -d aitodo_db

# Reset password
sudo -u postgres psql
ALTER USER aitodo WITH PASSWORD 'new_password';
```

### SSL Certificate Issues

```bash
# Check certificate
sudo certbot certificates

# Renew manually
sudo certbot renew

# Check nginx configuration
sudo nginx -t
```

### High Memory Usage

```bash
# Check processes
ps aux --sort=-%mem | head

# Restart services
sudo systemctl restart aitodo-backend aitodo-frontend

# Optimize PostgreSQL
# Edit /etc/postgresql/*/main/postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
```

---

## Security Checklist

- [ ] Change default passwords
- [ ] Use strong SECRET_KEY (32+ characters)
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall (ufw)
- [ ] Keep dependencies updated
- [ ] Regular backups
- [ ] Monitor logs for suspicious activity
- [ ] Use environment variables for secrets
- [ ] Restrict database access
- [ ] Enable fail2ban for SSH

---

## Updating the Application

```bash
# Pull latest code
cd /var/www/aitodo
sudo -u aitodo git pull

# Update backend
cd phase-2-web/backend
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart aitodo-backend

# Update frontend
cd ../frontend
npm install
npm run build
sudo systemctl restart aitodo-frontend

# Clear nginx cache (if applicable)
sudo systemctl reload nginx
```

---

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/aitodo/issues
- Documentation: See docs/ directory
- Email: support@yourdomain.com
