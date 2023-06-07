# Shop
## About project

The Shop application is the backend of an online store. The application includes the following features:

- Adding to the database via the Django admin panel: products, product categories, product 
manufacturers, discounts, promotional codes.
- Customer registration through the REST API interface with email confirmation.
- Customer authentication using JWT tokens.
- Automatic email distribution of products with current discounts.
- Order placement through the REST API interface.

This project written in Python using the *Django* framework. For installation using the *Docker*.


## Installation

Clone the repository from GitHub:

```sh
git clone https://github.com/maximchikAlexandr/shop.git
```

Create a file named '.env' in the root directory:

```sh
cd shop/
nano .env
```

and fill it with the following environment variables:

```sh
# Django application parameters
DEBUG=True
SECRET_KEY="the_key_used_for_encryption"
DJANGO_SETTINGS_MODULE=shop_project.settings
DJANGO_APP_HOST=web
DJANGO_APP_PORT=8000

# Database parameters
POSTGRES_DB="database_name"
POSTGRES_USER="your_database_username"
POSTGRES_PASSWORD="your_database_password"
POSTGRES_HOST=postgres_db
POSTGRES_PORT="port_of_your_database_in_container"
DB_OUT_PORT="outer_port_of_your_database"

# Email sending parameters
EMAIL_HOST_PASSWORD="gmail_password_for_your_application"
EMAIL_HOST_USER="your_full_gmail_address"
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

# Celery parameters
CELERY_PORT="celery_port"
CELERY_HOST="celery_host"

# Telegram Bot parameters
TELEGRAM_TOKEN="your_token_to_access_the_HTTP_API"
```

Create and start the docker containers:

```sh
docker compose up -d
```

If the application is deployed on the local machine, open the browser and navigate to the 
project's admin page at: 

http://localhost:8001/admin/


## Gmail SMTP server
To use the application, access to a Simple Mail Transfer Protocol (SMTP) server is required. 
To set up Gmail SMTP, obtain the password for your application. 
Instructions on how to do this are provided in the documentation: 

https://support.google.com/accounts/answer/185833

## Token for Telegram Bot API
Obtaining a token is as simple as contacting [@BotFather](https://t.me/botfather)
, issuing the **/newbot** 
command and following the steps until you're given a new token.


You can find a step-by-step guide:
https://core.telegram.org/bots/features#creating-a-new-bot


## API Documentation
Swagger is utilized for API documentation. If the application is deployed on the local machine, 
the documentation can be accessed through the following link:


http://localhost:8001/doc/
