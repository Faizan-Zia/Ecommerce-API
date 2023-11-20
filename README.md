# Ecommerce-API

## Overview
The Ecommerce-backend-API enables admininstrators keep track of the inventory, sales and revenues. 

### Access API Docs
A detailed breakdown of the API can be access by navigating to the `/docs` endpoint (you will be automatically redirected to the documentation when you spin up the container).

## Installation Steps
You can use the docker image with all the dependencies pre-installed here:
```
docker pull faizanzia1/ecommerce-backend
```

Once pulled, run the container by using the following command:
```
docker run -it -p 8000:8000 faizanzia1/ecommerce-backend
```

You could also build the Dockerfile available at the root of the repository. Simply clone the repository and build the Dockerfile. You can use the following command for that:
```
docker build -t Ecommerce-backend .
```

Once built, run the container using the command mentioned in the pre-configured docker image section.

## Database Guide
Since the requirement dictated the use of a relational database, Postgres was our choice of relational database with the Masonite-ORM at the helm of the migrations and database interactions. 

### Entities and Relations
Keeping things simple, we stuck with the classic Products and Orders entities with additional Categories and OrderItems to break stuff down into different contexts. Here is the breakdown of the tables and their relations:
- Users: primarily used for authentication and authorization (JWT to the rescue). 
    - The Orders table uses the logged in user. A single user can have many orders.
- Product Categories: To be managed by Admins. Contains only name and description.
- Products: The actual products. One product would only belong to one category.
- Order Items: Essentially what the orders are composed of. The Order Items keep track of the product, and the quantity in which that product was purchased.
- Orders: Important for revenue and sales management. A single order can have multiple order items. The API itself supports accessing Order Items on the basis of the Order Id.