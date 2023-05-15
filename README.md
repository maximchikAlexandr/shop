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
SECRET_KEY=some_key
DJANGO_SETTINGS_MODULE=shop_project.settings
DEBUG=True
POSTGRES_DB=some_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=some_password1
POSTGRES_HOST=postgres_db
POSTGRES_PORT=some_port1
DB_OUT_PORT=some_port2
EMAIL_HOST_PASSWORD=some_password2
EMAIL_HOST_USER=our_email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
CELERY_PORT=some_port2
CELERY_HOST=some_host
```

Create and start the docker containers:

```sh
docker compose up -d
```

Open up the browser and navigate to the main page of the project at http://localhost:8001/.

## Gmail SMTP server
SMTP (Simple Mail Transfer Protocol) 

## Swagger
