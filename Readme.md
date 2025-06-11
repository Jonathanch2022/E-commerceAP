🛒 E-Commerce REST API (Flask + MySQL)
This project is a RESTful API built with Flask, SQLAlchemy, and Marshmallow, designed to manage users, products, and orders for an e-commerce platform. The API connects to a MySQL database and supports full CRUD operations, as well as order-to-product relationships.

🔧 Tech Stack
Python 3

Flask

SQLAlchemy

MySQL (via PyMySQL)

Marshmallow (for schema validation and serialization)

⚙️ Setup Instructions
Install dependencies

bash
Copy
Edit
pip install Flask Flask-SQLAlchemy flask-marshmallow marshmallow-sqlalchemy pymysql
Configure MySQL

Create a database named ecommerce_api

Update the database URI in app.config['SQLALCHEMY_DATABASE_URI']:

perl
Copy
Edit
mysql+pymysql://<username>:<password>@localhost/ecommerce_api
Run the app

bash
Copy
Edit
python app.py
📦 API Overview
👤 Users
Method	Endpoint	Description
GET	/users	List all users
GET	/users/<id>	Get user by ID
POST	/users/	Create a new user
PUT	/users/<id>	Update user by ID
DELETE	/users/<id>	Delete user by ID

📦 Products
Method	Endpoint	Description
GET	/products	List all products
GET	/products/<id>	Get product by ID
POST	/products/	Create a new product
PUT	/products/<id>	Update product by ID
DELETE	/products/<id>	Delete product by ID

📑 Orders
Method	Endpoint	Description
GET	/orders/user/<user_id>	Get all orders for a user
GET	/orders/<id>/products	Get all products in an order
POST	/orders/	Create a new order
PUT	/orders/<order_id>/add_product/<product_id>	Add a product to an order (no duplicates)
DELETE	/orders/<order_id>/remove_product/<product_id>	Remove a product from an order
DELETE	/orders/<id>	Delete an order

📄 Data Models
User
id: int (primary key)

name: string

address: string

email: string (unique)

Product
id: int (primary key)

product_name: string

price: float

Order
id: int (primary key)

order_date: datetime (default: now)

user_id: foreign key to User

Order_ProductAssociation
Composite key: order_id + product_id

Many-to-many join table between orders and products

✅ Sample JSON
Create User
json
Copy
Edit
{
  "name": "John Doe",
  "email": "john@example.com",
  "address": "123 Main Street"
}
Create Product
json
Copy
Edit
{
  "product_name": "Gaming Keyboard",
  "price": 89.99
}
Create Order
json
Copy
Edit
{
  "user_id": 1
}
🛠 Notes
The app uses SQLAlchemy's ORM to define relationships.

Marshmallow is used to serialize/deserialize and validate incoming JSON data.

Routes are organized by resource type (users, products, orders).

Adding duplicate products to an order is prevented by checking existence in the join table before insert.
