# AWS EC2 Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [AWS EC2 Setup](#aws-ec2-setup)
3. [Server Configuration](#server-configuration)
4. [Application Deployment](#application-deployment)
5. [Database Setup](#database-setup)
6. [Nginx Configuration](#nginx-configuration)
7. [SSL Certificate Setup](#ssl-certificate-setup)
8. [Systemd Service Setup](#systemd-service-setup)
9. [Monitoring and Logs](#monitoring-and-logs)
10. [Troubleshooting](#troubleshooting)

## Prerequisites

Before starting deployment, ensure you have:
- AWS account with EC2 access
- GitHub repository with your code
- Domain name (optional, for SSL)
- Basic knowledge of Linux commands
- SSH client installed

## AWS EC2 Setup

### Step 1: Launch EC2 Instance

1. **Log into AWS Console**
   - Go to [AWS Console](https://console.aws.amazon.com)
   - Navigate to EC2 service

2. **Launch Instance**
   - Click "Launch Instance"
   - Choose "Ubuntu Server 20.04 LTS" (Free tier eligible)
   - Select "t2.micro" instance type
   - Create or select a key pair for SSH access
   - Configure security group (see below)
   - Launch instance

3. **Security Group Configuration**
   Create a security group with the following rules:
   ```
   SSH (22) - Your IP
   HTTP (80) - 0.0.0.0/0
   HTTPS (443) - 0.0.0.0/0
   Custom TCP (5000) - 0.0.0.0/0 (for testing)
   ```

4. **Get Instance Details**
   - Note the public IP address
   - Note the instance ID
   - Download the key pair (.pem file)

### Step 2: Connect to EC2 Instance

```bash
# Make key file secure
chmod 400 your-key-pair.pem

# Connect to instance
ssh -i your-key-pair.pem ubuntu@your-ec2-public-ip
```

## Server Configuration

### Step 1: Update System

```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git vim htop
```

### Step 2: Install Python and Dependencies

```bash
# Install Python 3.8+ and pip
sudo apt install -y python3 python3-pip python3-venv python3-dev

# Install build essentials (for psycopg2)
sudo apt install -y build-essential libpq-dev

# Verify installation
python3 --version
pip3 --version
```

### Step 3: Install PostgreSQL

```bash
# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE chatbot_db;
CREATE USER chatbot_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO chatbot_user;
ALTER USER chatbot_user CREATEDB;
\q
```

### Step 4: Install Nginx

```bash
# Install Nginx
sudo apt install -y nginx

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx
```

### Step 5: Install Node.js (for npm if needed)

```bash
# Install Node.js (optional, for frontend build tools)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

## Application Deployment

### Step 1: Clone Repository

```bash
# Create application directory
sudo mkdir -p /var/www/chatbot-app
sudo chown ubuntu:ubuntu /var/www/chatbot-app

# Clone your repository
cd /var/www/chatbot-app
git clone https://github.com/yourusername/chatbot-app.git .

# Or if you have SSH key set up:
# git clone git@github.com:yourusername/chatbot-app.git .
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Gunicorn for production
pip install gunicorn
```

### Step 3: Configure Environment Variables

```bash
# Create production environment file
nano .env
```

Add the following content:
```bash
# Production Environment Variables
GEMINI_API_KEY=your_actual_gemini_api_key
DATABASE_URL=postgresql://chatbot_user:your_secure_password@localhost:5432/chatbot_db
FLASK_ENV=production
SECRET_KEY=your_very_secure_secret_key_here
PORT=5000
HOST=0.0.0.0
```

### Step 4: Set Up Database

```bash
# Run database setup script
psql -U chatbot_user -d chatbot_db -f database_setup.sql

# Test database connection
python3 -c "
from models import db
if db.connect():
    print('Database connection successful')
    db.disconnect()
else:
    print('Database connection failed')
"
```

### Step 5: Test Application

```bash
# Test the application
python3 app.py

# In another terminal, test the API
curl http://localhost:5000/api/health
```

## Database Setup

### Step 1: Configure PostgreSQL for Production

```bash
# Edit PostgreSQL configuration
sudo nano /etc/postgresql/12/main/postgresql.conf

# Find and modify these settings:
# listen_addresses = 'localhost'
# port = 5432
# max_connections = 100

# Edit authentication
sudo nano /etc/postgresql/12/main/pg_hba.conf

# Add this line for local connections:
# local   all             chatbot_user                              md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Step 2: Create Database Backup Script

```bash
# Create backup script
nano /var/www/chatbot-app/backup_db.sh
```

Add the following content:
```bash
#!/bin/bash
BACKUP_DIR="/var/www/chatbot-app/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/chatbot_db_$DATE.sql"

mkdir -p $BACKUP_DIR

pg_dump -U chatbot_user -h localhost chatbot_db > $BACKUP_FILE

# Keep only last 7 days of backups
find $BACKUP_DIR -name "chatbot_db_*.sql" -mtime +7 -delete

echo "Database backup completed: $BACKUP_FILE"
```

```bash
# Make script executable
chmod +x /var/www/chatbot-app/backup_db.sh

# Test backup
/var/www/chatbot-app/backup_db.sh
```

## Nginx Configuration

### Step 1: Create Nginx Configuration

```bash
# Create Nginx site configuration
sudo nano /etc/nginx/sites-available/chatbot-app
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;  # Replace with your domain

    # Redirect HTTP to HTTPS (after SSL setup)
    # return 301 https://$server_name$request_uri;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static {
        alias /var/www/chatbot-app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
```

### Step 2: Enable Site

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/chatbot-app /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

## SSL Certificate Setup

### Step 1: Install Certbot

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx
```

### Step 2: Obtain SSL Certificate

```bash
# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

### Step 3: Update Nginx Configuration for HTTPS

```bash
# Certbot should have automatically updated your configuration
# Verify the configuration
sudo nginx -t
sudo systemctl reload nginx
```

## Systemd Service Setup

### Step 1: Create Systemd Service

```bash
# Create systemd service file
sudo nano /etc/systemd/system/chatbot-app.service
```

Add the following content:
```ini
[Unit]
Description=Chatbot Application
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=exec
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/chatbot-app
Environment=PATH=/var/www/chatbot-app/venv/bin
ExecStart=/var/www/chatbot-app/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 3 app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 2: Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable chatbot-app

# Start service
sudo systemctl start chatbot-app

# Check status
sudo systemctl status chatbot-app

# View logs
sudo journalctl -u chatbot-app -f
```

## Monitoring and Logs

### Step 1: Set Up Log Rotation

```bash
# Create logrotate configuration
sudo nano /etc/logrotate.d/chatbot-app
```

Add the following content:
```
/var/www/chatbot-app/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
    postrotate
        systemctl reload chatbot-app
    endscript
}
```

### Step 2: Set Up Monitoring Script

```bash
# Create monitoring script
nano /var/www/chatbot-app/monitor.sh
```

Add the following content:
```bash
#!/bin/bash

# Check if application is running
if ! systemctl is-active --quiet chatbot-app; then
    echo "$(date): Chatbot app is not running, restarting..." >> /var/log/chatbot-monitor.log
    systemctl restart chatbot-app
fi

# Check if Nginx is running
if ! systemctl is-active --quiet nginx; then
    echo "$(date): Nginx is not running, restarting..." >> /var/log/chatbot-monitor.log
    systemctl restart nginx
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "$(date): Disk usage is high: ${DISK_USAGE}%" >> /var/log/chatbot-monitor.log
fi
```

```bash
# Make script executable
chmod +x /var/www/chatbot-app/monitor.sh

# Add to crontab for monitoring every 5 minutes
crontab -e
# Add this line:
# */5 * * * * /var/www/chatbot-app/monitor.sh
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Application Won't Start
```bash
# Check service status
sudo systemctl status chatbot-app

# Check logs
sudo journalctl -u chatbot-app -f

# Check if port is in use
sudo netstat -tlnp | grep :5000
```

#### 2. Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test database connection
psql -U chatbot_user -d chatbot_db -h localhost

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-12-main.log
```

#### 3. Nginx Issues
```bash
# Check Nginx status
sudo systemctl status nginx

# Test Nginx configuration
sudo nginx -t

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

#### 4. SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Renew certificate manually
sudo certbot renew

# Check certificate expiration
openssl x509 -in /etc/letsencrypt/live/your-domain.com/cert.pem -text -noout | grep "Not After"
```

### Performance Optimization

#### 1. Enable Gzip Compression
Add to Nginx configuration:
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

#### 2. Set Up Caching
Add to Nginx configuration:
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

#### 3. Database Optimization
```sql
-- Add indexes for better performance
CREATE INDEX CONCURRENTLY idx_messages_timestamp_desc ON messages(timestamp DESC);
CREATE INDEX CONCURRENTLY idx_messages_user_message ON messages USING gin(to_tsvector('english', user_message));
```

### Security Checklist

- [ ] Firewall configured (only necessary ports open)
- [ ] SSH key authentication enabled
- [ ] Password authentication disabled for SSH
- [ ] Regular security updates enabled
- [ ] SSL certificate installed and working
- [ ] Database user has minimal required permissions
- [ ] Application runs as non-root user
- [ ] Environment variables secured
- [ ] Log files have appropriate permissions
- [ ] Backup strategy implemented

### Backup Strategy

#### 1. Database Backups
```bash
# Daily backup script
0 2 * * * /var/www/chatbot-app/backup_db.sh
```

#### 2. Application Backups
```bash
# Weekly application backup
0 3 * * 0 tar -czf /backups/chatbot-app-$(date +\%Y\%m\%d).tar.gz /var/www/chatbot-app
```

#### 3. Configuration Backups
```bash
# Backup important configuration files
sudo cp /etc/nginx/sites-available/chatbot-app /backups/
sudo cp /etc/systemd/system/chatbot-app.service /backups/
```

This deployment guide provides a comprehensive approach to deploying your chat application on AWS EC2 with production-ready configurations.
