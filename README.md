# Social Media LoveLink
LoveLink - own pet project, a dating platform that helps people find new acquaintances.

Project stack:
  ```
  -Django/DRF
  -PostgreSQL
  -Redis
  -Celery/Celery Beat
  -Docker/docker-desctop
  ```
## Project Deployment

1. Clone repository
   ```bash
   git clone https://github.com/MishaHmilenko/lovelink
   ```

2. Create `.env` file
   ```
    DEBUG=True
    SECRETKEY=your_secret_key

    APP_PORT=8000
    
    DB_USER=your_db_user
    DB_PASSWORD=yor_db_password
    DB_NAME=your_db_name
    DB_HOST=your_db_host
    DB_PORT=5432
    
    
    EMAIL_HOST=your_email_host
    EMAIL_PORT=your_email_port
    EMAIL_HOST_USER=your_email_user
    EMAIL_HOST_PASSWORD=your_email_password
    EMAIL_USE_TLS=True
    
    
    STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
    STRIPE_SECRET_KEY=your_stripe_secret_key
    STRIPE_ENDPOINT_SECRET=your_endpoint_secret
    
    REDIS_HOST=your_redis_host
    REDIS_PORT=6379
    
    NGINX_PORT=80
   ```

3. Launching a project in containers
   ```bash
   docker-compose up --build
   ```

4.  The application is available at
    ```
    localhost:80/
    ```

