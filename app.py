

import json
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Undefined
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime, func
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import ValidationError

ma = Marshmallow()

class Base(DeclarativeBase):
   pass
#create flask app instance
app = Flask(__name__)

userName = "root"
password = "MYSQL_PASSWORD_HERE"
database = "ecommerce_api"
host = "localhost"
#configure the MySQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{userName}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db= SQLAlchemy(model_class=Base)
db.init_app(app)
ma.init_app(app)

class User(db.Model):
   __tablename__ = 'user'
   id: Mapped[int] = mapped_column(primary_key = True, autoincrement=True)
   name: Mapped[str] = mapped_column(String(100))
   address: Mapped[str] = mapped_column(String(250))
   email:Mapped[str] = mapped_column(String(100),unique=True)
   orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
   
class Order(db.Model):
   __tablename__ = 'order'
   id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
   order_date: Mapped[DateTime] = mapped_column(DateTime,server_default=func.now())
   user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable= False)
   user = relationship("User", back_populates="orders")
 
class Product(db.Model):
   __tablename__ = "product"
   id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
   product_name: Mapped[str] = mapped_column(String(500))
   price: Mapped[float] = mapped_column(default=0)
   
class Order_ProductAssociation(db.Model):
   __tablename__ = "order_productassociation"
   order_id: Mapped[int] = mapped_column(ForeignKey('order.id'),primary_key=True)
   product_id: Mapped[int] = mapped_column(ForeignKey('product.id'),primary_key=True)
   
with app.app_context():
   db.create_all()
 
class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
     model = User
     load_instance = True
     
  id = ma.auto_field()
  name = ma.auto_field()
  address = ma.auto_field()
  email = ma.auto_field()
    
class ProductScheme(ma.SQLAlchemyAutoSchema):
   class Meta:
      model = Product
      load_instance = True
      
   id = ma.auto_field()
   product_name = ma.auto_field()
   price = ma.auto_field()

class OrderSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
      model = Order
      load_instance = True
      include_fk = True
      
   id = ma.auto_field()
   order_date = ma.auto_field()
   user_id = ma.auto_field()
   
class ProductAssociationSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
      model = Order_ProductAssociation
      load_instance = True
      include_fk = True
      
   order_id = ma.auto_field()
   product_id = ma.auto_field()
  
#Table User Routes 
#Retursn all users 
@app.route('/users',methods=["GET"])
def users():
    users = User.query.all()
    return (UserSchema(many=True).dump(users))
#Gets user by id    
@app.route('/users/<int:id>',methods=["GET"])
def user_detail(id):
  try:
    if(id >= 0):
        user = User.query.get(id)
        return(UserSchema(many=False).dump(user))
    else:
        return(jsonify("No user id provided"))
  except ValidationError as e:
     return(jsonify(e))
 #Creates a new user
@app.route('/users/', methods=["POST"])
def create_user(): 
   try:
       json_data = request.get_json()
       new_user : User = UserSchema().load(json_data)
       db.session.add(new_user)
       db.session.commit()
       return(jsonify("User created successfully!"))
   except ValidationError as e:
      return(jsonify(e))
 #Updates the user with user id  
@app.route('/users/<int:id>', methods=["PUT"])
def update_user(id):
    try:
        json_data = request.get_json()
        user = User.query.get(id)
        userUpdate: User = UserSchema().load(json_data, instance=user, partial=True)
        db.session.commit()
        return(jsonify("User updated successfully!"))
    except ValidationError as e:
        return(jsonify(e))
 #deletes user with id   
@app.route('/users/<int:id>',methods=["DELETE"])
def delete_user(id):
   try:
       user = User.query.get(id)
       if user:
           db.session.delete(user)
           db.session.commit()
           return(jsonify("User Deleted!"))
       else:
          return(jsonify("User does not exist!"))
   except ValidationError as e:
       return(e)
 
#Table Products Routes 
#returns all products
@app.route('/products',methods=["GET"])
def products():
    product = Product.query.all()
    return (ProductScheme(many=True).dump(product))
