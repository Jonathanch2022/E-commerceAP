from os import name
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime, func
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


ma = Marshmallow()

class Base(DeclarativeBase):
   pass
#create flask app instance
app = Flask(__name__)

#configure the MySQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Mdnk9966200723%40@localhost/ecommerce_api'
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
   user = relationship("User", back_populates="order", cascade="all, delete-orphan")
 
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
 
class UserShema(ma.SQLAlchemyAutoSchema):
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

      

@app.route('/')
def hello():
    users = User.query.all()
    return (UserShema(many=True).dump(users))
    

@app.route('/home')
def home():
    return("This is the home route")

if(__name__ == "__main__"):
  app.run()