#returns product with product id    
@app.route('/products/<int:id>',methods=["GET"])
def product_detail(id):
  try:
    if(id >= 0):
        product = Product.query.get(id)
        return(ProductScheme(many=False).dump(product))
    else:
        return(jsonify("No product id provided"))
  except ValidationError as e:
     return(jsonify(e))
 #creates anew product
@app.route('/products/', methods=["POST"])
def create_product(): 
   try:
       json_data = request.get_json()
       new_product : Product = ProductScheme().load(json_data)
       db.session.add(new_product)
       db.session.commit()
       return(jsonify("Product created successfully!"))
   except ValidationError as e:
      return(jsonify(e))
#updates the product with with id   
@app.route('/products/<int:id>', methods=["PUT"])
def update_product(id):
    try:
        json_data = request.get_json()
        product = Product.query.get(id)
        productUpdate: Product = ProductScheme().load(json_data, instance=product, partial=True)
        db.session.commit()
        return(jsonify("Product Updated Successfully!"))
    except ValidationError as e:
        return(jsonify(e))
#deletes the product with id    
@app.route('/products/<int:id>',methods=["DELETE"])
def delete_product(id):
   try:
       product = Product.query.get(id)
       if product:
           db.session.delete(product)
           db.session.commit()
           return(jsonify("Product Deleted!"))
       else:
          return(jsonify("Product does not exist!"))
   except ValidationError as e:
       return(e)
   
#Table ordrs routes
#return all orders for user with user_id
@app.route('/orders/user/<int:user_id>',methods=["GET"])
def orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return (OrderSchema(many=True).dump(orders))


#return all products for order    
@app.route('/orders/<int:id>/products',methods=["GET"])
def product_order_details(id):
  try:
    
    order = Order.query.get(id)
    if(order):    
        if order:
           orders = Order_ProductAssociation.query.filter_by(order_id=id).all()
           prd_list = []
           for t in orders:
             pr = Product.query.get(t.product_id)
             prd_list.append(ProductScheme(many=False).dump(pr))   
           return(jsonify(prd_list))       
    else:
        return(jsonify("Order not found"))
  except ValidationError as e:
     return(jsonify(e))

#Create a new order
@app.route('/orders/', methods=["POST"])
def create_order(): 
   try:
       json_data = request.get_json()
       new_order : Order = OrderSchema().load(json_data)
       db.session.add(new_order)
       db.session.commit()
       return(jsonify("Order created successfully!"))
   except ValidationError as e:
      return(jsonify(e))
 
  #Add product to order 
@app.route('/orders/<int:orderid>/add_product/<int:product_id>', methods=["PUT"])
def update_order(orderid,product_id):
    try:
       
        order = Order.query.get(orderid)
        prd = Product.query.get(product_id)
        checkproduct = Order_ProductAssociation.query.get((orderid,product_id))
        if not checkproduct:
            if order:
                if prd:
                    prdAsc = Order_ProductAssociation(order_id=orderid,product_id=product_id)
                    db.session.add(prdAsc)
                    db.session.commit()
                    return(jsonify("Product added to order!"))
                else:
                   return(jsonify("Product does not exist"))      
            else:
               return(jsonify("Order does not exist"))
        else:
           return(jsonify("product order already exist"))
    except ValidationError as e:
        return(jsonify(e))
#Delete a product from order 
@app.route('/orders/<int:orderid>/remove_product/<int:product_id>', methods=["DELETE"])
def delete_productOrder(orderid,product_id):
    try:
        
        productOrder = Order_ProductAssociation.query.get((orderid,product_id))
        if not productOrder:
            
               return(jsonify("Product Order does not exist"))
        else:
           db.session.delete(productOrder)
           db.session.commit()
           return(jsonify("Product order deleted"))
    except ValidationError as e:
        return(jsonify(e))
 #Delete order with order id   
@app.route('/orders/<int:id>',methods=["DELETE"])
def delete_order(id):
   try:
       order = Order.query.get(id)
       if order:
           db.session.delete(order)
           db.session.commit()
           return(jsonify("Order Deleted!"))
       else:
          return(jsonify("Order does not exist!"))
   except ValidationError as e:
       return(e)

if(__name__ == "__main__"):
  app.run()